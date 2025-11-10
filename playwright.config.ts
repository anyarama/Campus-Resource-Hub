import { defineConfig, devices } from '@playwright/test'

const port = Number(process.env.FLASK_RUN_PORT || 5001)

export default defineConfig({
  testDir: './tests',
  testMatch: ['playwright/**/*.spec.ts', 'ui/**/*.spec.ts'],
  timeout: 30 * 1000,
  expect: {
    timeout: 5000,
  },
  retries: process.env.CI ? 2 : 0,
  fullyParallel: true,
  reporter: [['list'], ['html', { open: 'never' }]],
  use: {
    baseURL: process.env.PLAYWRIGHT_BASE_URL || `http://127.0.0.1:${port}`,
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
    video: process.env.CI ? 'retain-on-failure' : 'off',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  webServer: {
    command: 'bash scripts/run_e2e_server.sh',
    url: `http://127.0.0.1:${port}`,
    timeout: 120 * 1000,
    reuseExistingServer: false,
  },
})
