const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database('./ecommerce.db');

const products = [
  { emoji: '📱', name: 'Smartphone', price: 699, description: 'Latest model with advanced features' },
  { emoji: '💻', name: 'Laptop', price: 1299, description: 'High-performance laptop for work and play' },
  { emoji: '🎧', name: 'Headphones', price: 199, description: 'Noise-canceling wireless headphones' },
  { emoji: '⌚', name: 'Smartwatch', price: 399, description: 'Track your fitness and stay connected' },
  { emoji: '📷', name: 'Camera', price: 899, description: 'Professional-grade digital camera' },
  { emoji: '🖥️', name: 'Monitor', price: 449, description: '4K ultra-wide display' },
  { emoji: '⌨️', name: 'Keyboard', price: 129, description: 'Mechanical gaming keyboard' },
  { emoji: '🖱️', name: 'Mouse', price: 79, description: 'Ergonomic wireless mouse' },
  { emoji: '🎮', name: 'Gaming Console', price: 499, description: 'Next-gen gaming experience' },
  { emoji: '📺', name: 'Smart TV', price: 799, description: '55-inch 4K smart television' },
  { emoji: '🔊', name: 'Speaker', price: 149, description: 'Bluetooth portable speaker' },
  { emoji: '🎤', name: 'Microphone', price: 99, description: 'Studio-quality USB microphone' },
  { emoji: '💾', name: 'External SSD', price: 179, description: '1TB portable storage' },
  { emoji: '🔌', name: 'Power Bank', price: 49, description: '20000mAh fast charging' },
  { emoji: '📡', name: 'Router', price: 159, description: 'WiFi 6 mesh router' },
  { emoji: '🖨️', name: 'Printer', price: 229, description: 'All-in-one wireless printer' },
  { emoji: '🎥', name: 'Webcam', price: 89, description: '1080p HD webcam' },
  { emoji: '🕹️', name: 'Controller', price: 69, description: 'Wireless game controller' },
  { emoji: '💡', name: 'Smart Bulb', price: 29, description: 'Color-changing LED bulb' },
  { emoji: '🔋', name: 'Batteries', price: 19, description: 'Rechargeable battery pack' }
];

db.serialize(() => {
  db.run('DROP TABLE IF EXISTS cart');
  db.run('DROP TABLE IF EXISTS reviews');
  db.run('DROP TABLE IF EXISTS products');
  
  db.run(`CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    emoji TEXT,
    name TEXT,
    price REAL,
    description TEXT
  )`);
  
  db.run(`CREATE TABLE cart (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    quantity INTEGER,
    FOREIGN KEY(product_id) REFERENCES products(id)
  )`);
  
  db.run(`CREATE TABLE reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    author TEXT,
    rating INTEGER,
    comment TEXT,
    FOREIGN KEY(product_id) REFERENCES products(id)
  )`);
  
  const stmt = db.prepare('INSERT INTO products (emoji, name, price, description) VALUES (?, ?, ?, ?)');
  products.forEach(p => stmt.run(p.emoji, p.name, p.price, p.description));
  stmt.finalize();
  
  const reviewStmt = db.prepare('INSERT INTO reviews (product_id, author, rating, comment) VALUES (?, ?, ?, ?)');
  for (let i = 1; i <= 20; i++) {
    reviewStmt.run(i, 'John Doe', 5, 'Excellent product! Highly recommend.');
    reviewStmt.run(i, 'Jane Smith', 4, 'Good quality, fast shipping.');
  }
  reviewStmt.finalize();
  
  console.log('Database initialized with sample data!');
});

db.close();
