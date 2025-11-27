const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const sqlite3 = require('sqlite3').verbose();

const app = express();
const PORT = 5000;

app.use(cors());
app.use(bodyParser.json());

const db = new sqlite3.Database('./ecommerce.db');

// Get all products
app.get('/api/products', (req, res) => {
  db.all('SELECT * FROM products', [], (err, rows) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(rows);
  });
});

// Get single product
app.get('/api/products/:id', (req, res) => {
  db.get('SELECT * FROM products WHERE id = ?', [req.params.id], (err, row) => {
    if (err) return res.status(500).json({ error: err.message });
    if (!row) return res.status(404).json({ error: 'Product not found' });
    
    db.all('SELECT * FROM reviews WHERE product_id = ?', [req.params.id], (err, reviews) => {
      if (err) return res.status(500).json({ error: err.message });
      res.json({ ...row, reviews });
    });
  });
});

// Get cart items
app.get('/api/cart', (req, res) => {
  db.all(`
    SELECT c.id as cart_item_id, c.product_id, c.quantity, 
           p.id as product_id, p.emoji, p.name, p.price, p.description
    FROM cart c 
    JOIN products p ON c.product_id = p.id
  `, [], (err, rows) => {
    if (err) return res.status(500).json({ error: err.message });
    // Restructure to have clear cart_item_id and product details
    const cartItems = rows.map(row => ({
      id: row.cart_item_id,
      product_id: row.product_id,
      quantity: row.quantity,
      product: {
        id: row.product_id,
        emoji: row.emoji,
        name: row.name,
        price: row.price,
        description: row.description
      }
    }));
    res.json(cartItems);
  });
});

// Add to cart
app.post('/api/cart', (req, res) => {
  const { product_id, quantity } = req.body;
  
  db.get('SELECT * FROM cart WHERE product_id = ?', [product_id], (err, row) => {
    if (err) return res.status(500).json({ error: err.message });
    
    if (row) {
      db.run('UPDATE cart SET quantity = quantity + ? WHERE product_id = ?', 
        [quantity, product_id], (err) => {
          if (err) return res.status(500).json({ error: err.message });
          res.json({ message: 'Cart updated' });
        });
    } else {
      db.run('INSERT INTO cart (product_id, quantity) VALUES (?, ?)', 
        [product_id, quantity], (err) => {
          if (err) return res.status(500).json({ error: err.message });
          res.json({ message: 'Added to cart' });
        });
    }
  });
});

// Update cart item quantity
app.put('/api/cart/:id', (req, res) => {
  const { quantity } = req.body;
  db.run('UPDATE cart SET quantity = ? WHERE id = ?', [quantity, req.params.id], (err) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json({ message: 'Cart updated' });
  });
});

// Delete cart item
app.delete('/api/cart/:id', (req, res) => {
  db.run('DELETE FROM cart WHERE id = ?', [req.params.id], (err) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json({ message: 'Item removed' });
  });
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
