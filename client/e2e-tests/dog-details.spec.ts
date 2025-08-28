import { test, expect } from '@playwright/test';

test.describe('Dog Details', () => {
  test('should navigate to dog details from homepage', async ({ page }) => {
    await page.goto('/');
    
    // Wait for dogs to load
    await page.waitForSelector('.grid a[href^="/dog/"]', { timeout: 10000 });
    
    // Get the first dog link
    const firstDogLink = page.locator('.grid a[href^="/dog/"]').first();
    
    // Get the dog name for verification
    const dogName = await firstDogLink.locator('h3').textContent();
    
    // Click on the first dog
    await firstDogLink.click();
    
    // Should be on a dog details page
    await expect(page.url()).toMatch(/\/dog\/\d+/);
    
    // Check that the page title is correct
    await expect(page).toHaveTitle(/Dog Details - Tailspin Shelter/);
    
    // Check for back button
    await expect(page.getByRole('link', { name: 'Back to All Dogs' })).toBeVisible();
  });

  test('should navigate back to homepage from dog details', async ({ page }) => {
    // Go directly to a dog details page (assuming dog with ID 1 exists)
    await page.goto('/dog/1');
    
    // Click the back button
    await page.getByRole('link', { name: 'Back to All Dogs' }).click();
    
    // Should be redirected to homepage
    await expect(page).toHaveURL('/');
    await expect(page.getByRole('heading', { name: 'Welcome to Tailspin Shelter' })).toBeVisible();
  });

  test('should handle invalid dog ID gracefully', async ({ page }) => {
    // Go to a dog page with an invalid ID
    await page.goto('/dog/99999');
    
    // The page should still load (even if no dog is found)
    await expect(page).toHaveTitle(/Dog Details - Tailspin Shelter/);
    
    // Back button should still be available
    await expect(page.getByRole('link', { name: 'Back to All Dogs' })).toBeVisible();
  });
});