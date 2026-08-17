#!/usr/bin/env node
/**
 * check_screen_registry.mjs — Node port of tools/check_screen_registry.py.
 *
 * Keeps the unpacked canvas-app source honest without Python, so the
 * Freebuff preview build step (which runs on a Node-only image) can guard
 * the same invariant as the repo's CI job:
 *
 *   1. A screen file exists (src/Src/scr_*.pa.yaml) but has no matching
 *      ScreensOrder entry in _EditorState.pa.yaml  -> FAIL
 *   2. A ScreensOrder entry has no matching screen file                  -> FAIL
 *
 * Usage:
 *   node tools/check_screen_registry.mjs [--src DIR] [--editor FILE]
 *
 * Defaults match the repo layout (src/Src + src/Src/_EditorState.pa.yaml).
 * Exit code 0 = registry consistent, 1 = mismatches found.
 */

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const TOOLS_DIR = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(TOOLS_DIR, "..");
const DEFAULT_SRC = path.join(REPO_ROOT, "src", "Src");
const DEFAULT_EDITOR = path.join(DEFAULT_SRC, "_EditorState.pa.yaml");

function parseArgs(argv) {
  const args = { src: DEFAULT_SRC, editor: DEFAULT_EDITOR };
  for (let i = 2; i < argv.length; i += 1) {
    if (argv[i] === "--src" && argv[i + 1]) {
      args.src = argv[i + 1];
      i += 1;
    } else if (argv[i] === "--editor" && argv[i + 1]) {
      args.editor = argv[i + 1];
      i += 1;
    }
  }
  return args;
}

function readText(p) {
  // Mirror Python's utf-8-sig: strip a leading BOM if present.
  let s = fs.readFileSync(p, "utf8");
  if (s.charCodeAt(0) === 0xfeff) s = s.slice(1);
  return s;
}

/** Screen name declared inside the file's `Screens:` block (first key). */
function screenNameFromFile(p) {
  const head = readText(p).slice(0, 2000);
  const m = head.match(/^Screens:\s*\n\s*([A-Za-z_][A-Za-z0-9_]*):/m);
  if (m) return m[1];
  const base = path.basename(p);
  return base.endsWith(".pa.yaml") ? base.slice(0, -".pa.yaml".length) : null;
}

/** Ordered list of screen names under `ScreensOrder:` in _EditorState. */
function editorScreens(p) {
  if (!fs.existsSync(p)) return [];
  const screens = [];
  let inOrder = false;
  for (const raw of readText(p).split("\n")) {
    const line = raw.trim();
    if (line.startsWith("ScreensOrder:")) {
      inOrder = true;
      continue;
    }
    if (!inOrder) continue;
    const m = line.match(/^-\s*([A-Za-z_][A-Za-z0-9_]*)\s*$/);
    if (m) {
      screens.push(m[1]);
    } else if (line.length > 0 && !line.startsWith("-")) {
      inOrder = false; // next top-level key
    }
  }
  return screens;
}

const args = parseArgs(process.argv);
const srcDir = path.resolve(args.src);
const editorPath = path.resolve(args.editor);

if (!fs.existsSync(srcDir) || !fs.statSync(srcDir).isDirectory()) {
  console.error(`ERROR: screen source directory not found: ${srcDir}`);
  process.exit(1);
}
if (!fs.existsSync(editorPath)) {
  console.error(`ERROR: _EditorState.pa.yaml not found: ${editorPath}`);
  process.exit(1);
}

const screenFiles = {}; // name -> filename
for (const name of fs.readdirSync(srcDir).sort()) {
  if (!name.endsWith(".pa.yaml")) continue;
  if (name === "App.pa.yaml" || name === "_EditorState.pa.yaml") continue;
  const p = path.join(srcDir, name);
  screenFiles[screenNameFromFile(p)] = name;
}

const registered = new Set(editorScreens(editorPath));

const unregistered = Object.keys(screenFiles)
  .filter((n) => !registered.has(n))
  .sort();
const orphaned = [...registered]
  .filter((n) => !(n in screenFiles))
  .sort();

const problems = [];
if (unregistered.length > 0) {
  problems.push(
    "Screen file(s) exist but are MISSING from _EditorState ScreensOrder: " +
      unregistered.map((n) => `${screenFiles[n]} (${n})`).join(", ")
  );
}
if (orphaned.length > 0) {
  problems.push(
    "_EditorState ScreensOrder entry(ies) with NO matching screen file: " +
      orphaned.join(", ")
  );
}

console.log("=".repeat(72));
console.log("Screen registry check — src/Src/*.pa.yaml <-> _EditorState.pa.yaml");
console.log("=".repeat(72));
console.log(`Screen files found : ${Object.keys(screenFiles).length}`);
console.log(`EditorState screens: ${registered.size}`);
for (const p of problems) console.log("FAIL:", p);
if (problems.length === 0) {
  console.log("OK: every screen file is registered and every entry has a file.");
}
console.log("-".repeat(72));
console.log(`Problems: ${problems.length}`);
process.exit(problems.length > 0 ? 1 : 0);
