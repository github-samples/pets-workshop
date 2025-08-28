import { test, expect } from '@playwright/test';

test.describe('API Integration', () => {
  test('should fetch dogs from API', async ({ page }) => {
    // Mock successful API response
    await page.route('/api/dogs', route => {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify([
          { id: 1, name: 'Buddy', breed: 'Golden Retriever' },
          { id: 2, name: 'Luna', breed: 'Husky' },
          { id: 3, name: 'Max', breed: 'Labrador' }
        ])
      });
    });

    await page.goto('/');
    
    // Check that mocked dogs are displayed
    await expect(page.getByText('Buddy')).toBeVisible();
    await expect(page.getByText('Golden Retriever')).toBeVisible();
    await expect(page.getByText('Luna')).toBeVisible();
    await expect(page.getByText('Husky')).toBeVisible();
    await expect(page.getByText('Max')).toBeVisible();
    await expect(page.getByText('Labrador')).toBeVisible();
  });

  test('should handle empty dog list', async ({ page }) => {
    // Mock empty API response
    await page.route('/api/dogs', route => {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify([])
      });
    });

    await page.goto('/');
    
    // Check that empty state message is displayed
    await expect(page.getByText('No dogs available at the moment')).toBeVisible();
  });

  test('should handle network errors', async ({ page }) => {
    // Mock network error
    await page.route('/api/dogs', route => {
      route.abort('failed');
    });

    await page.goto('/');
    
    // Check that error message is displayed
    await expect(page.getByText(/Error:/)).toBeVisible({ timeout: 10000 });
  });
});