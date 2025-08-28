# Test Identifiers Reference

This document provides a comprehensive reference for all `data-testid` attributes used in the Tailspin Shelter application for E2E testing with Playwright.

## Why Test Identifiers?

Test identifiers (`data-testid` attributes) provide stable, reliable selectors for E2E tests that won't break when:
- CSS classes change
- Styling is updated
- Component structure is refactored
- Text content is modified

## Naming Conventions

- **Format**: Use kebab-case (`dog-card-1`, `homepage-title`)
- **Descriptive**: Include component and purpose in the name
- **Unique**: Append IDs for repeated elements (`dog-card-${id}`)
- **Hierarchical**: Use prefixes for related elements (`dog-details-name`, `dog-details-breed`)

## Component Test IDs

### Homepage (`src/pages/index.astro`)
- `homepage-container`: Main page wrapper
- `homepage-title`: Welcome heading
- `homepage-description`: Descriptive text

### Dog List (`src/components/DogList.svelte`)
- `dog-list-container`: Main container
- `available-dogs-heading`: Section heading
- `dog-list-grid`: Grid of dog cards
- `dog-list-loading`: Loading state container
- `dog-list-error`: Error state container
- `dog-list-empty`: Empty state container
- `dog-card-{id}`: Individual dog cards (with ID)
- `dog-name-{id}`: Dog name within card
- `dog-breed-{id}`: Dog breed within card
- `dog-view-details-{id}`: View details link

### Dog Details (`src/components/DogDetails.svelte`)
- `dog-details-page`: Page container
- `dog-details-container`: Main details container
- `dog-details-loading`: Loading state
- `dog-details-error`: Error state
- `dog-details-no-data`: No data state
- `dog-details-name`: Dog name heading
- `dog-details-breed`: Breed information
- `dog-details-age`: Age information
- `dog-details-gender`: Gender information
- `dog-details-description`: About text
- `dog-details-about-heading`: About section heading
- `dog-status-available`: Available status badge
- `dog-status-pending`: Pending status badge
- `dog-status-adopted`: Adopted status badge

### Navigation
- `back-to-dogs-button`: Navigation button (dog details and about pages)
- `navigation-section`: Navigation container

### About Page (`src/pages/about.astro`)
- `about-page-container`: Page wrapper
- `about-page-title`: Page heading
- `about-page-content`: Main content area
- `about-page-description-1`: First paragraph
- `about-page-description-2`: Second paragraph
- `about-page-note`: Disclaimer section
- `fictional-organization-note`: Fictional org note
- `about-page-navigation`: Navigation section

### Header (`src/components/Header.astro`)
- `site-header`: Header container
- `menu-toggle-button`: Hamburger menu button
- `navigation-menu`: Dropdown menu
- `nav-home-link`: Home navigation link
- `nav-about-link`: About navigation link
- `site-title`: Site title heading
- `site-title-link`: Site title link

### Common State Elements
- `{component}-loading`: Loading states
- `{component}-error`: Error states
- `{component}-empty`: Empty states
- `error-message`: Error message text
- `empty-message`: Empty state message text

## Usage in Tests

### Preferred Locator Strategy
```typescript
// 1. Test IDs (most reliable)
await page.getByTestId('dog-card-1').click();
await expect(page.getByTestId('homepage-title')).toBeVisible();

// 2. Semantic locators (when test IDs aren't available)
await page.getByRole('heading', { name: 'Welcome' }).click();

// 3. Text content (for validation)
await expect(page.getByTestId('dog-name-1')).toContainText('Buddy');
```

### Common Patterns
```typescript
// Wait for content to load
await page.waitForSelector('[data-testid="dog-list-grid"]', { timeout: 10000 });

// Navigate to dog details
await page.getByTestId('dog-card-1').click();
await expect(page.getByTestId('dog-details-container')).toBeVisible();

// Handle error states
await expect(page.getByTestId('dog-list-error')).toBeVisible();
await expect(page.getByTestId('error-message')).toContainText('Failed to fetch');
```

## Adding New Test IDs

When creating new components or pages:

1. **Container**: Always add a main container ID
2. **States**: Include loading, error, and empty states
3. **Interactive Elements**: Buttons, links, form inputs
4. **Content**: Important headings and text
5. **Lists**: Individual items with unique identifiers

Example:
```svelte
<div data-testid="new-component-container">
  {#if loading}
    <div data-testid="new-component-loading">Loading...</div>
  {:else if error}
    <div data-testid="new-component-error">
      <p data-testid="error-message">{error}</p>
    </div>
  {:else}
    <div data-testid="new-component-content">
      {#each items as item}
        <div data-testid={`item-${item.id}`}>
          <h3 data-testid={`item-title-${item.id}`}>{item.title}</h3>
        </div>
      {/each}
    </div>
  {/if}
</div>
```
