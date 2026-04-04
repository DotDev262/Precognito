import { test, expect } from "@playwright/test";

test.describe("Reports and Analytics", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/login");
    await page.fill('input[type="email"]', "admin@precognito.ai");
    await page.fill('input[type="password"]', "Password123!");
    await page.click('button[type="submit"]');
  });

  test("should display reporting page with export options", async ({ page }) => {
    await page.goto("/reports");
    await expect(page.locator("h1")).toContainText("Reports");
    await expect(page.locator("text=Export PDF")).toBeVisible();
  });

  test("should display analytics page", async ({ page }) => {
    await page.goto("/analytics");
    await expect(page.locator("h1")).toContainText("Analytics");
    await expect(page.locator("text=Precision")).toBeVisible();
  });
});
