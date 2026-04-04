import { test, expect } from "@playwright/test";

test.describe("Work Orders Flow", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/login");
    await page.fill('input[type="email"]', "admin@precognito.ai");
    await page.fill('input[type="password"]', "Password123!");
    await page.click('button[type="submit"]');
  });

  test("should display work orders management", async ({ page }) => {
    await page.goto("/work-orders");
    await expect(page.locator("h1")).toContainText("Work Orders");
    await expect(page.locator("text=Assigned To")).toBeVisible();
  });
});
