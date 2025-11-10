import { test, expect } from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'

async function runAxe(page: any) {
  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa'])
    .analyze()
  const serious = results.violations.filter(
    (violation) => violation.impact === 'serious' || violation.impact === 'critical'
  )
  expect(serious).toEqual([])
}

test('login page passes axe scan', async ({ page }) => {
  await page.goto('/auth/login')
  await runAxe(page)
})

const authedPages = ['/dashboard', '/resources', '/resources/1']
const adminPages = ['/admin/dashboard', '/admin/users']
const adminCreds = { email: 'admin@example.com', password: 'Demo123!' }

test.describe('Authenticated accessibility', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/auth/login')
    await page.fill('input[name="email"]', 'student@example.com')
    await page.fill('input[name="password"]', 'Demo123!')
    await page.click('button:has-text("Login")')
    await page.waitForURL(/dashboard/)
  })

  for (const path of authedPages) {
    test(`axe scan for ${path}`, async ({ page }) => {
      await page.goto(path)
      await runAxe(page)
    })
  }
})

test.describe('Admin accessibility', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/auth/login')
    await page.fill('input[name="email"]', adminCreds.email)
    await page.fill('input[name="password"]', adminCreds.password)
    await page.click('button:has-text("Login")')
    await page.waitForURL(/dashboard/)
  })

  for (const path of adminPages) {
    test(`axe scan for ${path}`, async ({ page }) => {
      await page.goto(path)
      await runAxe(page)
    })
  }
})
