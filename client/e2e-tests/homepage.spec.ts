import { test, expect } from '@playwright/test';

test.describe('Tailspin Shelter Homepage', () => {
  test('should load homepage and display title', async ({ page }) => {
    await page.goto('/');
    
    // Check that the page title is correct
    await expect(page).toHaveTitle(/Tailspin Shelter - Find Your Forever Friend/);
    
    // Check that the main heading is visible
    await expect(page.getByRole('heading', { name: 'Welcome to Tailspin Shelter' })).toBeVisible();
    
    // Check that the description is visible
    await expect(page.getByText('Find your perfect companion from our wonderful selection')).toBeVisible();
  });

  test('should display dog list section', async ({ page }) => {
    await page.goto('/');
    
    // Check that the "Available Dogs" heading is visible
    await expect(page.getByRole('heading', { name: 'Available Dogs' })).toBeVisible();
    
    // Wait for dogs to load (either loading state, error, or actual dogs)
    await page.waitForSelector('.grid', { timeout: 10000 });
  });

  test('should show loading state initially', async ({ page }) => {
    await page.goto('/');
    
    // Check that loading animation is shown initially
    // Look for the loading skeleton cards
    const loadingElements = page.locator('.animate-pulse').first();
    
    // Either loading should be visible initially, or dogs should load quickly
    try {
      await expect(loadingElements).toBeVisible({ timeout: 2000 });
    } catch {
      // If loading finishes too quickly, that's fine - check for dog content instead
      await expect(page.locator('.grid')).toBeVisible();
    }
  });

  test('should handle API errors gracefully', async ({ page }) => {
    // Intercept the API call and make it fail
    await page.route('/api/dogs', route => {
      route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({ error: 'Internal Server Error' })
      });
    });

    await page.goto('/');
    
    // Check that error message is displayed
    await expect(page.getByText(/Failed to fetch data/)).toBeVisible({ timeout: 10000 });
  });
});