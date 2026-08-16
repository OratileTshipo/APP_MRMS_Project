# Activities.csv data-normalization report

Date: 2026-08-16. Generated from the git diff (HEAD vs working tree).

## Decisions (product)
- RISK and IC are kept as **separate** directorates (cleaned names below).
- **RIC (Risk and Internal Control) is retired**: Directorates.csv Active=False;
  the only APP_Users row on RIC (Oratile Tshipo) was reassigned to **Internal Control** (IC).
- DirectorateLabel is rewritten from the authoritative `Directorate` short-code column
  (blank-code rows resolved from ActivityCode prefix / label). ProgrammeLabel is mapped
  to the canonical Programmes.csv titles.
- Only the two label columns changed in Activities.csv; all other bytes preserved.

## DirectorateLabel changes (Activities.csv)

| Old value | New value | Rows |
|---|---|---|
| `` | `Internal Control` | 1 |
| `` | `Legal Services` | 1 |
| `` | `Strategic Planning Monitoring and Evaluations` | 1 |
| `1. Prepare and issue Risk Management Committee packs 2.Convine the Quarter 2 Risk Management Committee meeting and record resolutions` | `Risk Management` | 1 |
| `Cummunication` | `Communications` | 1 |
| `FINANCE` | `Finance` | 58 |
| `HUMAN RESOURCE DEVELOPMENT` | `Human Resource Development` | 3 |
| `HUman Resource Management` | `Human Resources Management` | 2 |
| `Human Resouorce Management` | `Human Resources Management` | 1 |
| `Human Resource  Development` | `Human Resource Development` | 1 |
| `Human Resource Management` | `Human Resources Management` | 66 |
| `Human Resource Managemnt` | `Human Resources Management` | 1 |
| `Human Resource Mnagement` | `Human Resources Management` | 1 |
| `Human Rsource Management` | `Human Resources Management` | 1 |
| `IFINANCE` | `Finance` | 1 |
| `Iinternal Control` | `Internal Control` | 1 |
| `LEGAL SERVICES` | `Legal Services` | 3 |
| `Legal SErvices` | `Legal Services` | 1 |
| `Legal Service` | `Legal Services` | 1 |
| `Legal services` | `Legal Services` | 1 |
| `Mid-year financial control assessment` | `Internal Control` | 1 |
| `Monitor expenditure trends` | `Internal Control` | 1 |
| `Programme 1` | `Finance` | 1 |
| `SPECIAL PEOGRAMMES` | `Special Programmes` | 1 |
| `SPECIAL PROGEMMES` | `Special Programmes` | 1 |
| `SPECIAL PROGRAMME` | `Special Programmes` | 1 |
| `SPECIAL PROGRAMMES` | `Special Programmes` | 17 |
| `Strategic PLanning, Monitoring and Evaluation` | `Strategic Planning Monitoring and Evaluations` | 1 |
| `Strategic PLanning,Monitoring and Evaluation` | `Strategic Planning Monitoring and Evaluations` | 1 |
| `Strategic Planning Monitoring & Evaluation` | `Strategic Planning Monitoring and Evaluations` | 3 |
| `Strategic Planning, Monitoring And Evaluation` | `Strategic Planning Monitoring and Evaluations` | 1 |
| `Strategic Planning, Monitoring and Evaluation` | `Strategic Planning Monitoring and Evaluations` | 11 |
| `Strategic Planning,MOnitoring and Evaluation` | `Strategic Planning Monitoring and Evaluations` | 2 |
| `Strategic Planning,Monitoring Evaluation` | `Strategic Planning Monitoring and Evaluations` | 1 |
| `Strategic Planning,Monitoring and Evaluation` | `Strategic Planning Monitoring and Evaluations` | 39 |
| `Strategic Planning,monitoring and Evaluation` | `Strategic Planning Monitoring and Evaluations` | 1 |
| `Stretegic Planning, Monitoring and Evaluation` | `Strategic Planning Monitoring and Evaluations` | 1 |
| `Suplly Chain Management` | `Supply Chain Management` | 1 |
| `Supplt Chain Programme` | `Supply Chain Management` | 1 |
| `Supply  Chain Management` | `Supply Chain Management` | 2 |
| `Supply Chain Managament` | `Supply Chain Management` | 1 |
| `Supply Chain Managemant` | `Supply Chain Management` | 4 |
| `Track implementation of Quarter 4 Risk Management Committee resolutions and obtain progress evidence from responsible officials.` | `Risk Management` | 1 |
| `strategic Planning,Monitoring and Evaluation` | `Strategic Planning Monitoring and Evaluations` | 1 |

## ProgrammeLabel changes (Activities.csv)

| Old value | New value | Rows |
|---|---|---|
| `` | `Programme 1` | 1 |
| `FINANCE` | `Programme 1` | 1 |
| `PRogramme 1` | `Programme 1` | 1 |
| `Pragramme 1` | `Programme 1` | 1 |
| `Programme` | `Programme 1` | 14 |
| `Programmes 1` | `Programme 1` | 3 |
| `programme 1` | `Programme 1` | 1 |

## Directorates.csv changes

| ID | Old | New |
|---|---|---|
| RIC | `Active=True` | `Active=False` |
| RISK | `RISK MANAGEMENT` | `Risk Management` |
| IC | `INTERNAL CONTROL` | `Internal Control` |

## APP_Users.csv changes

| User | Old | New |
|---|---|---|
| Oratile Tshipo | `Risk and Internal Control` | `Internal Control` |
| Oratile Tshipo ID | `RIC` | `IC` |
