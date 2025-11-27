---
inclusion: always
---

# Tech Stack

## Architecture

3-tier architecture:
- **Frontend**: React 18 SPA
- **Backend**: Node.js/Express REST API
- **Database**: SQLite

## Frontend Stack

- React 18.2 with functional components
- React Router DOM 6 for client-side routing
- Create React App (react-scripts) for build tooling
- Proxy configured to backend at `http://localhost:5000`

## Backend Stack

- Express 4.18 for REST API
- SQLite3 for database
- CORS enabled for cross-origin requests
- Body-parser for JSON request handling

## Development Dependencies

- Concurrently for running frontend and backend simultaneously

## Common Commands

### Initial Setup
```bash
npm run install-all    # Install all dependencies (root + client)
npm run init-db        # Initialize SQLite database with sample data
```

### Development
```bash
npm run dev           # Run both frontend and backend concurrently
npm run server        # Run backend only (port 5000)
npm run client        # Run frontend only (port 3000)
```

### Frontend Only
```bash
cd client
npm start            # Start React dev server
npm run build        # Build production bundle
```

## Ports

- Frontend: `http://localhost:3000`
- Backend: `http://localhost:5000`
