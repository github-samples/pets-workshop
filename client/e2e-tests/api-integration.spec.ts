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
    
    // Wait for dog list to load
    await expect(page.getByTestId('dog-list-grid')).toBeVisible({ timeout: 10000 });
    
    // Check that mocked dogs are displayed using test IDs
    await expect(page.getByTestId('dog-name-1')).toContainText('Buddy');
    await expect(page.getByTestId('dog-breed-1')).toContainText('Golden Retriever');
    await expect(page.getByTestId('dog-name-2')).toContainText('Luna');
    await expect(page.getByTestId('dog-breed-2')).toContainText('Husky');
    await expect(page.getByTestId('dog-name-3')).toContainText('Max');
    await expect(page.getByTestId('dog-breed-3')).toContainText('Labrador');
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
    
    // Check that empty state message is displayed using test IDs
    await expect(page.getByTestId('dog-list-empty')).toBeVisible({ timeout: 10000 });
    await expect(page.getByTestId('empty-message')).toContainText('No dogs available at the moment');
  });

  test('should handle network errors', async ({ page }) => {
    // Mock network error
    await page.route('/api/dogs', route => {
      route.abort('failed');
    });

    await page.goto('/');
    
    // Check that error message is displayed using test IDs
    await expect(page.getByTestId('dog-list-error')).toBeVisible({ timeout: 10000 });
    await expect(page.getByTestId('error-message')).toContainText('Error:');
  });
});