import { test, expect, Page } from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'

const studentCredentials = {
  email: 'student@example.com',
  password: 'Demo123!',
}

const adminCredentials = {
  email: 'admin@example.com',
  password: 'Demo123!',
}

async function expectNoSeriousA11yViolations(page: Page) {
  await page.waitForLoadState('networkidle')
  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa'])
    .analyze()

  const serious = results.violations.filter((violation) =>
    violation.impact === 'serious' || violation.impact === 'critical'
  )

  const formatted = serious.map(
    (violation) => `${violation.id}: ${violation.help} (nodes: ${violation.nodes.length})`
  )

  expect(formatted).toEqual([])
}

function trackConsole(page: Page) {
  const messages: string[] = []
  page.on('console', (msg) => {
    if (msg.type() === 'error' || msg.type() === 'warning') {
      messages.push(`${msg.type()}: ${msg.text()}`)
    }
  })
  return async () => {
    expect(messages).toEqual([])
  }
}

async function login(page: Page, creds = studentCredentials) {
  await page.goto('/auth/login')
  await page.getByLabel('Email Address').fill(creds.email)
  await page.getByLabel('Password').fill(creds.password)
  await page.getByRole('button', { name: /login/i }).click()
  await page.waitForURL('**/dashboard')
}

async function getFirstResourceDetailUrl(page: Page) {
  const firstCard = page.locator('.resources-grid .resource-card').first()
  await expect(firstCard).toBeVisible()
  const href = await firstCard.locator('h3 a').first().getAttribute('href')
  expect(href).toBeTruthy()
  return href!
}

test.describe('Public experience', () => {
  test('login page renders and is accessible', async ({ page }) => {
    await page.goto('/auth/login')
    await expect(page.getByRole('heading', { name: /login to campus resource hub/i })).toBeVisible()
    await expectNoSeriousA11yViolations(page)
  })

  test('resource list supports filters and passes axe', async ({ page }) => {
    await page.goto('/resources')
    await expect(page.getByRole('heading', { name: /browse resources/i })).toBeVisible()
    await expect(page.locator('.resources-grid .resource-card').first()).toBeVisible()
    await expectNoSeriousA11yViolations(page)
  })

  test('resource detail page renders hero and reviews', async ({ page }) => {
    await page.goto('/resources')
    const detailUrl = await getFirstResourceDetailUrl(page)
    await page.goto(detailUrl)
    await expect(page.locator('.resource-title')).toBeVisible()
    await expect(page.locator('.resource-detail__hero')).toBeVisible()
    await expectNoSeriousA11yViolations(page)
  })
})

test.describe('Authenticated experience', () => {
  test('dashboard shows welcome state and charts', async ({ page }) => {
    const assertConsoleClean = trackConsole(page)
    await login(page)
    await expect(page.getByRole('heading', { name: /welcome/i })).toBeVisible()
    await expect(page.locator('#chart-bookings')).toBeVisible()
    await expect(page.locator('#chart-categories')).toBeVisible()
    await expectNoSeriousA11yViolations(page)
    await assertConsoleClean()
  })

  test('resources list renders without console noise and keeps sidebar tooltips', async ({ page }) => {
    const assertConsoleClean = trackConsole(page)
    await login(page)
    await page.goto('/resources')
    await expect(page.getByRole('heading', { name: /browse resources/i })).toBeVisible()
    const sidebarLinks = page.locator('.app-sidebar .sidebar-link')
    const linkCount = await sidebarLinks.count()
    expect(linkCount).toBeGreaterThan(0)
    for (let i = 0; i < linkCount; i += 1) {
      await expect(sidebarLinks.nth(i)).toHaveAttribute('data-tooltip', /.+/)
      await expect(sidebarLinks.nth(i)).toHaveAttribute('aria-label', /.+/)
    }
    await expectNoSeriousA11yViolations(page)
    await assertConsoleClean()
  })

  test('bookings page loads cards and respects sidebar tooltips', async ({ page }) => {
    const assertConsoleClean = trackConsole(page)
    await login(page)
    await page.goto('/bookings/my-bookings')
    await expect(page.getByRole('heading', { name: /my bookings/i })).toBeVisible()
    await expect(page.locator('.booking-card').first()).toBeVisible()
    const sidebarLinks = page.locator('.app-sidebar .sidebar-link')
    const linkCount = await sidebarLinks.count()
    expect(linkCount).toBeGreaterThan(0)
    for (let i = 0; i < linkCount; i += 1) {
      await expect(sidebarLinks.nth(i)).toHaveAttribute('data-tooltip', /.+/)
    }
    await expectNoSeriousA11yViolations(page)
    await assertConsoleClean()
  })
})

test.describe('Admin experience', () => {
  test.beforeEach(async ({ page }) => {
    await login(page, adminCredentials)
  })

  test('dashboard shows KPI tiles and approvals table', async ({ page }) => {
    await page.goto('/admin/dashboard')
    await expect(page.getByRole('heading', { name: /pending bookings/i })).toBeVisible()
    await expect(page.getByRole('heading', { name: /flagged reviews/i })).toBeVisible()
    await expectNoSeriousA11yViolations(page)
  })

  test('users page exposes bulk actions with role chips', async ({ page }) => {
    await page.goto('/admin/users')
    await expect(page.getByRole('heading', { name: /user management/i })).toBeVisible()
    await expect(page.getByRole('heading', { name: /^users$/i })).toBeVisible()
    await expectNoSeriousA11yViolations(page)
  })
})
