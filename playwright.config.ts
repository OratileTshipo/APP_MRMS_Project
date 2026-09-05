import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  // Tests spawn Python subprocesses (py_compile + the CI check scripts), so keep
  // parallelism modest to avoid memory pressure on constrained machines.
  workers: process.env.CI ? 1 : 4,
  reporter: [
    ['html', { outputFolder: 'test-results/html-report' }],
    ['json', { outputFile: 'test-results/test-results.json' }],
    ['list'],
  ],
  use: {
    baseURL: 'file://' + process.cwd(),
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'powerapp-validation',
      testMatch: '**/*.spec.ts',
    },
  ],
  outputDir: 'test-results',
});
