import { test, expect, Page } from '@playwright/test'

type Scene = {
  name: string
  path: string
  needsAuth?: boolean
  readySelector: string
}

const BREAKPOINTS = [1280, 1024, 768, 640]

const studentCredentials = {
  email: 'student@example.com',
  password: 'Demo123!',
}

async function login(page: Page) {
  await page.goto('/auth/login')
  await page.getByLabel('Email Address').fill(studentCredentials.email)
  await page.getByLabel('Password').fill(studentCredentials.password)
  await page.getByRole('button', { name: /login/i }).click()
  await page.waitForURL('**/dashboard')
}

const scenes: Scene[] = [
  {
    name: 'login',
    path: '/auth/login',
    readySelector: 'form',
  },
  {
    name: 'dashboard',
    path: '/dashboard',
    needsAuth: true,
    readySelector: '.resources-dashboard',
  },
  {
    name: 'resources-list',
    path: '/resources',
    needsAuth: true,
    readySelector: '.resources-list',
  },
]

test.describe('visual regressions', () => {
  for (const scene of scenes) {
    test(`${scene.name} responsive snapshots`, async ({ page }) => {
      if (scene.needsAuth) {
        await login(page)
      }

      for (const width of BREAKPOINTS) {
        await page.setViewportSize({ width, height: 900 })
        await page.goto(scene.path, { waitUntil: 'networkidle' })
        await page.waitForSelector(scene.readySelector)
        await expect(page).toHaveScreenshot(`${scene.name}-${width}.png`, {
          fullPage: true,
          animations: 'disabled',
        })
      }
    })
  }
})
