---
applyTo: "**/*.spec.ts"
---

# Playwright E2E Testing Guidelines for Tailspin Shelter

Essential patterns for writing effective Playwright tests in the Tailspin Shelter application.

## Core Principles

1. **Test User Workflows** - Focus on complete user journeys, not implementation details
2. **Use Test IDs First** - Always prefer `data-testid` attributes for reliable element identification
3. **Semantic Locators Second** - Use `getByRole()`, `getByText()`, `getByLabel()` when test IDs aren't available
4. **Handle Async Behavior** - Always account for loading states and API calls

> 📋 **Reference**: See [`test-identifiers.md`](./test-identifiers.md) for complete list of available test IDs

## Locator Patterns

### Preferred Approach (In Order of Priority)
```typescript
// ✅ Test IDs (most reliable)
await page.getByTestId('dog-card-1').click();
await expect(page.getByTestId('homepage-title')).toBeVisible();
await page.getByTestId('back-to-dogs-button').click();

// ✅ Semantic locators (when test IDs aren't available)
await page.getByRole('heading', { name: 'Welcome to Tailspin Shelter' }).click();
await page.getByRole('link', { name: 'Back to All Dogs' }).click();

// ✅ Combined approach (test ID + semantic validation)
const dogCard = page.getByTestId('dog-card-1');
await expect(dogCard.getByTestId('dog-name-1')).toContainText('Buddy');
await dogCard.click();
```

### Avoid
```typescript
// ❌ Fragile CSS selectors
await page.locator('.bg-slate-800 .p-6 h3').click();
await page.locator('a').nth(0).click();
await page.locator('.grid > div:first-child').click();
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
  
  // Wait for content to load using test IDs
  await page.waitForSelector('[data-testid="dog-list-grid"]', { timeout: 10000 });
  
  // Verify loading is complete
  await expect(page.getByTestId('dog-list-loading')).not.toBeVisible();
  await expect(page.getByTestId('dog-card-1')).toBeVisible();
});
```

### Navigation Flow
```typescript
test('should navigate dog details workflow', async ({ page }) => {
  await page.goto('/');
  
  // Wait for dogs to load using test ID
  await page.waitForSelector('[data-testid="dog-list-grid"]', { timeout: 10000 });
  
  // Click first dog using test ID
  await page.getByTestId('dog-card-1').click();
  
  // Verify navigation
  await expect(page.url()).toMatch(/\/dog\/\d+/);
  await expect(page).toHaveTitle(/Dog Details/);
  await expect(page.getByTestId('dog-details-container')).toBeVisible();
  
  // Navigate back using test ID
  await page.getByTestId('back-to-dogs-button').click();
  await expect(page).toHaveURL('/');
  await expect(page.getByTestId('homepage-container')).toBeVisible();
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
  
  // Verify error state using test ID
  await expect(page.getByTestId('dog-list-error')).toBeVisible({ timeout: 10000 });
  await expect(page.getByTestId('error-message')).toContainText('Failed to fetch');
});
```

## Common Assertions

```typescript
// Page state
await expect(page).toHaveTitle(/Expected Title/);
await expect(page).toHaveURL('/path');

// Element visibility using test IDs
await expect(page.getByTestId('homepage-title')).toBeVisible();
await expect(page.getByTestId('dog-list-loading')).not.toBeVisible();

// Element content using test IDs
await expect(page.getByTestId('dog-name-1')).toContainText('Buddy');
await expect(page.getByTestId('error-message')).toContainText('Failed to fetch');

// Element states using test IDs
await expect(page.getByTestId('submit-button')).toBeEnabled();
await expect(page.getByTestId('search-input')).toHaveValue('search term');
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

- **Use test IDs first**: Always prefer `data-testid` attributes for reliable element identification
- Use `page.waitForSelector('[data-testid="element"]')` for dynamic content, not `networkidle`
- Group tests with `test.describe()` and descriptive names
- Set reasonable timeouts (5-10 seconds)
- Test real user scenarios, not implementation details
- Include both happy path and error scenarios in your test suites
