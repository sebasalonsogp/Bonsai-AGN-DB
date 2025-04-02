# AGN-DB

A React-based web application for managing and querying AGN (Active Galactic Nuclei) data, featuring team information, search tools, and catalog metadata.

## Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Key Dependencies](#key-dependencies)
- [Routing Setup](#routing-setup)
- [Setup Instructions](#setup-instructions)
- [Security Notes](#security-notes)
- [Styling](#styling)
- [Data Flow](#data-flow)
- [Image Handling](#image-handling)

## Features
- **Home Page**: Landing page with a central image
- **Search**: Password-protected query builder with react-querybuilder
- **People**: Responsive grid displaying team members (students/professors)
- **Information**: Tabbed interface for database metadata and catalog references
- **Responsive Layout**: Consistent navigation across all pages

## Project Structure
```
front-end/
├── src/
│   ├── components/
│   │   ├── Hero.jsx         # Hero section component
│   │   ├── layout.jsx       # Main layout with header/footer and routing logic
│   │   ├── Navbar.jsx       # Navigation bar component
│   │   ├── NavButton.jsx    # Navigation button component
│   │   ├── QuerySearch.jsx  # Interactive query builder using react-querybuilder
│   │   └── peoplegrid.jsx   # Displays team members in a responsive grid
│   ├── pages/
│   │   ├── Home.jsx         # Landing page with title and image
│   │   ├── Search.jsx       # Password-protected page for query access
│   │   ├── People.jsx       # Wrapper for <PeopleGrid />
│   │   └── Information.jsx  # Tabbed metadata tables for database columns and catalog references
│   ├── App.jsx              # Main application router
│   ├── App.css              # Main application styles
│   ├── index.css            # Global styles
│   └── main.jsx             # Application entry point
├── public/                  # Static assets
├── index.html              # HTML entry point
├── package.json            # Project dependencies and scripts
├── vite.config.js          # Vite configuration
└── eslint.config.js        # ESLint configuration
```

| File               | Description                                                                 |
|--------------------|-----------------------------------------------------------------------------|
| `Hero.jsx`         | Hero section component with main content display                             |
| `layout.jsx`       | Main layout with header/footer and routing logic                            |
| `Navbar.jsx`       | Navigation bar component with responsive design                             |
| `NavButton.jsx`    | Reusable navigation button with active state styling                       |
| `peoplegrid.jsx`   | Displays team members in a responsive grid                                  |
| `QuerySearch.jsx`  | Interactive query builder using `react-querybuilder`                       |
| `Home.jsx`         | Landing page with title and image                                           |
| `Search.jsx`       | Password-protected page for query access (frontend validation only)         |
| `People.jsx`       | Wrapper for `<PeopleGrid />`                                               |
| `Information.jsx`  | Tabbed metadata tables for database columns and catalog references         |

---

## Key Dependencies
- **Routing**: `react-router-dom`
- **UI Components**: 
  - `react-tabs` (for tabbed interfaces)
  - `react-querybuilder` (for search queries)
- **Styling**: Tailwind CSS
- **Data**: Static arrays for team members (`students`, `professors`) and catalog metadata.

---

## Setup
1. Clone the repository.
2. Install dependencies:
   ```bash
   npm i
3. Run the app:
```bash
    npm run dev
```
## Security Notes
⚠️ Warning: The password validation in Search.jsx is a frontend-only placeholder. For production use:

- Implement backend authentication.

- Avoid hardcoding credentials in the client.

## Styling
- Built with Tailwind CSS utility classes.

- Responsive grids (grid-cols-1 sm:grid-cols-2...).

- Conditional active state styling for navigation buttons.

- Alternating row colors in tables (odd:bg-white even:bg-gray-100).

## Data Flow
- **Routing**: Managed by layout.jsx using \<Outlet />.

- **Dynamic Content:**

    - PeopleGrid renders data from static students and professors arrays.

    - Information.jsx uses variables and references arrays for metadata.

- **State Management:**

    - QuerySearch.jsx locally manages query state with useState.

## Image Handling
- Team Photos: Imported directly in peoplegrid.jsx from /photos/.

```jsx
import Jef from '/photos/JeffersonBoyd.jpg?url';
```
