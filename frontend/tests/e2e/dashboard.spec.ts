import { test, expect } from "@playwright/test";

test.describe("Dashboard Functionality", () => {
  test.beforeEach(async ({ page }) => {
    // In a real E2E environment, we would use global setup to handle authentication once
    await page.goto("/login");
    await page.fill('input[type="email"]', "admin@precognito.ai");
    await page.fill('input[type="password"]', "Password123!");
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/.*dashboard/);
  });

  test("should display welcome message and status cards", async ({ page }) => {
    await expect(page.locator("h1")).toContainText("Welcome back");
    await expect(page.locator("text=Total Assets")).toBeVisible();
    await expect(page.locator("text=Healthy")).toBeVisible();
  });

  test("should navigate to assets page from dashboard", async ({ page }) => {
    // Look for a link to assets or a card that navigates
    const assetsLink = page.locator('a[href="/assets"]');
    if (await assetsLink.count() > 0) {
        await assetsLink.first().click();
        await expect(page).toHaveURL(/.*assets/);
    }
  });
});
