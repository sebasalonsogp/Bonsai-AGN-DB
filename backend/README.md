# AGN-DB Backend

This document provides a detailed technical overview of the backend architecture, implementation patterns, and developer guidelines for the Astrophysics AGN Database (AGN-DB) web application.

## Architectural Overview

The AGN-DB backend follows a rigorously structured approach based on the following design principles:

### Clean Architecture

The codebase is organized according to Clean Architecture principles with Repository pattern & CQRS-lite, establishing clear boundaries between:

- **API Layer**: Handles HTTP requests/responses
- **Service Layer**: Contains business logic and orchestration
- **Repository Layer**: Abstracts data access operations
- **Data Layer**: ORM models and database connection

This separation of concerns enables:
- ✅ Independent testing of each layer
- ✅ Swappable implementation details (e.g., changing database providers)
- ✅ Clear responsibility boundaries
- ✅ Code that is easier to maintain and extend

### Repository Pattern

The Repository Pattern provides a clean abstraction over data access:
- Repository interfaces define data operations
- Implementation details of database access are isolated
- Business logic never interacts directly with ORM models
- Query-specific repositories can optimize for specific use cases

### CQRS-lite

Command Query Responsibility Segregation (CQRS-lite) separates:
- **Commands**: Write operations that modify state (POST, PUT, DELETE)
- **Queries**: Read operations that return data without side effects (GET)

This separation allows for optimized:
- Read models tuned for specific query patterns
- Independent scaling of read and write operations
- Clear API organization by responsibility

## Architectural Layers and Their Interactions

### Layer Purposes and Responsibilities

#### 1. API Layer (`/api/`)
- **Primary Purpose**: Acts as the interface between clients and the application core
- **Key Responsibilities**:
  - Translates HTTP requests into application commands and queries
  - Validates incoming data using Pydantic schemas
  - Handles request routing and parameter extraction
  - Maps internal results to appropriate HTTP responses
  - Implements proper status codes and error handling
  - Documents endpoints via OpenAPI/Swagger annotations
- **Why it matters**: This layer isolates all HTTP/REST-specific concerns from the application core, allowing the core to remain protocol-agnostic. It enables easy adaptation to different API protocols (REST, GraphQL) without changing business logic.

#### 2. Service Layer (`/services/`)
- **Primary Purpose**: Implements business logic and orchestrates multiple operations
- **Key Responsibilities**:
  - Coordinates multiple repository operations within a single business transaction
  - Enforces business rules that span multiple entities
  - Provides domain-specific operations that don't map directly to CRUD
  - Handles complex workflows that require multiple steps
  - Manages application-level validation beyond simple schema validation
- **Why it matters**: This layer embodies the core business logic independent of API protocols or data access methods. It ensures that business rules remain central and aren't scattered across the codebase.

#### 3. Repository Layer (`/repositories/`)
- **Primary Purpose**: Abstracts data access patterns from the business logic
- **Key Responsibilities**:
  - Provides a domain-friendly interface for data operations
  - Hides the details of database queries and ORM operations
  - Encapsulates complex query logic for specific use cases
  - Handles data transformation between ORM models and domain entities
  - Manages transaction boundaries for data operations
- **Why it matters**: This layer decouples business logic from specific database technologies, making the system more testable and allowing the data access approach to evolve independently from business logic.

#### 4. Data Layer (`/database/`)
- **Primary Purpose**: Manages database connectivity and data structure definitions
- **Key Responsibilities**:
  - Defines ORM models that map to database tables
  - Manages database connection pools and sessions
  - Provides database migrations for schema evolution
  - Implements database-specific optimizations (indices, constraints)
  - Handles low-level data access operations
- **Why it matters**: This layer isolates database-specific concerns, allowing the system to potentially switch database technologies with minimal impact on upper layers.

### Layer Interactions and Data Flow

#### Request Flow (From Client to Database)

1. **Client Request → API Layer**
   - An HTTP request arrives at a FastAPI endpoint
   - The API layer validates request parameters and body using Pydantic schemas
   - Dependencies like authentication and database session are injected

2. **API Layer → Service Layer**
   - The validated data is passed to the appropriate service
   - For simple CRUD operations, API may bypass services and go directly to repositories

3. **Service Layer → Repository Layer**
   - The service orchestrates one or more repository operations
   - It applies business rules and transforms data as needed
   - Service methods are transaction-oriented, representing complete business operations

4. **Repository Layer → Data Layer**
   - The repository translates domain operations into database operations
   - It constructs SQL queries using SQLAlchemy and executes them
   - It converts ORM model instances to domain entities where needed

5. **Data Layer → Database**
   - SQLAlchemy ORM models define the structure of database tables
   - Database connectivity and session management is handled here
   - Actual SQL execution occurs

#### Response Flow (From Database to Client)

1. **Database → Data Layer**
   - Query results are returned as ORM model instances
   - Any lazy-loading relationships are resolved

2. **Data Layer → Repository Layer**
   - ORM model instances are collected and processed
   - Any necessary data transformations occur

3. **Repository Layer → Service Layer**
   - Repository returns domain-friendly data to the service
   - Repository handles any database-specific exceptions

4. **Service Layer → API Layer**
   - Service applies additional business logic or transformations
   - Returns domain objects or processed data to API layer

5. **API Layer → Client**
   - API converts domain objects to response schemas
   - Response is formatted according to API conventions (JSON, etc.)
   - HTTP status codes and headers are applied
   - Response is sent to client

### Communication Patterns and Dependencies

#### Dependency Direction
- Dependencies flow inward: API → Services → Repositories → Data
- Inner layers have no knowledge of outer layers
- This enforces Clean Architecture's Dependency Rule: source code dependencies only point inward

#### Dependency Injection
- FastAPI's dependency injection system is used throughout
- Database sessions are injected into repositories via endpoints
- Repositories are injected into services
- Services are injected into API handlers

#### Error Propagation
- Errors bubble up through the layers
- Database-specific errors are caught in repositories and translated to domain exceptions
- Domain exceptions are caught in API layer and translated to HTTP responses
- This ensures clean separation of error handling responsibilities

#### Cross-Cutting Concerns
- Logging happens at every layer, but with appropriate level of detail
- Authentication & authorization are primarily handled at the API layer
- Transactions span multiple layers but are typically controlled by services

### Specific Implementation Examples

#### Example: Adding a New Source (Command Operation)
1. **API Layer**: Endpoint `/api/v1/commands/sources` receives POST request with source data
2. **Service Layer**: `SourceService.create_source()` performs validation and coordinates operations
3. **Repository Layer**: `SourceRepository.create()` handles database operations
4. **Data Layer**: ORM models are created and persisted

#### Example: Searching Sources (Query Operation)
1. **API Layer**: Endpoint `/api/v1/queries/search` receives search parameters
2. **Service Layer**: (Optional) `SearchService` may coordinate complex searches
3. **Repository Layer**: `SearchRepository.search()` translates search params to query
4. **Data Layer**: Query is executed and ORM models are returned

## Directory Structure Explained

```
/backend/
├── main.py                        # FastAPI app entry point (initializes app, middleware, routers)
├── requirements.txt               # Project dependencies 
├── Dockerfile                     # Container definition for production deployment
├── pytest.ini                     # PyTest configuration for running tests
│
├── /core/                         # Core application components
│   ├── config.py                  # Environment-based configuration via Pydantic
│   ├── exceptions.py              # Custom exception classes and global handlers
│   └── logging_config.py          # Loguru logging setup with structured logging
│
├── /api/                          # API endpoints organized by version and CQRS
│   ├── router.py                  # Main router that aggregates all API versions
│   └── /v1/                       # Version 1 API endpoints
│       ├── /commands/             # Write operations (POST/PUT/DELETE)
│       │   ├── sources.py         # Source creation/update/delete endpoints
│       │   ├── photometry.py      # Photometry data management endpoints
│       │   ├── redshift.py        # Redshift measurement management endpoints
│       │   └── classification.py  # Classification data management endpoints
│       └── /queries/              # Read operations (GET)
│           ├── sources.py         # Source retrieval endpoints
│           ├── photometry.py      # Photometry data retrieval endpoints
│           ├── redshift.py        # Redshift measurement retrieval endpoints
│           ├── classification.py  # Classification data retrieval endpoints
│           └── search.py          # Complex search and filtering endpoints
│
├── /schemas/                      # Pydantic data validation schemas
│   ├── base.py                    # Base schemas and common response models
│   ├── source.py                  # Source-related schemas (creation, update, response)
│   ├── photometry.py              # Photometry data schemas
│   ├── redshift.py                # Redshift measurement schemas
│   ├── classification.py          # Classification data schemas
│   ├── query.py                   # Search query and filter schemas
│   └── responses.py               # Standardized API response models
│
├── /repositories/                 # Data access layer with Repository pattern
│   ├── base.py                    # Abstract base repository with generic CRUD operations
│   ├── source_repository.py       # Source-specific data access methods
│   ├── photometry_repository.py   # Photometry data access methods
│   ├── redshift_repository.py     # Redshift measurement data access methods
│   ├── classification_repository.py # Classification data access methods
│   └── search_repository.py       # Complex search query execution
│
├── /services/                     # Business logic and orchestration layer
│   ├── export_service.py          # Data export functionality (CSV, VOTable)
│   └── validation_service.py      # Domain validation rules and cross-entity validation
│
├── /database/                     # Database configuration and ORM models
│   ├── connection.py              # Async database connection setup
│   ├── models.py                  # SQLAlchemy ORM model definitions
│   └── /migrations/               # Database schema migrations (when added)
│
├── /tests/                        # Test suite organized by component
│   ├── conftest.py                # Shared test fixtures and configuration
│   ├── /api/                      # API endpoint tests
│   ├── /repositories/             # Repository tests with mock databases
│   ├── /services/                 # Service layer tests
│   └── /database/                 # Database model and migration tests
│
└── /logs/                         # Runtime logs directory (auto-created)
    └── backend.log                # Application logs with rotation
```

## Key Components Detailed

### Database Models

The database schema represents astrophysical data with these core entities:

- **SourceAGN**: Central entity representing an astronomical source with coordinates
  - Primary attributes: `agn_id`, `ra` (Right Ascension), `declination`
  - Relationships: One-to-many with Photometry, RedshiftMeasurement, and Classification
  
- **Photometry**: Brightness measurements across different wavelength bands
  - Primary attributes: `phot_id`, `band_label`, `filter_name`, `mag_value`, `mag_error`
  - Foreign key: `agn_id` linking to SourceAGN
  
- **RedshiftMeasurement**: Distance/velocity measurements of sources
  - Primary attributes: `redshift_id`, `redshift_type`, `z_value`, `z_error`
  - Foreign key: `agn_id` linking to SourceAGN
  
- **Classification**: Categorization of sources by different characteristics
  - Primary attributes: `class_id`, various classification types (`spec_class`, `xray_class`, etc.)
  - Foreign key: `agn_id` linking to SourceAGN

All models include metadata like `created_at` and `updated_at` timestamps.

### Repositories

Repositories implement the data access pattern with a consistent interface:

- **BaseRepository**: Generic implementation of CRUD operations
  - Type parameterized for different models and schemas
  - Implements: `create`, `get`, `get_multi`, `update`, `delete`, etc.
  
- **Domain-specific repositories**: Extend BaseRepository with specialized methods
  - **SourceRepository**: Methods like `get_by_coordinates`, `get_nearest_sources`
  - **PhotometryRepository**: Methods for band filtering, magnitude ranges
  - **RedshiftRepository**: Methods for redshift ranges, type filtering
  - **ClassificationRepository**: Methods for class distribution, classification filtering
  - **SearchRepository**: Complex cross-entity search functionality

All repositories use async SQLAlchemy for non-blocking database operations.

### API Endpoints

API endpoints are organized by CQRS and versioning:

#### Command Endpoints (Write Operations)
- `/api/v1/sources`: Create, update, delete source records
- `/api/v1/photometry`: Add, update, delete photometric measurements
- `/api/v1/redshift`: Add, update, delete redshift measurements
- `/api/v1/classification`: Add, update, delete classification data

#### Query Endpoints (Read Operations)
- `/api/v1/sources`: Get sources by ID, coordinates, filters
- `/api/v1/photometry`: Get photometry by filters, bands, magnitude ranges
- `/api/v1/redshift`: Get redshifts by type, value ranges, source ID
- `/api/v1/classification`: Get classifications by types, distributions
- `/api/v1/search`: Complex multi-entity search with filtering

All endpoints include:
- Comprehensive validation via Pydantic schemas
- Structured error handling and consistent responses
- Detailed API documentation via OpenAPI/Swagger

### Services

Services implement business logic that spans multiple repositories or requires orchestration:

- **ExportService**: Handles data export in various formats
  - CSV generation for tabular data
  - VOTable generation for VO-compatible applications
  - Streaming response support for large datasets
  
- **ValidationService**: Cross-entity validation logic
  - Domain-specific validation rules
  - Data integrity checks across related entities

## Authentication and Security (TODO)

Authentication is implemented through:
- Environment-configured authentication providers
- JWT-based authentication
- Role-based access control for administrative operations
- API key options for programmatic access

## Error Handling

Comprehensive error handling through:
- Custom exception classes mapped to HTTP response codes
- Global exception handlers for consistent response formats
- Detailed error logging with context information
- Graceful degradation patterns

## Logging

Structured logging is implemented with Loguru:
- Console logging for development
- File logging with rotation for production
- JSON-formatted logs for easy parsing
- Context-enhanced logging with correlation IDs
- Log level configuration via environment variables

## Development Workflow

### Setting Up Development Environment

1. **Clone repository and navigate to backend directory**

2. **Create a virtual environment**:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

4. **Configure local environment**:
   ```
   cp .env.example .env
   # Edit .env with your local database settings
   ```

5. **Run development server with auto-reload**:
   ```
   uvicorn main:app --reload
   ```

6. **Access API documentation**:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Development Guidelines

#### Coding Standards

- Follow PEP 8 standards for Python code style
- Use Google-style docstrings for function and class documentation
- Apply type hints consistently throughout the codebase
- Maintain test coverage for all new code

#### Adding New Features

1. **Create new model** in `database/models.py` if needed
2. **Define schemas** in the `schemas/` directory
3. **Implement repository** in the `repositories/` directory
4. **Add service methods** if business logic is required
5. **Create API endpoints** in appropriate CQRS module
6. **Write tests** for all new components

#### Running Tests

Run the entire test suite:
```
pytest
```

Run specific test categories:
```
pytest tests/api/        # API tests only
pytest tests/repository/ # Repository tests only
```

Run with coverage report:
```
pytest --cov=. tests/
```

## Docker Deployment

Build and run with Docker:

```
docker build -t agndb-backend .
docker run -p 8000:8000 --env-file .env agndb-backend
```

## Performance Considerations

- **Database Indexing**: Critical fields are indexed in models
- **Query Optimization**: Repositories implement specialized query methods
- **Pagination**: All multi-record endpoints support pagination
- **Async Operations**: Non-blocking I/O for database and external services
- **Connection Pooling**: Database connection pooling for efficient resource use

## Data Management

### Import Workflows

Bulk data imports are handled through:
- Specialized command endpoints with validation
- Background tasks for large dataset processing
- Transaction management for data integrity

### Export Options

Data export is supported in multiple formats:
- CSV for general use
- VOTable for astronomical applications
- JSON for API consumers
- Streaming responses for large datasets

## Future Enhancements (TODO--discussion neccessary)

Planned architectural enhancements include:
- Alembic integration for database migrations
- Redis caching for frequently accessed data
- Background worker processes for long-running tasks
- Virtual Observatory protocol implementation
- GraphQL API option for flexible querying 