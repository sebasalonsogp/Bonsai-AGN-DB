# AGN-DB: Astrophysical Active Galactic Nuclei Database

## Table of Contents

- [AGN-DB: Astrophysical Active Galactic Nuclei Database](#agn-db-astrophysical-active-galactic-nuclei-database)
  - [Table of Contents](#table-of-contents)
  - [Project Overview](#project-overview)
    - [Purpose and Scope](#purpose-and-scope)
    - [Domain Context](#domain-context)
    - [Key Features](#key-features)
  - [Architecture](#architecture)
    - [System Design](#system-design)
    - [Design Patterns](#design-patterns)
    - [Technology Stack](#technology-stack)
      - [Backend](#backend)
      - [Frontend](#frontend)
      - [Database \& Infrastructure](#database--infrastructure)
  - [Project Structure](#project-structure)
    - [Directory Organization](#directory-organization)
    - [Key Components](#key-components)
      - [Frontend](#frontend-1)
      - [Backend](#backend-1)
      - [Database](#database)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Development Environment Setup](#development-environment-setup)
    - [Production Deployment](#production-deployment)
    - [Environment Variables](#environment-variables)
      - [Database Container](#database-container)
      - [Backend Container](#backend-container)
      - [Frontend Container](#frontend-container)
  - [Backend Documentation](#backend-documentation)
    - [API Structure](#api-structure)
    - [Data Models](#data-models)
      - [Entity Models (SQLAlchemy)](#entity-models-sqlalchemy)
      - [Schema Models (Pydantic)](#schema-models-pydantic)
    - [Clean Architecture Implementation](#clean-architecture-implementation)
    - [Logging System](#logging-system)
    - [Error Handling](#error-handling)
  - [Frontend Documentation](#frontend-documentation)
    - [Component Structure](#component-structure)
    - [State Management](#state-management)
    - [Routing](#routing)
    - [Query Builder](#query-builder)
  - [Database Schema](#database-schema)
    - [Entity Relationship Diagram](#entity-relationship-diagram)
    - [Table Descriptions](#table-descriptions)
      - [source\_agn](#source_agn)
      - [photometry](#photometry)
      - [redshift\_measurement](#redshift_measurement)
      - [classification](#classification)
    - [Indexing Strategy](#indexing-strategy)
  - [API Reference](#api-reference)
    - [Endpoints Overview](#endpoints-overview)
      - [Health and Information](#health-and-information)
      - [Search and Queries](#search-and-queries)
      - [Source Operations](#source-operations)
    - [Authentication](#authentication)
    - [Query Structure](#query-structure)
    - [Response Formats](#response-formats)
  - [Development Workflow](#development-workflow)
    - [Code Standards](#code-standards)
    - [Testing](#testing)
    - [CI/CD](#cicd)
  - [Troubleshooting and FAQs](#troubleshooting-and-faqs)
    - [Common Issues](#common-issues)
    - [Frequently Asked Questions](#frequently-asked-questions)
  - [Contribution Guidelines](#contribution-guidelines)
  - [License](#license)
  - [Acknowledgements](#acknowledgements)

## Project Overview

### Purpose and Scope

AGN-DB is a comprehensive web application designed for astrophysics researchers to explore, analyze, and export data related to Active Galactic Nuclei (AGN). The system provides a user-friendly interface for complex queries on a large astronomical dataset, supporting scientific research in the field of astrophysics.

### Domain Context

**Active Galactic Nuclei (AGN)** are compact regions at the center of galaxies that exhibit much higher than normal luminosity across the electromagnetic spectrum. This project provides a database and tools for working with AGN observations including:

- **Source coordinates**: Right Ascension (RA) and Declination (DEC) positioning in the sky
- **Photometric data**: Light measurements across different wavelength bands and filters
- **Redshift measurements**: Important for determining distance and recessional velocity
- **Classification schemes**: Different ways AGNs are categorized based on observational characteristics

### Key Features

- **Advanced Search Functionality**: Complex query builder interface for filtering AGN sources
- **Data Visualization**: Interactive tables for reviewing and understanding astronomical data
- **Export Capabilities**: Download data in multiple formats (CSV, VOTable) for analysis in external tools
- **Scientific Metadata**: Comprehensive information about data sources and measurement techniques
- **Asynchronous Architecture**: Fast, non-blocking backend operations for handling millions of records
- **Comprehensive Logging**: Detailed activity tracking for debugging and audit purposes

## Architecture

### System Design

AGN-DB follows a modern containerized microservices architecture with three main components:

1. **Frontend**: React-based SPA with responsive UI components
2. **Backend API**: FastAPI-powered async REST API implementing Clean Architecture with Repository Pattern & CQRS-lite (evolutionary adoption)
3. **Database**: MariaDB optimized for astronomical data storage and retrieval

The system is designed to handle large datasets efficiently while providing a responsive user experience.

### Design Patterns

The project implements several architecture and design patterns:

- **Clean Architecture**: Separation of concerns with distinct layers for business logic, data access, and presentation
- **Repository Pattern**: Abstraction over database access operations
- **CQRS-lite**: Separation of read operations (Queries) and write operations (Commands)
- **Dependency Injection**: For loose coupling and better testability
- **Unit of Work**: Transaction management through session handling

### Technology Stack

#### Backend
- **FastAPI**: Modern, high-performance async Python web framework
- **SQLAlchemy**: ORM with async support for database operations
- **Pydantic**: Data validation and settings management
- **Loguru**: Structured logging with rotation support
- **Asyncmy**: Async MySQL/MariaDB driver
- **Pytest**: Testing framework

#### Frontend
- **React**: Component-based UI library
- **React Router**: Client-side routing
- **React Query Builder**: Visual query construction
- **Tailwind CSS**: Utility-first CSS framework
- **Vite**: Fast build tool and development server

#### Database & Infrastructure
- **MariaDB**: Relational database optimized for high-performance queries
- **Docker**: Containerization for consistent development and deployment
- **Docker Compose**: Multi-container application orchestration
- **Nginx**: Web server for frontend static files (production)

## Project Structure

### Directory Organization

```
/
├── frontend/            # React frontend application
├── backend/             # FastAPI backend application
├── database/            # Database setup and sample data
├── docker-compose.yml   # Production Docker configuration
└── docker-compose.dev.yml # Development Docker configuration
```

### Key Components

#### Frontend
```
frontend/
├── src/                # Source code
│   ├── components/     # Reusable UI components
│   ├── pages/          # Page components for routing
│   ├── services/       # API interaction logic
│   ├── hooks/          # Custom React hooks
│   ├── utils/          # Utility functions
│   └── App.jsx         # Application entry point
├── public/             # Static assets
├── Dockerfile          # Production container configuration
├── nginx.conf          # Nginx configuration for production
└── package.json        # Dependencies and scripts
```

#### Backend
```
backend/
├── main.py             # Application entry point
├── api/                # API routes (versioned)
│   ├── v1/
│       ├── commands/   # Write operations endpoints
│       └── queries/    # Read operations endpoints
├── core/               # Core configuration
│   ├── config.py       # Application settings
│   ├── exceptions.py   # Custom exception handling
│   └── logging_config.py # Logging setup
├── database/           # Database connectivity
│   ├── connection.py   # Async DB connection management
│   └── models.py       # SQLAlchemy ORM models
├── repositories/       # Data access layer
│   ├── base.py         # Generic repository implementation
│   └── [entity]_repository.py # Entity-specific repositories
├── schemas/            # Data validation models
│   └── [entity].py     # Pydantic models for each entity
├── services/           # Business logic
└── tests/              # Unit and integration tests
```

#### Database
```
database/
├── scripts/
│   ├── 00_init_wrapper.sh     # Initialization script
│   ├── 01_schema.sql          # Database schema definition
│   ├── 02_sample_data.sql     # Basic sample data
│   └── 03_generate_data.py    # Python script for generating larger datasets
├── Dockerfile                 # Database container configuration
└── README.md                  # Database-specific documentation
```

## Getting Started

### Prerequisites

To set up and run AGN-DB, you'll need:

- **Docker** (20.10+) and **Docker Compose** (v2+)
- **Git** for version control
- Web browser (Chrome, Firefox, Safari, or Edge)

For local development without Docker:
- **Node.js** (v18+) and **npm** (v8+) for frontend
- **Python** (v3.9+) for backend
- **MariaDB** (v10.5+) for database

### Development Environment Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/agn-db.git
   cd agn-db
   ```

2. **Start the development environment using Docker Compose**
   ```bash
   docker-compose -f docker-compose.dev.yml up -d
   ```

   This will start three containers with hot-reloading:
   - `agndb-database-dev`: MariaDB instance on port 3307
   - `agndb-backend-dev`: FastAPI server on port 8000
   - `agndb-frontend-dev`: Vite dev server on port 5173

3. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

4. **View logs**
   ```bash
   # View all logs
   docker-compose -f docker-compose.dev.yml logs -f
   
   # View logs for a specific service
   docker-compose -f docker-compose.dev.yml logs -f backend
   ```

5. **Stop the development environment**
   ```bash
   docker-compose -f docker-compose.dev.yml down
   ```

### Production Deployment

1. **Deploy using production Docker Compose configuration**
   ```bash
   docker-compose up -d
   ```

   This will start three containers:
   - `agndb-database`: MariaDB instance on port 3306
   - `agndb-backend`: FastAPI server on port 8000
   - `agndb-frontend`: Nginx serving static files on port 80

2. **Access the application**
   - Frontend: http://localhost
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Environment Variables

The application uses several environment variables for configuration:

#### Database Container
- `MYSQL_ROOT_PASSWORD`: Root password for MariaDB
- `MYSQL_DATABASE`: Database name (default: "agndb")
- `MYSQL_USER`: Database user (default: "agndb_user")
- `MYSQL_PASSWORD`: Database user password
- `GENERATE_LARGE_DATASET`: When "true", generates ~5000 sample records

#### Backend Container
- `ENVIRONMENT`: "development" or "production"
- `DEBUG`: "true" or "false"
- `DB_HOST`: Database hostname
- `DB_PORT`: Database port
- `DB_USER`: Database username
- `DB_PASSWORD`: Database password
- `DB_NAME`: Database name
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

#### Frontend Container
- `VITE_API_URL`: Backend API URL (development mode only)

## Backend Documentation

### API Structure

The backend follows a versioned API structure with a clear separation between query (read) and command (write) operations:

- `/api/v1/queries/*`: Endpoints for retrieving data
- `/api/v1/commands/*`: Endpoints for creating, updating, and deleting data

The API includes these key endpoints:

- **Search API**: `/api/v1/queries/search/` - Complex search functionality
- **Export API**: `/api/v1/queries/search/export` - Data export in various formats
- **Field Metadata**: `/api/v1/queries/search/available-fields` - Dynamic field information
- **CRUD Operations**: Entity-specific endpoints for each data type

### Data Models

#### Entity Models (SQLAlchemy)

The application uses these primary database models:

1. **SourceAGN**: Central entity representing an astronomical source
   - `agn_id`: Primary key
   - `ra`: Right Ascension coordinates (0-360 degrees)
   - `declination`: Declination coordinates (-90 to +90 degrees)
   - Plus timestamps and relationships

2. **Photometry**: Light measurements for sources
   - `phot_id`: Primary key
   - `agn_id`: Foreign key to SourceAGN
   - `band_label`: Observational band (e.g., 'optical', 'radio')
   - `filter_name`: Specific filter used
   - `mag_value`: Magnitude (brightness) value
   - `mag_error`: Measurement error
   - `extinction`: Extinction correction value

3. **RedshiftMeasurement**: Distance/velocity indicators
   - `redshift_id`: Primary key
   - `agn_id`: Foreign key to SourceAGN
   - `redshift_type`: Measurement method
   - `z_value`: Redshift value
   - `z_error`: Measurement error

4. **Classification**: Categorization data
   - `class_id`: Primary key
   - `agn_id`: Foreign key to SourceAGN
   - Multiple classification fields (spec_class, gen_class, etc.)

#### Schema Models (Pydantic)

The API uses Pydantic models for validation and serialization:

- **Request Models**: Validate incoming data
- **Response Models**: Standardize API responses
- **Internal Models**: Support service and repository operations

### Clean Architecture Implementation

The backend follows Clean Architecture principles with distinct layers:

1. **Domain Layer**: Core business logic and entities
   - SQLAlchemy models
   - Domain-specific exceptions

2. **Application Layer**: Orchestration and use cases
   - Service components handling business operations
   - Exception management

3. **Interface Adapters**: Bridges between layers
   - Repositories abstraction over data access
   - API routes defining endpoints

4. **Frameworks & Drivers**: External components
   - Database connections
   - FastAPI web framework
   - Logging system

### Logging System

The application uses Loguru for advanced logging with:

- **Multiple output formats**: Human-readable or structured JSON
- **Log rotation**: Size or time-based file rotation
- **Retention policies**: Automatic cleanup of old log files
- **Contextual logging**: Enhanced debugging with contextual data
- **Exception tracking**: Full traceback capture and error reporting

Logs are organized into several severity levels (TRACE, DEBUG, INFO, SUCCESS, WARNING, ERROR, CRITICAL) and stored at `backend/logs/backend.log`.

### Error Handling

The API implements consistent error handling using:

1. **Custom Exception Classes**:
   - `AGNDBException`: Base exception class
   - `NotFoundException`: For missing resources (404)
   - `ValidationException`: For validation errors (422)
   - `DatabaseException`: For database operation failures (500)

2. **Global Exception Handlers**:
   - Standardized error response format
   - Detailed error information for debugging
   - Protection against information leakage in production

3. **Response Structure**:
   - Consistent error response format with status code, message, and details
   - Structured validation error information

## Frontend Documentation

### Component Structure

The frontend follows a component-based architecture with:

1. **Layout Components**:
   - `Layout`: Main application wrapper with navigation
   - `Navbar`: Navigation component
   - `NavButton`: Reusable navigation button

2. **Page Components**:
   - `Home`: Landing page
   - `Search`: Search interface with query builder
   - `Information`: Metadata about database structure
   - `People`: Team information

3. **Feature Components**:
   - `QuerySearch`: Complex query builder
   - `PeopleGrid`: Team member display
   - `Hero`: Hero section for landing page

### State Management

The application uses React's built-in state management with:

- **Local Component State**: For UI state using `useState`
- **Context API**: For shared state across components
- **Custom Hooks**: For reusable stateful logic

### Routing

Routing is handled using React Router with:

- **Route definitions**: In `App.jsx`
- **Layout-based routing**: Using nested routes and outlets
- **Active route tracking**: For navigation highlighting

### Query Builder

The search interface is powered by `react-querybuilder` with:

1. **Dynamic Field Selection**: Fields from backend metadata
2. **Operator Support**: Comparison, text, and logical operators
3. **Group Support**: AND/OR condition groups
4. **JSON Query Generation**: Creates structured query for the backend

## Database Schema (W.I.P)

### Entity Relationship Diagram (W.I.P)

```
┌─────────────┐       ┌────────────────┐
│  source_agn │       │   photometry   │
├─────────────┤       ├────────────────┤
│ agn_id (PK) │◄──┐   │ phot_id (PK)   │
│ ra          │   │   │ agn_id (FK)    │
│ declination │   └───┤ band_label     │
│ created_at  │       │ filter_name    │
│ updated_at  │       │ mag_value      │
└─────────────┘       │ mag_error      │
        ▲             │ extinction     │
        │             │ created_at     │
        │             │ updated_at     │
        │             └────────────────┘
        │
        │             ┌─────────────────────┐
        │             │ redshift_measurement │
        │             ├─────────────────────┤
        │             │ redshift_id (PK)    │
        └─────────────┤ agn_id (FK)         │
        │             │ redshift_type       │
        │             │ z_value             │
        │             │ z_error             │
        │             │ created_at          │
        │             │ updated_at          │
        │             └─────────────────────┘
        │
        │             ┌─────────────────┐
        │             │ classification  │
        │             ├─────────────────┤
        │             │ class_id (PK)   │
        └─────────────┤ agn_id (FK)     │
                      │ spec_class      │
                      │ gen_class       │
                      │ xray_class      │
                      │ best_class      │
                      │ image_class     │
                      │ sed_class       │
                      │ created_at      │
                      │ updated_at      │
                      └─────────────────┘
```

### Table Descriptions

#### source_agn
The central table containing basic information about Active Galactic Nuclei sources.

| Column | Type | Description |
|--------|------|-------------|
| agn_id | INT | Primary key with auto-increment |
| ra | DOUBLE | Right ascension in degrees (0-360) |
| declination | DOUBLE | Declination in degrees (-90 to +90) |
| created_at | TIMESTAMP | Record creation time |
| updated_at | TIMESTAMP | Record update time |

#### photometry
Stores brightness measurements across different wavelength bands.

| Column | Type | Description |
|--------|------|-------------|
| phot_id | INT | Primary key with auto-increment |
| agn_id | INT | Foreign key to source_agn |
| band_label | VARCHAR(50) | Observational band (e.g., 'optical', 'radio') |
| filter_name | VARCHAR(100) | Specific filter used (e.g., 'SDSS-g') |
| mag_value | DOUBLE | Magnitude (brightness) value |
| mag_error | DOUBLE | Measurement error margin |
| extinction | DOUBLE | Extinction correction value |
| created_at | TIMESTAMP | Record creation time |
| updated_at | TIMESTAMP | Record update time |

#### redshift_measurement
Contains redshift measurements critical for determining distance and velocity.

| Column | Type | Description |
|--------|------|-------------|
| redshift_id | INT | Primary key with auto-increment |
| agn_id | INT | Foreign key to source_agn |
| redshift_type | VARCHAR(50) | Measurement method (e.g., 'spectroscopic') |
| z_value | DOUBLE | Redshift value |
| z_error | DOUBLE | Measurement error margin |
| created_at | TIMESTAMP | Record creation time |
| updated_at | TIMESTAMP | Record update time |

#### classification
Stores various classification schemes for AGN sources.

| Column | Type | Description |
|--------|------|-------------|
| class_id | INT | Primary key with auto-increment |
| agn_id | INT | Foreign key to source_agn |
| spec_class | VARCHAR(50) | Spectroscopic classification |
| gen_class | VARCHAR(50) | General classification |
| xray_class | VARCHAR(50) | X-ray based classification |
| best_class | VARCHAR(50) | Best/consensus classification |
| image_class | VARCHAR(50) | Morphological classification |
| sed_class | VARCHAR(50) | Spectral energy distribution classification |
| created_at | TIMESTAMP | Record creation time |
| updated_at | TIMESTAMP | Record update time |

### Indexing Strategy

The database uses a targeted indexing strategy to optimize query performance:

1. **Primary Keys**: All tables have auto-incrementing primary keys
2. **Foreign Keys**: All relationships are indexed for join performance
3. **Search Fields**:
   - `ra` and `declination` in `source_agn` for spatial queries
   - `band_label` and `filter_name` in `photometry` for filtered queries
   - `z_value` in `redshift_measurement` for range queries
   - `best_class` in `classification` for type filtering

4. **Cascading Deletes**: All foreign keys use CASCADE to maintain referential integrity

## API Reference

### Endpoints Overview

#### Health and Information
- `GET /`: Basic API information
- `GET /health`: Health check endpoint

#### Search and Queries
- `POST /api/v1/queries/search/`: Execute complex search query
- `POST /api/v1/queries/search/export`: Export search results
- `GET /api/v1/queries/search/available-fields`: Get field metadata

#### Source Operations
- `GET /api/v1/queries/sources/{agn_id}`: Get source by ID
- `GET /api/v1/queries/sources/`: List sources with pagination
- `POST /api/v1/commands/sources/`: Create new source
- `PUT /api/v1/commands/sources/{agn_id}`: Update source
- `DELETE /api/v1/commands/sources/{agn_id}`: Delete source

Similar endpoints exist for photometry, redshift, and classification data.

### Authentication

*Note: The current version has minimal authentication. Production deployments should implement proper authentication.*

### Query Structure

The search endpoint accepts a JSON query structure:

```json
{
  "combinator": "and",
  "rules": [
    {
      "field": "ra",
      "operator": "<=",
      "value": "10"
    },
    {
      "field": "declination",
      "operator": ">",
      "value": "0"
    },
    {
      "combinator": "or",
      "rules": [
        {
          "field": "z_value",
          "operator": ">=",
          "value": "2.5"
        },
        {
          "field": "best_class",
          "operator": "equals",
          "value": "Quasar"
        }
      ]
    }
  ]
}
```

Supported operators include:
- Comparison: `equals`, `notEquals`, `greaterThan`, `lessThan`, etc.
- Text: `contains`, `beginsWith`, `endsWith`
- Null: `null`, `notNull`
- Lists: `in`, `notIn`

### Response Formats

Standard API responses follow this structure:

```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "pages": 10,
  "size": 10
}
```

Error responses follow:

```json
{
  "detail": "Error message",
  "status_code": 400,
  "errors": [
    {
      "loc": ["body", "query", "rules", 0, "field"],
      "msg": "Field 'unknown_field' does not exist",
      "type": "value_error"
    }
  ]
}
```

## Development Workflow

### Code Standards

The project follows these coding standards:

- **Python**: PEP 8 style guide
- **JavaScript/React**: ESLint and Prettier configuration
- **SQL**: Uppercase keywords, lowercase identifiers

### Testing

The backend includes a test suite using pytest:

```bash
# Run tests
docker-compose exec backend pytest

# Run tests with coverage
docker-compose exec backend pytest --cov=app
```

### CI/CD

[To be implemented]

## Troubleshooting and FAQs

### Common Issues

1. **Database Connection Failures**
   - Ensure the database container is running: `docker-compose ps`
   - Check database logs: `docker-compose logs database`
   - Verify environment variables in docker-compose.yml

2. **Backend API Not Responding**
   - Check backend logs: `docker-compose logs backend`
   - Ensure the database is accessible to the backend
   - Verify that the backend container started without errors

3. **Frontend Not Loading**
   - Check frontend logs: `docker-compose logs frontend`
   - Verify that the API URL is correctly set in the environment
   - Check browser console for JavaScript errors

### Frequently Asked Questions

1. **How do I add more sample data?**
   - You can either set `GENERATE_LARGE_DATASET=true` in the environment
   - Or run the data generation script manually:
     ```bash
     docker-compose exec database python3 /docker-entrypoint-initdb.d/03_generate_data.py
     ```

2. **How do I modify the database schema?**
   - Edit the `database/scripts/01_schema.sql` file
   - Update the corresponding SQLAlchemy models in `backend/database/models.py`
   - Rebuild the database container: `docker-compose up -d --build database`

3. **Can I run the project without Docker?**
   - Yes, see component-specific README files for instructions

## Contribution Guidelines

[To be added]

## License

[MIT License](LICENSE)

## Acknowledgements

This project is designed for educational and research purposes in astrophysics. It provides a platform for exploring and analyzing Active Galactic Nuclei data. 
