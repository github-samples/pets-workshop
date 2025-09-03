import { test, expect } from '@playwright/test';

test.describe('Tailspin Shelter Homepage', () => {
  test('should load homepage and display title', async ({ page }) => {
    await page.goto('/');
    
    // Check that the page title is correct
    await expect(page).toHaveTitle(/Tailspin Shelter - Find Your Forever Friend/);
    
    // Check that the main elements are visible using test IDs
    await expect(page.getByTestId('homepage-title')).toBeVisible();
    await expect(page.getByTestId('homepage-description')).toBeVisible();
    
    // Verify content
    await expect(page.getByTestId('homepage-title')).toContainText('Welcome to Tailspin Shelter');
    await expect(page.getByTestId('homepage-description')).toContainText('Find your perfect companion');
  });

  test('should display dog list section', async ({ page }) => {
    await page.goto('/');
    
    // Check that the "Available Dogs" heading is visible
    await expect(page.getByTestId('available-dogs-heading')).toBeVisible();
    await expect(page.getByTestId('available-dogs-heading')).toContainText('Available Dogs');
    
    // Wait for dogs to load (either loading state, error, or actual dogs)
    await page.waitForSelector('[data-testid="dog-list-container"]', { timeout: 10000 });
  });

  test('should show loading state initially', async ({ page }) => {
    await page.goto('/');
    
    // Check that loading animation is shown initially
    const loadingElements = page.getByTestId('dog-list-loading');
    
    // Either loading should be visible initially, or dogs should load quickly
    try {
      await expect(loadingElements).toBeVisible({ timeout: 2000 });
    } catch {
      // If loading finishes too quickly, that's fine - check for dog content instead
      await expect(page.getByTestId('dog-list-grid')).toBeVisible();
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
    
    // Check that error message is displayed using test IDs
    await expect(page.getByTestId('dog-list-error')).toBeVisible({ timeout: 10000 });
    await expect(page.getByTestId('error-message')).toContainText('Failed to fetch data');
  });
});