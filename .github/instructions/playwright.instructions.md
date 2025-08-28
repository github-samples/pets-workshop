---
applyTo: "**/*.spec.ts"
---

# Playwright E2E Testing Guidelines for Tailspin Shelter

Essential patterns for writing effective Playwright tests in the Tailspin Shelter application.

## Core Principles

1. **Test User Workflows** - Focus on complete user journeys, not implementation details
2. **Use Semantic Locators** - Prefer `getByRole()`, `getByText()`, `getByLabel()` over CSS selectors
3. **Handle Async Behavior** - Always account for loading states and API calls

## Locator Patterns

### Preferred Approach
```typescript
// ✅ Semantic locators
await expect(page.getByRole('heading', { name: 'Welcome to Tailspin Shelter' })).toBeVisible();
await page.getByRole('link', { name: 'Back to All Dogs' }).click();
await expect(page.getByText('Find your perfect companion')).toBeVisible();

// ✅ Test IDs when needed
await page.getByTestId('dog-card-123').click();
```

### Avoid
```typescript
// ❌ Fragile selectors
await page.locator('.bg-slate-800 .p-6 h3').click();
await page.locator('a').nth(0).click();
```

## Essential Test Patterns

### Basic Test Structure
```typescript
import { test, expect } from '@playwright/test';

test.describe('Feature Name', () => {
  test('should perform user action', async ({ page }) => {
    await page.goto('/');
    await page.getByRole('button', { name: 'Submit' }).click();
    await expect(page.getByText('Success')).toBeVisible();
  });
});
```

### Loading States
```typescript
test('should handle loading content', async ({ page }) => {
  await page.goto('/');
  
  // Wait for content to load
  await page.waitForSelector('.grid', { timeout: 10000 });
  
  // Verify loading is complete
  await expect(page.locator('.animate-pulse')).not.toBeVisible();
  await expect(page.getByRole('link', { name: /dog/i }).first()).toBeVisible();
});
```

### Navigation Flow
```typescript
test('should navigate dog details workflow', async ({ page }) => {
  await page.goto('/');
  
  // Wait for dogs to load
  await page.waitForSelector('.grid a[href^="/dog/"]', { timeout: 10000 });
  
  // Click first dog
  const firstDogLink = page.locator('.grid a[href^="/dog/"]').first();
  await firstDogLink.click();
  
  // Verify navigation
  await expect(page.url()).toMatch(/\/dog\/\d+/);
  await expect(page).toHaveTitle(/Dog Details/);
  
  // Navigate back
  await page.getByRole('link', { name: 'Back to All Dogs' }).click();
  await expect(page).toHaveURL('/');
});
```

### Error Handling
```typescript
test('should handle API errors', async ({ page }) => {
  // Mock API failure
  await page.route('/api/dogs', route => {
    route.fulfill({
      status: 500,
      body: JSON.stringify({ error: 'Server Error' })
    });
  });

  await page.goto('/');
  await expect(page.getByText(/Failed to fetch/)).toBeVisible({ timeout: 10000 });
});
```

## Common Assertions

```typescript
// Page state
await expect(page).toHaveTitle(/Expected Title/);
await expect(page).toHaveURL('/path');

// Element visibility
await expect(page.getByRole('heading', { name: 'Title' })).toBeVisible();
await expect(page.getByText('Loading')).not.toBeVisible();

// Element states
await expect(page.getByRole('button')).toBeEnabled();
await expect(page.getByRole('textbox')).toHaveValue('value');
```

## File Organization

- `homepage.spec.ts` - Main page tests
- `dog-details.spec.ts` - Individual dog page tests
- `api-integration.spec.ts` - API error scenarios
- `navigation.spec.ts` - Navigation workflows

## Running Tests

```bash
npm run test:e2e          # Run all tests
npm run test:e2e:ui       # Debug with UI
npm run test:e2e:headed   # See browser
```

## Key Tips

- Use `page.waitForSelector()` for dynamic content, not `networkidle`
- Group tests with `test.describe()` and descriptive names
- Set reasonable timeouts (5-10 seconds)
- Test real user scenarios, not implementation details
