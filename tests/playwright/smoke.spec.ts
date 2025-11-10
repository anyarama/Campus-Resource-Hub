import { test, expect, Page } from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'

const credentials = {
  email: 'student@example.com',
  password: 'Demo123!'
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

async function login(page: Page) {
  await page.goto('/auth/login')
  await page.getByLabel('Email Address').fill(credentials.email)
  await page.getByLabel('Password').fill(credentials.password)
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
    await login(page)
    await expect(page.getByRole('heading', { name: /welcome/i })).toBeVisible()
    await expect(page.locator('#bookings-timeline-chart')).toBeVisible()
    await expectNoSeriousA11yViolations(page)
  })
})
