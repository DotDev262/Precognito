import { test, expect } from "@playwright/test";

test.describe("Authentication and Dashboard", () => {
  test("should show login page by default", async ({ page }) => {
    await page.goto("/dashboard");
    // Should redirect to login because of middleware
    await expect(page).toHaveURL(/.*login/);
    await expect(page.locator("h1")).toContainText("Precognito");
  });

  test("should login successfully with valid credentials", async ({ page }) => {
    await page.goto("/login");
    
    // Fill login form
    await page.fill('input[type="email"]', "admin@precognito.ai");
    await page.fill('input[type="password"]', "Password123!");
    
    await page.click('button[type="submit"]');
    
    // Should navigate to dashboard
    await expect(page).toHaveURL(/.*dashboard/);
    await expect(page.locator("nav")).toBeVisible();
  });

  test("should show validation errors for weak passwords", async ({ page }) => {
    await page.goto("/login");
    
    await page.fill('input[type="email"]', "test@example.com");
    await page.fill('input[type="password"]', "weak");
    
    await page.click('button[type="submit"]');
    
    // Check for validation message added in previous security hardening
    await expect(page.locator("text=Password must be at least 8 characters")).toBeVisible();
  });
});
