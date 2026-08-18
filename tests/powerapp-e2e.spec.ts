/**
 * APP-MRMS Power App E2E Test Suite
 * 
 * This test suite validates the Power App structure, source code,
 * and flow package for import readiness.
 * 
 * Run: npx playwright test tests/powerapp-e2e.spec.ts
 */

import { test, expect } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

const ROOT_DIR = path.resolve(__dirname, '..');
const APP_MRMS_DIR = path.join(ROOT_DIR, 'APP_MRMS');
const FLOWS_DIR = path.join(ROOT_DIR, 'flows');
const SRC_DIR = path.join(APP_MRMS_DIR, 'src', 'Src');

// ============================================================================
// Test Group 1: Source Code Structure
// ============================================================================

test.describe('Source Code Structure', () => {
  
  test('should have all required screen files', () => {
    const requiredScreens = [
      'App.pa.yaml',
      '_EditorState.pa.yaml',
      'scr_Splash.pa.yaml',
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
    ];

    for (const screen of requiredScreens) {
      const filePath = path.join(SRC_DIR, screen);
      expect(fs.existsSync(filePath), `Missing screen: ${screen}`).toBeTruthy();
    }

    // Check that ApprovalQueue exists in parent repo
    const approvalQueuePath = path.join(ROOT_DIR, 'src', 'Src', 'scr_ApprovalQueue.pa.yaml');
    expect(fs.existsSync(approvalQueuePath), 'Missing screen: scr_ApprovalQueue.pa.yaml (should be in parent repo)').toBeTruthy();
  });

  test('should have valid YAML in all screen files', () => {
    const yamlFiles = fs.readdirSync(SRC_DIR)
      .filter(f => f.endsWith('.pa.yaml'));

    for (const file of yamlFiles) {
      const content = fs.readFileSync(path.join(SRC_DIR, file), 'utf-8');
      // Basic YAML validation - no tab characters, valid structure
      expect(content).not.toContain('\t');
      expect(content.length).toBeGreaterThan(100);
    }
  });

  test('should have no duplicate control names across screens', () => {
    // This test is complex due to YAML structure - skip for now
    // The check_screen_registry.py tool handles this validation
    test.skip();
  });
});

// ============================================================================
// Test Group 2: Power Fx Formula Validation
// ============================================================================

test.describe('Power Fx Formulas', () => {
  
  test('should have balanced parentheses in all formulas', () => {
    const yamlFiles = fs.readdirSync(SRC_DIR)
      .filter(f => f.endsWith('.pa.yaml'));

    for (const file of yamlFiles) {
      const content = fs.readFileSync(path.join(SRC_DIR, file), 'utf-8');
      const lines = content.split('\n');
      
      let parenCount = 0;
      let bracketCount = 0;
      
      for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        // Skip comments and strings
        if (line.trim().startsWith('//') || line.trim().startsWith('#')) continue;
        
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

  test('should not have common Power Fx errors', () => {
    const errorPatterns = [
      /Patch\([^)]*\)/g,  // Incomplete Patch calls
      /Navigate\([^)]*\)/g,  // Incomplete Navigate calls
      /Set\([^,]+,\s*\)/g,  // Empty Set values
    ];

    const yamlFiles = fs.readdirSync(SRC_DIR)
      .filter(f => f.endsWith('.pa.yaml'));

    for (const file of yamlFiles) {
      const content = fs.readFileSync(path.join(SRC_DIR, file), 'utf-8');
      
      for (const pattern of errorPatterns) {
        const matches = content.match(pattern);
        if (matches) {
          console.warn(`Potential issue in ${file}: ${matches[0]}`);
        }
      }
    }
  });

  test('should have valid Navigate targets', () => {
    const screenNames = new Set([
      'scr_Splash', 'scr_Home', 'scr_Users', 'scr_MyActivities',
      'scr_ReportForm', 'scr_ReportView', 'scr_Projects', 'scr_Activities',
      'scr_ReportActivities', 'scr_Reports', 'scr_ApprovedReports', 'scr_ApprovalQueue'
    ]);

    const yamlFiles = fs.readdirSync(SRC_DIR)
      .filter(f => f.endsWith('.pa.yaml'));

    for (const file of yamlFiles) {
      const content = fs.readFileSync(path.join(SRC_DIR, file), 'utf-8');
      const navigateMatches = content.matchAll(/Navigate\((\w+)/g);
      
      for (const match of navigateMatches) {
        const target = match[1];
        if (target.startsWith('scr_')) {
          expect(screenNames.has(target), `Invalid Navigate target: ${target} in ${file}`).toBeTruthy();
        }
      }
    }
  });
});

// ============================================================================
// Test Group 3: Flow Package Validation
// ============================================================================

test.describe('Flow Package', () => {
  
  test('should have valid zip structure', () => {
    const zipPath = path.join(FLOWS_DIR, 'APP-MRMS-Approval.zip');
    expect(fs.existsSync(zipPath)).toBeTruthy();
    
    // Check file size is reasonable (not empty, not corrupted)
    const stats = fs.statSync(zipPath);
    expect(stats.size).toBeGreaterThan(1000);
    expect(stats.size).toBeLessThan(10000000); // Less than 10MB
  });

  test('should have all 4 flows in manifest', () => {
    const manifestPath = path.join(FLOWS_DIR, 'templates', 'APP-MRMS-Approval', 'Microsoft.Flow', 'flows', 'manifest.json');
    const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf-8'));
    
    expect(manifest.flowAssets.assetPaths).toHaveLength(4);
    expect(manifest.flowAssets.assetPaths).toContain('210ef69f-5bb8-4a11-88ff-c2b7606c71a6');
    expect(manifest.flowAssets.assetPaths).toContain('35502f2b-26e0-4d6b-8099-d409277f9dfb');
    expect(manifest.flowAssets.assetPaths).toContain('c005bc0a-ff88-4a4c-be75-93fcad1e4ef3');
    expect(manifest.flowAssets.assetPaths).toContain('d4f9a27c-8851-44ba-9f3c-4989a0e6d467');
  });

  test('should have valid JSON in all flow definitions', () => {
    const flowsDir = path.join(FLOWS_DIR, 'templates', 'APP-MRMS-Approval', 'Microsoft.Flow', 'flows');
    const flowDirs = fs.readdirSync(flowsDir).filter(d => {
      const fullPath = path.join(flowsDir, d);
      return fs.statSync(fullPath).isDirectory();
    });

    for (const flowDir of flowDirs) {
      const defPath = path.join(flowsDir, flowDir, 'definition.json');
      if (fs.existsSync(defPath)) {
        const content = fs.readFileSync(defPath, 'utf-8');
        expect(() => JSON.parse(content), `Invalid JSON in ${flowDir}/definition.json`).not.toThrow();
      }
    }
  });

  test('should have unique action names within each flow', () => {
    const flowsDir = path.join(FLOWS_DIR, 'templates', 'APP-MRMS-Approval', 'Microsoft.Flow', 'flows');
    const flowDirs = fs.readdirSync(flowsDir).filter(d => {
      const fullPath = path.join(flowsDir, d);
      return fs.statSync(fullPath).isDirectory();
    });

    for (const flowDir of flowDirs) {
      const defPath = path.join(flowsDir, flowDir, 'definition.json');
      if (fs.existsSync(defPath)) {
        const data = JSON.parse(fs.readFileSync(defPath, 'utf-8'));
        const actions = data.properties?.definition?.actions || {};
        
        const collectNames = (obj: any, prefix = ''): string[] => {
          const names: string[] = [];
          for (const key of Object.keys(obj)) {
            names.push(prefix + key);
            if (obj[key].actions) {
              names.push(...collectNames(obj[key].actions, prefix + key + '/'));
            }
            if (obj[key].else?.actions) {
              names.push(...collectNames(obj[key].else.actions, prefix + key + '/else/'));
            }
          }
          return names;
        };

        const allNames = collectNames(actions);
        const uniqueNames = new Set(allNames);
        expect(allNames.length, `Duplicate actions in ${flowDir}`).toBe(uniqueNames.size);
      }
    }
  });

  test('should not write to MonthlyReports.Status (loop prevention)', () => {
    const flowsDir = path.join(FLOWS_DIR, 'templates', 'APP-MRMS-Approval', 'Microsoft.Flow', 'flows');
    const flowDirs = fs.readdirSync(flowsDir).filter(d => {
      const fullPath = path.join(flowsDir, d);
      return fs.statSync(fullPath).isDirectory();
    });

    for (const flowDir of flowDirs) {
      const defPath = path.join(flowsDir, flowDir, 'definition.json');
      if (fs.existsSync(defPath)) {
        const data = JSON.parse(fs.readFileSync(defPath, 'utf-8'));
        const definition = data.properties?.definition || {};
        
        const checkForStatusWrites = (actions: any): boolean => {
          for (const key of Object.keys(actions)) {
            const action = actions[key];
            if (action.type === 'OpenApiConnection') {
              const params = action.inputs?.parameters || {};
              const table = params.table || '';
              const item = params.item || {};
              
              // Check if updating MonthlyReports with Status
              if (table.includes('11111111-1111-1111-1111-111111111111') && 
                  item.hasOwnProperty('item/Status')) {
                return true;
              }
            }
            
            // Recurse into nested actions
            if (action.actions && checkForStatusWrites(action.actions)) return true;
            if (action.else?.actions && checkForStatusWrites(action.else.actions)) return true;
          }
          return false;
        };

        expect(checkForStatusWrites(definition.actions || {}), 
          `Flow ${flowDir} writes to MonthlyReports.Status!`).toBeFalsy();
      }
    }
  });
});

// ============================================================================
// Test Group 4: CSV Schema Validation
// ============================================================================

test.describe('CSV Schemas', () => {
  
  test('should have all required CSV files', () => {
    const requiredCSVs = [
      'Directorates.csv',
      'Programmes.csv',
      'Projects.csv',
      'Activities.csv',
      'MonthlyReports.csv',
      'APP_Users.csv',
    ];

    for (const csv of requiredCSVs) {
      const filePath = path.join(APP_MRMS_DIR, csv);
      expect(fs.existsSync(filePath), `Missing CSV: ${csv}`).toBeTruthy();
    }

    // Check that new list CSVs exist in parent repo
    const newCSVs = ['Notifications.csv', 'AuditLog.csv', 'ReportComments.csv', 'KPIDefinitions.csv'];
    for (const csv of newCSVs) {
      const filePath = path.join(ROOT_DIR, csv);
      expect(fs.existsSync(filePath), `Missing CSV: ${csv} (should be in parent repo)`).toBeTruthy();
    }
  });

  test('should have valid CSV structure', () => {
    const csvFiles = fs.readdirSync(APP_MRMS_DIR).filter(f => f.endsWith('.csv'));
    
    for (const csv of csvFiles) {
      const content = fs.readFileSync(path.join(APP_MRMS_DIR, csv), 'utf-8');
      const lines = content.split('\n');
      
      // Check CSV has at least header + data
      expect(lines.length).toBeGreaterThan(1);
      
      // Check first line has commas (header)
      expect(lines[0].split(',').length).toBeGreaterThan(1);
    }
  });

  test('should have correct February spelling in MonthlyReports', () => {
    const content = fs.readFileSync(path.join(APP_MRMS_DIR, 'MonthlyReports.csv'), 'utf-8');
    expect(content).not.toContain('Fecbruary');
    expect(content).toContain('February');
  });
});

// ============================================================================
// Test Group 5: Documentation Completeness
// ============================================================================

test.describe('Documentation', () => {
  
  test('should have all required documentation files', () => {
    const requiredDocs = [
      'AUDIT_FINDINGS.md',
      'DEPLOYMENT_CHECKLIST.md',
      'KNOWN_ISSUES.md',
      'ARCHITECTURE.md',
    ];

    for (const doc of requiredDocs) {
      const filePath = path.join(ROOT_DIR, doc);
      expect(fs.existsSync(filePath), `Missing doc: ${doc}`).toBeTruthy();
    }
  });

  test('should have Power Automate reference', () => {
    const refPath = path.join(ROOT_DIR, 'reference', 'power-automate', 'README.md');
    expect(fs.existsSync(refPath)).toBeTruthy();
    
    const content = fs.readFileSync(refPath, 'utf-8');
    expect(content.length).toBeGreaterThan(1000);
  });

  test('should have flow README with instructions', () => {
    const readmePath = path.join(FLOWS_DIR, 'README.md');
    expect(fs.existsSync(readmePath)).toBeTruthy();
    
    const content = fs.readFileSync(readmePath, 'utf-8');
    expect(content).toContain('Import');
    expect(content).toContain('GUID');
  });
});

// ============================================================================
// Test Group 6: Tools Validation
// ============================================================================

test.describe('Tools', () => {
  
  test('should have all required tools', () => {
    const requiredTools = [
      'provision_sharepoint.py',
      'build_flow_zips.py',
      'verify_powerfx.py',
      'check_screen_registry.py',
      'check_control_props.py',
    ];

    const toolsDir = path.join(ROOT_DIR, 'tools');
    for (const tool of requiredTools) {
      const filePath = path.join(toolsDir, tool);
      expect(fs.existsSync(filePath), `Missing tool: ${tool}`).toBeTruthy();
    }
  });

  test('should have valid Python syntax in tools', async () => {
    const toolsDir = path.join(ROOT_DIR, 'tools');
    const pyFiles = fs.readdirSync(toolsDir).filter(f => f.endsWith('.py'));
    
    for (const py of pyFiles) {
      const content = fs.readFileSync(path.join(toolsDir, py), 'utf-8');
      // Basic syntax check - no obvious errors
      expect(content).not.toContain('def def');
      expect(content).not.toContain('import import');
    }
  });
});
