# End-to-End Tests for Tailspin Shelter

This directory contains Playwright end-to-end tests for the Tailspin Shelter website.

## Test Files

- `homepage.spec.ts` - Tests for the main homepage functionality
- `about.spec.ts` - Tests for the about page
- `dog-details.spec.ts` - Tests for individual dog detail pages
- `api-integration.spec.ts` - Tests for API integration and error handling

## Running Tests

### Prerequisites

Make sure you have installed dependencies:
```bash
npm install
```

### Running Tests

```bash
# Run all tests
npm run test:e2e

# Run tests with UI mode (for debugging)
npm run test:e2e:ui

# Run tests in headed mode (see browser)
npm run test:e2e:headed

# Run only WebKit tests
npm run test:e2e:webkit

# Debug tests
npm run test:e2e:debug
```

## Test Coverage

The tests cover the following core functionality:

### Homepage Tests
- Page loads with correct title and content
- Dog list displays properly
- Loading states work correctly
- Error handling for API failures

### About Page Tests
- About page content displays correctly
- Navigation back to homepage works

### Dog Details Tests
- Navigation from homepage to dog details
- Navigation back from dog details to homepage
- Handling of invalid dog IDs

### API Integration Tests
- Successful API responses
- Empty dog list handling
- Network error handling

## Configuration

Tests are configured in `../playwright.config.ts` and automatically start the application servers using the existing `scripts/start-app.sh` script before running tests.

The tests run against:
- Client (Astro): http://localhost:4321
- Server (Flask): http://localhost:5100