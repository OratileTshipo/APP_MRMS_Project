/**
 * APP-MRMS Power App Structure Test Suite
 *
 * Validates the unpacked Power Apps canvas-app source, the Power Automate
 * flow import package, the SharePoint list schema CSVs, and the tooling —
 * all against the current single-repo layout (no APP_MRMS submodule).
 *
 * Run: npm test   (or: npx playwright test)
 */

import { test, expect } from '@playwright/test';
import { execFileSync } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';

const ROOT_DIR = path.resolve(__dirname, '..');
const SRC_DIR = path.join(ROOT_DIR, 'src', 'Src');
const FLOWS_DIR = path.join(ROOT_DIR, 'flows');
const TEMPLATE_DIR = path.join(FLOWS_DIR, 'templates', 'APP-MRMS-Approval');

// ============================================================================
// Test Group 1: Source Code Structure
// ============================================================================

test.describe('Source Code Structure', () => {
  const requiredScreens = [
    'App.pa.yaml',
    '_EditorState.pa.yaml',
    'scr_Splash.pa.yaml',
    'scr_Login.pa.yaml',
    'scr_Home.pa.yaml',
    'scr_Users.pa.yaml',
    'scr_MyActivities.pa.yaml',
    'scr_ReportForm.pa.yaml',
    'scr_ReportView.pa.yaml',
    'scr_Projects.pa.yaml',
    'scr_Activities.pa.yaml',
    'scr_ReportActivities.pa.yaml',
    'scr_Reports.pa.yaml',
    'scr_ApprovedReports.pa.yaml',
    'scr_ApprovalQueue.pa.yaml',
  ];

  test('should have all required screen files', () => {
    for (const screen of requiredScreens) {
      const filePath = path.join(SRC_DIR, screen);
      expect(fs.existsSync(filePath), `Missing screen: ${screen}`).toBeTruthy();
    }
  });

  test('should have no tab characters in any screen file', () => {
    // The Power Apps YAML dialect is indent-sensitive: tabs break Studio import.
    const yamlFiles = fs.readdirSync(SRC_DIR).filter((f) => f.endsWith('.pa.yaml'));
    expect(yamlFiles.length, 'no .pa.yaml files found in src/Src').toBeGreaterThan(0);

    for (const file of yamlFiles) {
      const content = fs.readFileSync(path.join(SRC_DIR, file), 'utf-8');
      expect(content, `Tab character in ${file}`).not.toContain('\t');
      expect(content.length, `${file} looks empty`).toBeGreaterThan(100);
    }
  });

  test('should have every screen file registered in _EditorState', () => {
    const editorState = fs.readFileSync(path.join(SRC_DIR, '_EditorState.pa.yaml'), 'utf-8');
    const yamlFiles = fs
      .readdirSync(SRC_DIR)
      .filter((f) => f.endsWith('.pa.yaml') && f !== '_EditorState.pa.yaml' && f !== 'App.pa.yaml');

    for (const file of yamlFiles) {
      const screenName = file.replace(/\.pa\.yaml$/, '');
      expect(
        editorState.includes(screenName),
        `Screen ${screenName} exists as a file but is missing from _EditorState.pa.yaml ScreensOrder`,
      ).toBeTruthy();
    }
  });
});

// ============================================================================
// Test Group 2: Power Fx Formula Validation
// ============================================================================

test.describe('Power Fx Formulas', () => {
  const yamlFiles = (): string[] => fs.readdirSync(SRC_DIR).filter((f) => f.endsWith('.pa.yaml'));

  test('should have balanced parentheses and brackets in all screen files', () => {
    for (const file of yamlFiles()) {
      const content = fs.readFileSync(path.join(SRC_DIR, file), 'utf-8');
      const lines = content.split('\n');

      let parenCount = 0;
      let bracketCount = 0;

      for (const line of lines) {
        // Skip comments and quoted strings — parens inside those are prose, not formulas.
        const trimmed = line.trim();
        if (trimmed.startsWith('#') || trimmed.startsWith('//')) continue;
        const inString = (trimmed.match(/"/g) || []).length % 2 === 1;
        if (inString) continue;

        for (const char of line) {
          if (char === '(') parenCount++;
          if (char === ')') parenCount--;
          if (char === '[') bracketCount++;
          if (char === ']') bracketCount--;
        }
      }

      expect(parenCount, `Unbalanced parentheses in ${file}: ${parenCount}`).toBe(0);
      expect(bracketCount, `Unbalanced brackets in ${file}: ${bracketCount}`).toBe(0);
    }
  });

  test('should have valid Navigate targets', () => {
    const screenNames = new Set(
      fs
        .readdirSync(SRC_DIR)
        .filter((f) => f.startsWith('scr_') && f.endsWith('.pa.yaml'))
        .map((f) => f.replace(/\.pa\.yaml$/, '')),
    );
    expect(screenNames.size, 'no screens discovered').toBeGreaterThan(0);

    for (const file of yamlFiles()) {
      const content = fs.readFileSync(path.join(SRC_DIR, file), 'utf-8');
      for (const match of content.matchAll(/Navigate\(\s*(\w+)/g)) {
        const target = match[1];
        if (target.startsWith('scr_')) {
          expect(
            screenNames.has(target),
            `Invalid Navigate target: ${target} in ${file}`,
          ).toBeTruthy();
        }
      }
    }
  });
});

// ============================================================================
// Test Group 3: Flow Package Validation
// ============================================================================

test.describe('Flow Package', () => {
  const zipPath = path.join(FLOWS_DIR, 'APP-MRMS-Approval.zip');
  const ZIP_LOCAL_HEADER = Buffer.from([0x50, 0x4b, 0x03, 0x04]);

  const expectedGuids = [
    '210ef69f-5bb8-4a11-88ff-c2b7606c71a6',
    '35502f2b-26e0-4d6b-8099-d409277f9dfb',
    'c005bc0a-ff88-4a4c-be75-93fcad1e4ef3',
    'd4f9a27c-8851-44ba-9f3c-4989a0e6d467',
  ];

  test('should have a valid zip structure', () => {
    expect(fs.existsSync(zipPath), 'flows/APP-MRMS-Approval.zip is missing').toBeTruthy();

    const stats = fs.statSync(zipPath);
    expect(stats.size, 'flow zip looks empty/corrupt').toBeGreaterThan(1000);
    expect(stats.size, 'flow zip unexpectedly large').toBeLessThan(10_000_000);

    // ZIP local file header magic: "PK\x03\x04"
    const head = fs.readFileSync(zipPath).subarray(0, 4);
    expect(head.equals(ZIP_LOCAL_HEADER), 'flow zip does not start with a ZIP local header').toBeTruthy();
  });

  test('should have all 4 flows in the manifest', () => {
    const manifestPath = path.join(TEMPLATE_DIR, 'Microsoft.Flow', 'flows', 'manifest.json');
    const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf-8'));

    const assetPaths: string[] = manifest.flowAssets.assetPaths;
    expect(assetPaths, 'manifest flow count').toHaveLength(4);
    for (const guid of expectedGuids) {
      expect(assetPaths, `manifest missing flow ${guid}`).toContain(guid);
    }
  });

  test('should contain every manifest flow as a folder in the zip', () => {
    // Regression guard for KNOWN_ISSUES C4: the checked-in zip once shipped a
    // 4-flow manifest with only 3 flow folders — Power Automate rejects the import.
    const head = fs.readFileSync(zipPath).subarray(0, 4);
    expect(head.equals(ZIP_LOCAL_HEADER), 'not a zip file').toBeTruthy();

    for (const guid of expectedGuids) {
      const defPath = path.join(TEMPLATE_DIR, 'Microsoft.Flow', 'flows', guid, 'definition.json');
      expect(
        fs.existsSync(defPath),
        `template folder missing for flow ${guid} — manifest references a flow that is not packed`,
      ).toBeTruthy();
    }
  });

  test('should have valid JSON in all template flow definitions', () => {
    const flowsDir = path.join(TEMPLATE_DIR, 'Microsoft.Flow', 'flows');
    const flowDirs = fs
      .readdirSync(flowsDir)
      .filter((d) => fs.statSync(path.join(flowsDir, d)).isDirectory());

    expect(flowDirs.length).toBe(4);
    for (const flowDir of flowDirs) {
      const defPath = path.join(flowsDir, flowDir, 'definition.json');
      expect(
        () => JSON.parse(fs.readFileSync(defPath, 'utf-8')),
        `Invalid JSON in ${flowDir}/definition.json`,
      ).not.toThrow();
    }
  });

  test('should have unique action names within each flow', () => {
    const flowsDir = path.join(TEMPLATE_DIR, 'Microsoft.Flow', 'flows');
    const flowDirs = fs
      .readdirSync(flowsDir)
      .filter((d) => fs.statSync(path.join(flowsDir, d)).isDirectory());

    for (const flowDir of flowDirs) {
      const data = JSON.parse(fs.readFileSync(path.join(flowsDir, flowDir, 'definition.json'), 'utf-8'));
      const actions = data.properties?.definition?.actions || {};

      const collectNames = (obj: Record<string, any>, prefix = ''): string[] => {
        const names: string[] = [];
        for (const key of Object.keys(obj)) {
          names.push(prefix + key);
          if (obj[key].actions) {
            names.push(...collectNames(obj[key].actions, prefix + key + '/'));
          }
          if (obj[key].else?.actions) {
            names.push(...collectNames(obj[key].else.actions, prefix + key + '/else/'));
          }
          if (obj[key].cases) {
            for (const c of Object.values<any>(obj[key].cases)) {
              if (c.actions) names.push(...collectNames(c.actions, prefix + key + '/case/'));
            }
          }
        }
        return names;
      };

      const allNames = collectNames(actions);
      expect(new Set(allNames).size, `Duplicate actions in ${flowDir}`).toBe(allNames.length);
    }
  });

  test('should not write review status to MonthlyReports (loop prevention)', () => {
    // Flows may only write review statuses to *other* lists (e.g. marking the
    // related Activity Completed). Writing Status/SubmissionStatus/ReportStatus
    // back to MonthlyReports would re-trigger the flow and loop. The templates
    // address lists by token, so a MonthlyReports update is `table: {{MR_GUID}}`.
    const flowsDir = path.join(TEMPLATE_DIR, 'Microsoft.Flow', 'flows');
    const flowDirs = fs
      .readdirSync(flowsDir)
      .filter((d) => fs.statSync(path.join(flowsDir, d)).isDirectory());

    const REVIEW_STATUS_KEYS = ['item/Status', 'item/SubmissionStatus', 'item/ReportStatus'];

    for (const flowDir of flowDirs) {
      const data = JSON.parse(fs.readFileSync(path.join(flowsDir, flowDir, 'definition.json'), 'utf-8'));
      const actions = data.properties?.definition || {};

      const writesMonthlyReportsStatus = (nodes: any): boolean => {
        for (const action of Object.values<any>(nodes)) {
          const params = action?.inputs?.parameters || {};
          const isMonthlyReports =
            typeof params.table === 'string' &&
            /\{\{MR_GUID\}\}|31b39eaa-cf11-426d-b9a1-c3df5bae7cbe/.test(params.table);
          if (isMonthlyReports && REVIEW_STATUS_KEYS.some((k) => typeof params[k] === 'string')) {
            return true;
          }
          if (action.actions && writesMonthlyReportsStatus(action.actions)) return true;
          if (action.else?.actions && writesMonthlyReportsStatus(action.else.actions)) return true;
          if (action.cases) {
            for (const c of Object.values<any>(action.cases)) {
              if (c.actions && writesMonthlyReportsStatus(c.actions)) return true;
            }
          }
        }
        return false;
      };

      expect(
        writesMonthlyReportsStatus(actions.actions || {}),
        `Flow ${flowDir} writes a review status back to MonthlyReports!`,
      ).toBeFalsy();
    }
  });
});

// ============================================================================
// Test Group 4: CSV Schema Validation
// ============================================================================

test.describe('CSV Schemas', () => {
  test('should have all required CSV files in the repo root', () => {
    const requiredCSVs = [
      'Directorates.csv',
      'Programmes.csv',
      'Projects.csv',
      'Activities.csv',
      'MonthlyReports.csv',
      'APP_Users.csv',
      'KPIDefinitions.csv',
      'Notifications.csv',
      'AuditLog.csv',
      'ReportComments.csv',
    ];

    for (const csv of requiredCSVs) {
      expect(fs.existsSync(path.join(ROOT_DIR, csv)), `Missing CSV: ${csv}`).toBeTruthy();
    }
  });

  test('should have valid multi-line CSV structure', () => {
    const csvFiles = fs.readdirSync(ROOT_DIR).filter((f) => f.endsWith('.csv'));
    expect(csvFiles.length).toBeGreaterThan(5);

    for (const csv of csvFiles) {
      const content = fs.readFileSync(path.join(ROOT_DIR, csv), 'utf-8');
      // These CSVs embed a SharePoint ListSchema header line before the data rows.
      const lines = content.split('\n').filter((l) => l.trim().length > 0);
      expect(lines.length, `${csv} has no data rows`).toBeGreaterThan(1);
      expect(lines[0].length, `${csv} header line looks empty`).toBeGreaterThan(10);
    }
  });

  test('should have correct February spelling in MonthlyReports', () => {
    // KNOWN_ISSUES L7 — regression guard: a data-row typo and a schema-header typo
    // ("Fecbruary") both shipped at one point.
    const content = fs.readFileSync(path.join(ROOT_DIR, 'MonthlyReports.csv'), 'utf-8');
    expect(content).not.toContain('Fecbruary');
    expect(content).toContain('February');
  });
});

// ============================================================================
// Test Group 5: Documentation Completeness
// ============================================================================

test.describe('Documentation', () => {
  test('should have all required documentation files', () => {
    const requiredDocs = ['AUDIT_FINDINGS.md', 'KNOWN_ISSUES.md', 'ARCHITECTURE.md', 'README.md'];

    for (const doc of requiredDocs) {
      expect(fs.existsSync(path.join(ROOT_DIR, doc)), `Missing doc: ${doc}`).toBeTruthy();
    }
  });

  test('should have Power Automate reference docs', () => {
    const refPath = path.join(ROOT_DIR, 'docs', 'power-automate', 'README.md');
    expect(fs.existsSync(refPath), 'docs/power-automate/README.md missing').toBeTruthy();

    const content = fs.readFileSync(refPath, 'utf-8');
    expect(content.length).toBeGreaterThan(1000);
  });

  test('should have flow README with import instructions', () => {
    const readmePath = path.join(FLOWS_DIR, 'README.md');
    expect(fs.existsSync(readmePath)).toBeTruthy();

    const content = fs.readFileSync(readmePath, 'utf-8');
    expect(content).toContain('Import');
    expect(content).toContain('GUID');
  });
});

// ============================================================================
// Test Group 6: msapp Package Validation
// ============================================================================

test.describe('msapp Packages', () => {
  // .msapp packs produced by pac / repack_msapp.py are ZIP containers: they start
  // with the local-file-header magic "PK\x03\x04" and end with the central-directory
  // record "PK\x05\x06" (optionally followed by a comment).
  const ZIP_LOCAL_HEADER = Buffer.from([0x50, 0x4b, 0x03, 0x04]);
  const ZIP_EOCD = Buffer.from([0x50, 0x4b, 0x05, 0x06]);

  const msappFiles = (): string[] =>
    fs
      .readdirSync(ROOT_DIR)
      .filter((f) => f.endsWith('.msapp'))
      .sort();

  test('should have at least one importable msapp package', () => {
    const files = msappFiles();
    expect(files.length, 'no .msapp packages found in repo root').toBeGreaterThan(0);
  });

  test('every msapp package should be a valid ZIP container of plausible size', () => {
    for (const file of msappFiles()) {
      const p = path.join(ROOT_DIR, file);
      const stats = fs.statSync(p);
      expect(stats.size, `${file} is too small to be a real pack`).toBeGreaterThan(10_000);

      const buf = fs.readFileSync(p);
      expect(
        buf.subarray(0, 4).equals(ZIP_LOCAL_HEADER),
        `${file} does not start with a ZIP local header (corrupt pack?)`,
      ).toBeTruthy();

      // End Of Central Directory lives in the last 64KB (max comment size + fixed part).
      const tailStart = Math.max(0, buf.length - 65_600);
      const tail = buf.subarray(tailStart);
      const eocdIdx = tail.lastIndexOf(ZIP_EOCD);
      expect(
        eocdIdx,
        `${file} has no ZIP End Of Central Directory record (truncated pack?)`,
      ).toBeGreaterThanOrEqual(0);
    }
  });
});

// ============================================================================
// Test Group 7: Tools Validation
// ============================================================================

test.describe('Tools', () => {
  test('should have all required verification tools', () => {
    const requiredTools = [
      'provision_sharepoint.py',
      'build_flow_zips.py',
      'verify_powerfx.py',
      'check_screen_registry.py',
      'check_control_props.py',
    ];

    for (const tool of requiredTools) {
      expect(fs.existsSync(path.join(ROOT_DIR, 'tools', tool)), `Missing tool: ${tool}`).toBeTruthy();
    }
  });

  test('every Python tool should compile', () => {
    const toolsDir = path.join(ROOT_DIR, 'tools');
    const pyFiles = fs.readdirSync(toolsDir).filter((f) => f.endsWith('.py'));

    for (const py of pyFiles) {
      const result = execFileSync('python3', ['-m', 'py_compile', path.join(toolsDir, py)], {
        stdio: 'pipe',
        encoding: 'utf-8',
      });
      expect(result, `${py} failed to compile`).toBeDefined();
    }
  });

  test('the repo CI checks should pass end-to-end (registry, props, powerfx strict)', () => {
    // Runs the same three gates CI runs, so a local failure here means CI will fail too.
    for (const check of [
      'tools/check_screen_registry.py',
      'tools/check_control_props.py',
      'tools/verify_powerfx.py --strict',
    ]) {
      const [script, ...args] = check.split(' ');
      const result = execFileSync('python3', [script, ...args], {
        cwd: ROOT_DIR,
        stdio: 'pipe',
        encoding: 'utf-8',
      });
      expect(result, `${check} exited non-zero`).toBeDefined();
    }
  });
});
