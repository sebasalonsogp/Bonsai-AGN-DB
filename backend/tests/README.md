# Backend Tests

This directory contains tests for the backend application. Tests are organized by component type.

## Directory Structure

- `repositories/`: Tests for repository classes
- `api/`: Tests for API endpoints
- `schemas/`: Tests for schema validation
- `services/`: Tests for service layer components

## Running Tests

To run all tests:

```bash
cd backend
pytest
```

To run tests with verbose output:

```bash
pytest -v
```

To run tests in a specific directory:

```bash
pytest tests/repositories/
```

To run a specific test file:

```bash
pytest tests/repositories/test_photometry_repository.py
```

## Writing Tests

When adding new tests, follow these conventions:

1. Place tests in the appropriate directory based on the component being tested
2. Name test files with the prefix `test_` followed by the name of the module being tested
3. For asynchronous tests, use the `async def` syntax and `await` the function calls
4. Use fixtures defined in `conftest.py` for common test setup
5. Follow the AAA pattern: Arrange, Act, Assert

## Test Dependencies

The test suite uses:

- `pytest`: The main testing framework
- `pytest-asyncio`: For testing asynchronous code
- `unittest.mock`: For mocking dependencies

Make sure these are included in your development dependencies. 