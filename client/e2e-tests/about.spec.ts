import { test, expect } from '@playwright/test';

test.describe('About Page', () => {
  test('should load about page and display content', async ({ page }) => {
    await page.goto('/about');
    
    // Check that the page title is correct
    await expect(page).toHaveTitle(/About - Tailspin Shelter/);
    
    // Check that the main elements are visible using test IDs
    await expect(page.getByTestId('about-page-container')).toBeVisible();
    await expect(page.getByTestId('about-page-title')).toBeVisible();
    await expect(page.getByTestId('about-page-title')).toContainText('About Tailspin Shelter');
    
    // Check that content is visible
    await expect(page.getByTestId('about-page-description-1')).toContainText('Nestled in the heart of Seattle');
    await expect(page.getByTestId('about-page-description-2')).toContainText('The name "Tailspin" reflects');
    
    // Check the fictional organization note
    await expect(page.getByTestId('fictional-organization-note')).toContainText('Tailspin Shelter is a fictional organization');
  });

  test('should navigate back to homepage from about page', async ({ page }) => {
    await page.goto('/about');
    
    // Wait for page to load
    await expect(page.getByTestId('about-page-container')).toBeVisible();
    
    // Click the "Back to Dogs" button using test ID
    await page.getByTestId('back-to-dogs-button').click();
    
    // Should be redirected to homepage
    await expect(page).toHaveURL('/');
    await expect(page.getByTestId('homepage-container')).toBeVisible();
    await expect(page.getByTestId('homepage-title')).toContainText('Welcome to Tailspin Shelter');
  });
});