# Medical Appointment System

This is a FastAPI backend for a medical appointment scheduling system, built using hexagonal architecture principles.

## Prerequisites

- Python 3.11+
- Poetry
- PostgreSQL (for database)

## Setup

1. Clone the repository

2. Install Poetry (if not already installed)::

   ```
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. Create and activate the virtual environment:

   ```
   poetry shell
   ```

   This command creates a virtual environment (if it doesn't exist) and activates it.

4. Install dependencies:

   ```
   make install
   ```

   Note: If you're on Windows and `make` is not available, you can run the equivalent command:

   ```
   poetry install
   ```

After completing these steps, your virtual environment will be activated and all dependencies installed.

To deactivate the virtual environment when you're done working on the project, simply run:

```
deactivate
```

## Development

### Running the application

To run the application in development mode:

```
make run
```

The API will be available at `http://localhost:8000`. You can access the API documentation at `http://localhost:8000/docs`.

### Code Formatting and Linting

To format the code:

```
make format
```

To run linters:

```
make lint
```

To run tests:

```
make test
```

### Updating Dependencies

To update project dependencies:

```
make update
```

## Project Structure

The project follows a hexagonal architecture:

```
/
│
├── api/
│   ├── src/
│   │   ├── dtos/
│   │   ├── events/
│   │   ├── exception_handlers/
│   │   └── routers/
│   │       ├── v1/
│   │       └── v2/
│   └── tests/
│
├── core/
│   ├── src/
│   │   ├── exceptions/
│   │   │   ├── business/
│   │   │   └── repository/
│   │   ├── repositories/
│   │   ├── use_cases/
│   │   └── models/
│   └── tests/
│
├── adapters/
│   ├── src/
│   │   ├── repositories/
│   └── tests/
├── factories
```

- `api/`: Contains API-related components
  - `dtos/`: Data Transfer Objects for API requests and responses
  - `events/`: Event handlers for API-related events
  - `exception_handlers/`: Custom exception handlers for API errors
  - `routers/`: API route definitions, separated by versions
- `core/`: Contains the core business logic
  - `exceptions/`: Custom exceptions for business logic and repositories
  - `repositories/`: Repository interfaces
  - `use_cases/`: Application use cases (business logic)
  - `models/`: Domain models
- `adapters/`: Contains implementations of interfaces defined in the core
  - `repositories/`: Concrete implementations of repository interfaces
- `factories/`: Factory classes for creating complex objects

## Development Workflow

### Branch Strategy

We follow a branch naming convention based on our Jira tickets:

```
git checkout -b AP-<ticket-number>-brief-description
```

For example:

```
git checkout -b AP-7-initialize-backend
```

### Commit Conventions

We use Conventional Commits to standardize our commit messages. The format is as follows:

```
<type>(<optional scope>): <description> (<ticket number>)
[optional body]
[optional footer(s)]
```

Types include:

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code (white-space, formatting, etc)
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to the build process or auxiliary tools and libraries such as documentation generation

Include the Jira ticket number in parentheses at the end of the description.

Examples:

```
feat(auth): implement JWT authentication (AP-7)
fix(api): resolve database connection issue (AP-12)
docs(readme): update development workflow (AP-15)
style(ui): format CSS according to style guide (AP-18)
refactor(utils): simplify error handling functions (AP-20)
```

The scope is optional but recommended when it adds clarity. The ticket number should always be included.

For more details on Conventional Commits, visit [https://www.conventionalcommits.org/](https://www.conventionalcommits.org/)
