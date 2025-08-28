import { test, expect } from '@playwright/test';

test.describe('About Page', () => {
  test('should load about page and display content', async ({ page }) => {
    await page.goto('/about');
    
    // Check that the page title is correct
    await expect(page).toHaveTitle(/About - Tailspin Shelter/);
    
    // Check that the main heading is visible
    await expect(page.getByRole('heading', { name: 'About Tailspin Shelter' })).toBeVisible();
    
    // Check that content is visible
    await expect(page.getByText('Nestled in the heart of Seattle')).toBeVisible();
    await expect(page.getByText('The name "Tailspin" reflects')).toBeVisible();
    
    // Check the fictional organization note
    await expect(page.getByText('Tailspin Shelter is a fictional organization')).toBeVisible();
  });

  test('should navigate back to homepage from about page', async ({ page }) => {
    await page.goto('/about');
    
    // Click the "Back to Dogs" button
    await page.getByRole('link', { name: 'Back to Dogs' }).click();
    
    // Should be redirected to homepage
    await expect(page).toHaveURL('/');
    await expect(page.getByRole('heading', { name: 'Welcome to Tailspin Shelter' })).toBeVisible();
  });
});