# E-Commerce Website

A simple 3-tier e-commerce application with React frontend, Node.js backend, and SQLite database.

## Setup Instructions

1. Install dependencies:
```bash
npm run install-all
```

2. Initialize the database:
```bash
npm run init-db
```

3. Start the application:
```bash
npm run dev
```

The frontend will run on http://localhost:3000 and the backend on http://localhost:5000.

## Architecture

- **Frontend**: React with React Router for navigation
- **Backend**: Node.js with Express for REST API
- **Database**: SQLite for storing products, cart items, and reviews

## Features

- Home page with 20 products (using emojis as product images)
- Product detail page with description, price, quantity selector, and reviews
- Shopping cart with quantity updates and item removal
- Responsive design with clean UI
