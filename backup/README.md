# Backups — pristine snapshots before modifications

These are immutable copies of the app **before any screen changes are made**.
If a pack/edit breaks the app, restore from here.

| Path | Contents |
|---|---|
| `original-pack/APP-MRMS_Project_app.msapp` | The original Power Apps package exactly as provided (SHA-256 `4d0d5b00…` — verify with `sha256sum`). |
| `unpacked/` | The unpacked `SourceCode` layout as produced by `pac canvas unpack` (`.msapr` resources archive + `Src/*.pa.yaml`), untouched. |

## How to restore

```bash
# Restore the original importable package
cp backup/original-pack/APP-MRMS_Project_app.msapp APP-MRMS_Project_app.msapp

# Restore the pristine unpacked source (then repack if needed)
rm -rf src && cp -r backup/unpacked src
```

## Integrity checks

- `backup/original-pack/APP-MRMS_Project_app.msapp` is byte-identical to the
  top-level `APP-MRMS_Project_app.msapp` (same file, copied before changes).
- `backup/unpacked/` is byte-identical to the original `APP_MRMS_Unpacked/`
  output of `pac canvas unpack` (SourceCode layout).
- Round-trip was verified before this backup: pack → unpack produces
  byte-identical Src YAML and internal JSON (see CHANGES.md §6).
