# AGN-DB Frontend

This document provides a detailed technical overview of the frontend architecture, implementation patterns, and developer guidelines for the Astrophysics AGN Database (AGN-DB) web application.

## Architectural Overview

The AGN-DB frontend is built using a modern React-based architecture with a focus on:

### Component-Based Architecture

The application follows a component-based architecture with:
- **Reusable UI Components**: Modular, self-contained components for consistent UI elements
- **Page Components**: Higher-level components that represent complete views
- **Layout Components**: Structure components that provide consistent page templates

This approach enables:
- ✅ Reusable UI elements across the application
- ✅ Clear separation of concerns
- ✅ Maintainable code structure
- ✅ Consistent user experience

### Services Pattern

The application uses a services pattern to handle API communication:
- **API Services**: Encapsulated in dedicated modules
- **Data Fetching**: Centralized request handling with error management

### Responsive Design

The UI is built with a mobile-first approach using:
- **Responsive Layouts**: Flex and grid-based responsive containers
- **Breakpoint-Based Styling**: Tailwind's responsive utility classes

## Architectural Layers and Their Interactions

### Layer Purposes and Responsibilities

#### 1. Page Layer (`/pages/`)
- **Primary Purpose**: Provides complete views representing distinct application routes
- **Key Responsibilities**:
  - Composes components to create full page views
  - Handles page-level state management
  - Connects to services for data retrieval
  - Implements route-specific logic
- **Why it matters**: This layer serves as the entry point for each route and orchestrates component composition

#### 2. Component Layer (`/components/`)
- **Primary Purpose**: Provides reusable UI building blocks
- **Key Responsibilities**:
  - Implements UI patterns consistently across the application
  - Manages component-specific state
  - Handles user interactions
  - Emits events to parent components
- **Why it matters**: This layer enables consistent UI patterns and simplifies maintenance through reuse

#### 3. Services Layer (`/services/`)
- **Primary Purpose**: Handles data fetching and API communication
- **Key Responsibilities**:
  - Provides API integration with the backend
  - Centralizes request/response handling
  - Manages errors and timeout scenarios
  - Formats data for component consumption
- **Why it matters**: This layer decouples the UI from data fetching concerns, creating a more maintainable codebase

#### 4. Assets & Static Resources
- **Primary Purpose**: Provides static resources for the application
- **Key Responsibilities**:
  - Stores images, icons, and other media
  - Provides global styles
  - Contains static data files when necessary
- **Why it matters**: Properly organized assets improve performance and maintainability

### Layer Interactions and Data Flow

#### Request Flow (User Interaction to Backend)

1. **User Interaction → Component Layer**
   - User interacts with a component (click, input, etc.)
   - Component triggers an event handler
   - Component may update local state

2. **Component Layer → Page Layer**
   - Component emits events to parent page
   - Page component processes the event
   - Page may update page-level state

3. **Page Layer → Services Layer**
   - Page calls appropriate service method
   - Service prepares the API request
   - Request is sent to the backend API

4. **Services Layer → Backend API**
   - Request is formatted according to API requirements
   - Authentication headers are added if needed
   - Request is sent and awaited

#### Response Flow (Backend to User Interface)

1. **Backend API → Services Layer**
   - Response is received from the backend
   - Service layer processes the response
   - Errors are handled appropriately
   - Data is transformed if necessary

2. **Services Layer → Page Layer**
   - Processed data is returned to the page component
   - Page updates its state with the new data
   - Error states are handled if necessary

3. **Page Layer → Component Layer**
   - Page passes updated data to child components
   - Components re-render with new data
   - UI reflects the updated state

### Communication Patterns

#### State Management
- **Component State**: For UI-specific state
- **Page State**: For view-level state
- **Context API**: For cross-component shared state (when needed)

#### Error Handling
- Centralized in the services layer
- Propagated up to UI components for display
- Consistent error messaging patterns

#### Loading States
- Managed at the page level
- Displayed using shared LoadingSpinner component
- Provides feedback during async operations

## Directory Structure Explained

```
/frontend/
├── index.html                     # HTML entry point
├── package.json                   # Project dependencies and scripts
├── vite.config.js                 # Vite bundler configuration
├── .env                           # Environment variables
├── Dockerfile                     # Container definition for production
├── nginx.conf                     # Nginx configuration for serving the app
│
├── /src/                          # Application source code
│   ├── main.jsx                   # Application entry point
│   ├── App.jsx                    # Main router configuration
│   ├── App.css                    # Global application styles
│   ├── index.css                  # Base styles and Tailwind imports
│   │
│   ├── /components/               # Reusable UI components
│   │   ├── Hero.jsx               # Hero section component
│   │   ├── Navbar.jsx             # Navigation bar component
│   │   ├── NavButton.jsx          # Navigation button component
│   │   ├── layout.jsx             # Main application layout
│   │   ├── LoadingSpinner.jsx     # Loading indicator component
│   │   ├── ErrorMessage.jsx       # Error display component
│   │   ├── peoplegrid.jsx         # Team members grid display
│   │   ├── QuerySearch.jsx        # Advanced search query builder
│   │   └── ExportDialog.jsx       # Data export dialog interface
│   │
│   ├── /pages/                    # Application page components
│   │   ├── Home.jsx               # Landing page
│   │   ├── Search.jsx             # Search interface page
│   │   ├── People.jsx             # Team members page
│   │   └── Information.jsx        # Database information page
│   │
│   ├── /services/                 # API and data services
│   │   └── api.js                 # API client with endpoints for backend communication
│   │
│   └── /tests/                    # Test configurations and specs
│
├── /public/                       # Static assets
│   └── /photos/                   # Team member photos and static images
│
└── /node_modules/                 # Dependencies (not in version control)
```

## Key Components Detailed

### Page Components

- **Home**: Landing page with hero section and introduction to the database
  - Simple layout showcasing the purpose of the application
  - Entry point for new users

- **Search**: Page container for the search functionality, including access control.
  - Presents a password prompt for access (placeholder mechanism).
  - Renders the `QuerySearch` component upon successful validation.
  - Does *not* contain the query builder logic itself.

- **People**: Team members showcase
  - Displays researchers and contributors in a responsive grid
  - Presents photos and role information

- **Information**: Database schema and reference information
  - Tabbed interface for different information categories
  - Presents metadata about available data and its structure
  - Provides reference documentation

### UI Components

- **Hero**: Configurable hero section with title and description
  - Used on the home page for the main visual
  - Adaptable for different content needs

- **Layout**: Page structure with consistent header and footer
  - Provides navigation through Navbar
  - Maintains consistent spacing and structure

- **QuerySearch**: Advanced query building interface
  - Complex component for constructing database queries
  - Integrates with react-querybuilder
  - Handles query validation and submission
  - Manages search results display

- **ExportDialog**: Data export interface
  - Allows selection of export format (CSV, VOTable)
  - Configures export parameters
  - Handles download process

### Service Layer

- **API Service**: Central handler for backend communication
  - Implements endpoints for all backend resources
  - Handles request/response processing
  - Manages errors and timeouts
  - Provides consistent interface for data operations

## Integration with Backend

The frontend integrates with the backend API through:

1. **API Client**: Structured services for different resource types
   - Source data
   - Photometry data
   - Redshift measurements
   - Classification data
   - Search functionality

2. **Data Flow**:
   - Query construction in UI
   - API requests through service layer
   - Response handling and display
   - Error management and user feedback

3. **Authentication**: (When implemented)
   - JWT token management
   - Secure API access
   - Protected routes

## Development Workflow

### Setting Up Development Environment

1. **Clone repository and navigate to frontend directory**

2. **Install dependencies**:
   ```
   npm install
   ```

3. **Configure local environment**:
   ```
   # Create .env file with:
   VITE_API_URL=http://localhost:8000/api/v1
   ```

4. **Run development server**:
   ```
   npm run dev
   ```

5. **Access the application**:
   - Dev server: http://localhost:5173

### Development Guidelines

#### Coding Standards

- Follow modern React practices (functional components, hooks)
- Use appropriate component composition patterns
- Implement proper prop validation
- Follow consistent naming conventions
- Implement proper error handling

#### Adding New Features

1. **Create new components** in the appropriate directory
2. **Add page component** if implementing a new route
3. **Update services** if new API endpoints are needed
4. **Add to router** in App.jsx if it's a new page
5. **Implement tests** for new functionality

#### Running Tests
(TODO--not complete)
```
npm test
```

## Docker Deployment

Build and run with Docker:

```
docker build -t agndb-frontend .
docker run -p 80:80 -e VITE_API_URL=http://backend-host/api/v1 agndb-frontend
```

## Performance Considerations

- **Pagination**: Search results and large datasets use pagination
- **Error Boundaries**: Prevent cascading failures in the UI

## Future Enhancements
(TODO--discussion neeeded)

Planned frontend enhancements include:
- Improved visualization of astronomical data
- Advanced filtering capabilities
- User account management (when backend supports it)
- Data submission interface for researchers
- Interactive data visualization tools
