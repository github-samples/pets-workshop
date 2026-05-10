import { test, expect } from '@playwright/test';

test.describe('Staff Authentication', () => {
  test('guest browsing still works and shows login link', async ({ page }) => {
    await page.goto('/');

    await expect(page.getByRole('heading', { name: 'Welcome to Tailspin Shelter' })).toBeVisible();
    await expect(page.getByRole('link', { name: 'Login' })).toBeVisible();
  });

  test('guest visiting upload is sent to login', async ({ page }) => {
    await page.goto('/upload');

    await expect(page).toHaveURL(/\/login\?next=\/upload$/);
    await expect(page.getByRole('heading', { name: 'Staff Login' })).toBeVisible();
  });

  test('staff can log in and reach upload page', async ({ page }) => {
    await page.goto('/login');

    await page.getByTestId('login-submit').click();

    await expect(page).toHaveURL('/upload');
    await expect(page.getByTestId('upload-heading')).toHaveText('AI Listing Agent');
    await expect(page.getByRole('link', { name: 'Upload Listing' })).toBeVisible();
  });

  test('staff can log out and return to guest navigation', async ({ page }) => {
    await page.goto('/login');
    await page.getByTestId('login-submit').click();
    await expect(page).toHaveURL('/upload');

    await page.getByRole('button', { name: 'Logout' }).click();

    await expect(page).toHaveURL('/');
    await expect(page.getByRole('link', { name: 'Login' })).toBeVisible();
  });
});
