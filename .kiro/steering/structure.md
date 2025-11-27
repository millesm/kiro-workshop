---
inclusion: always
---

# Project Structure

## Root Level

```
/
├── client/              # React frontend application
├── server/              # Node.js backend application
├── ecommerce.db         # SQLite database file (generated)
├── package.json         # Root package with scripts for full-stack dev
└── README.md
```

## Frontend Structure (`/client`)

```
client/
├── public/
│   └── index.html       # HTML template
├── src/
│   ├── pages/           # Page components (route handlers)
│   │   ├── Home.js      # Product listing page
│   │   ├── Product.js   # Product detail page
│   │   └── Cart.js      # Shopping cart page
│   ├── App.js           # Main app component with routing
│   ├── index.js         # React entry point
│   └── index.css        # Global styles
└── package.json         # Frontend dependencies
```

## Backend Structure (`/server`)

```
server/
├── index.js             # Express server with REST API endpoints
└── initDb.js            # Database initialization script
```

## API Endpoints

All endpoints are prefixed with `/api`:

- `GET /api/products` - List all products
- `GET /api/products/:id` - Get product details with reviews
- `GET /api/cart` - Get cart items with product details
- `POST /api/cart` - Add item to cart (or update if exists)
- `PUT /api/cart/:id` - Update cart item quantity
- `DELETE /api/cart/:id` - Remove item from cart

## Database Schema

**products**
- id, emoji, name, price, description

**cart**
- id, product_id (FK), quantity

**reviews**
- id, product_id (FK), author, rating, comment

## Conventions

- React components use functional components (no class components)
- Backend uses callback-based SQLite queries
- Frontend fetches data using native `fetch()` API
- Product images represented by emojis (stored in database)
- All API responses return JSON
