import { test, expect } from '@playwright/test';

test.describe('Dog Details', () => {
  test('should navigate to dog details from homepage', async ({ page }) => {
    await page.goto('/');
    
    // Wait for dogs to load using test ID
    await page.waitForSelector('[data-testid="dog-list-grid"]', { timeout: 10000 });
    
    // Get the first dog card using test ID
    const firstDogCard = page.getByTestId('dog-card-1');
    await expect(firstDogCard).toBeVisible();
    
    // Get the dog name for verification
    const dogName = await firstDogCard.getByTestId('dog-name-1').textContent();
    
    // Click on the first dog
    await firstDogCard.click();
    
    // Should be on a dog details page
    await expect(page.url()).toMatch(/\/dog\/1/);
    
    // Check that the page title is correct
    await expect(page).toHaveTitle(/Dog Details - Tailspin Shelter/);
    
    // Check for dog details container and back button using test IDs
    await expect(page.getByTestId('dog-details-container')).toBeVisible();
    await expect(page.getByTestId('back-to-dogs-button')).toBeVisible();
    
    // Verify the dog name matches
    if (dogName) {
      await expect(page.getByTestId('dog-details-name')).toContainText(dogName);
    }
  });

  test('should navigate back to homepage from dog details', async ({ page }) => {
    // Go directly to a dog details page (assuming dog with ID 1 exists)
    await page.goto('/dog/1');
    
    // Wait for dog details to load
    await expect(page.getByTestId('dog-details-page')).toBeVisible();
    
    // Click the back button using test ID
    await page.getByTestId('back-to-dogs-button').click();
    
    // Should be redirected to homepage
    await expect(page).toHaveURL('/');
    await expect(page.getByTestId('homepage-container')).toBeVisible();
    await expect(page.getByTestId('homepage-title')).toContainText('Welcome to Tailspin Shelter');
  });

  test('should handle invalid dog ID gracefully', async ({ page }) => {
    // Go to a dog page with an invalid ID
    await page.goto('/dog/99999');
    
    // The page should still load (even if no dog is found)
    await expect(page).toHaveTitle(/Dog Details - Tailspin Shelter/);
    await expect(page.getByTestId('dog-details-page')).toBeVisible();
    
    // Back button should still be available
    await expect(page.getByTestId('back-to-dogs-button')).toBeVisible();
    
    // Should show either error state or no data message
    try {
      await expect(page.getByTestId('dog-details-error')).toBeVisible({ timeout: 5000 });
    } catch {
      await expect(page.getByTestId('dog-details-no-data')).toBeVisible();
    }
  });
});