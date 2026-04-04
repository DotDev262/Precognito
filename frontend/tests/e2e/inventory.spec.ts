import { test, expect } from "@playwright/test";

test.describe("Inventory and Alerts", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/login");
    await page.fill('input[type="email"]', "admin@precognito.ai");
    await page.fill('input[type="password"]', "Password123!");
    await page.click('button[type="submit"]');
  });

  test("should display inventory management page", async ({ page }) => {
    await page.goto("/inventory");
    await expect(page.locator("h1")).toContainText("Inventory");
    await expect(page.locator("text=JIT Alerts")).toBeVisible();
  });

  test("should show alerts page", async ({ page }) => {
    await page.goto("/alerts");
    await expect(page.locator("h1")).toContainText("Alerts");
  });
});
