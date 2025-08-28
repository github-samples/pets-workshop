# Tailspin Shelter

The Tailspin Shelter is a full-stack web application that showcases a fictional dog shelter.

## Technology Stack

### Frontend (Client)

- **Framework**: [Astro](https://astro.build/) v5.4+ - Static site generator with server-side rendering
- **Component Library**: [Svelte](https://svelte.dev/) v5.23+ - For dynamic interactive components
- **Styling**: [Tailwind CSS](https://tailwindcss.com/) v4.0+ - Utility-first CSS framework
- **Language**: TypeScript - Strongly typed JavaScript
- **Adapter**: Node.js adapter for server-side rendering

### Backend (Server)

- **Framework**: [Flask](https://flask.palletsprojects.com/) - Python web framework
- **Database**: SQLite with [SQLAlchemy](https://www.sqlalchemy.org/) ORM
- **Language**: Python 3.13+ with type hints
- **CORS**: Flask-CORS for cross-origin requests

### Testing

- **Python/Server/Flask**: Python unittest framework
- **E2E testing**: [Playwright](https://playwright.dev/) v1.49+ - End-to-end testing framework

## Project Structure

```
pets-workshop/
├── client/                 # Astro frontend application
│   ├── src/components/     # Svelte components (DogList, DogDetails)
│   ├── src/layouts/        # Astro layout templates
│   ├── src/pages/          # Astro pages (routing)
│   ├── src/styles/         # Global CSS and Tailwind imports
│   └── e2e-tests/          # Playwright end-to-end tests
├── server/                 # Flask backend API
│   ├── models/             # SQLAlchemy models (Dog, Breed)
│   ├── tests/              # Python unit tests
│   └── app.py              # Main Flask application
└── scripts/                # Automation scripts (run-tests.sh, setup-environment.sh, start-app.sh)
```

## Design Philosophy & Theme

**CRITICAL**: Maintain the dark, modern aesthetic throughout:
- **HTML Class**: Always include `class="dark"` on the html element
- **Background**: Use `bg-slate-900` for main backgrounds
- **Text**: Default to `text-white` for primary content
- **Typography**: Inter font family with clean, readable text
- **Responsive**: Mobile-first approach using Tailwind's responsive prefixes
- **Transitions**: Include `transition-colors duration-300` for smooth interactions

## Development Guidelines

### Use Scripts, Not Direct Commands
**IMPORTANT**: Always prefer using the provided scripts in the `scripts/` directory rather than running commands directly:
- **Testing**: Use `./scripts/run-server-tests.sh` instead of `python -m unittest`
- **E2E Testing**: Use `./scripts/run-e2e-tests` instead of `npm run tests:e2e`
- **Environment Setup**: Use `./scripts/setup-environment.sh` for initial setup
- **Application Start**: Use `./scripts/start-app.sh` to launch the application

### API Patterns
- **Endpoints**: RESTful API design with `/api/` prefix
- **Response Format**: Always return JSON with proper HTTP status codes
- **Type Hints**: Use Python type hints for all function parameters and returns

### Frontend Patterns
- **Component Structure**: Use Svelte for interactive components, Astro for static layouts
- **Data Fetching**: Fetch data on the server side when possible
- **Styling**: Use Tailwind utility classes, avoid custom CSS unless necessary
- **Routing**: File-based routing through Astro's pages directory
- **Test Identifiers**: Always include `data-testid` attributes for E2E testing resilience (see [`test-identifiers.md`](./instructions/test-identifiers.md))

### Database Patterns
- **Models**: Use SQLAlchemy declarative base with proper relationships
- **Queries**: Prefer SQLAlchemy query syntax over raw SQL
- **Data Seeding**: Use the utilities in `utils/seed_database.py`

### Testing Patterns

Below are the only types of tests we use in this project. Do not add additional test types unless instructed otherwise.

- **E2E Tests**: Playwright tests in `client/e2e-tests/` cover full user workflows
- **Unit tests**: Unit tests for Flask endpoints and utilities, stored in `server/tests`

## Coding Standards

### Python (Backend)
- Follow PEP 8 style guidelines
- Use type hints for all function signatures
- Use meaningful variable names with snake_case
- Handle exceptions gracefully with proper error messages

### TypeScript/JavaScript (Frontend)
- Use TypeScript for type safety
- Follow Astro's component conventions
- Use camelCase for variables and functions
- Include proper prop types for Svelte components

### CSS/Styling
- Use Tailwind utility classes primarily
- Maintain dark theme consistency
- Ensure responsive design across all breakpoints
- Use semantic HTML elements when possible

## AI Assistant Guidelines

When working with this codebase:
1. Always maintain the dark theme aesthetic
2. Use the provided scripts for common operations
3. Follow the established patterns for API responses and component structure
4. Utilize the tests to validate app behavior; don't launch the app or run `curl` commands to do so
4. Ensure type safety in both Python and TypeScript code
5. Test changes using the appropriate testing frameworks
