import React, { useState, useEffect } from 'react';

function Cart() {
  const [cartItems, setCartItems] = useState([]);

  const fetchCart = () => {
    fetch('/api/cart')
      .then(res => res.json())
      .then(data => setCartItems(data))
      .catch(err => console.error(err));
  };

  useEffect(() => {
    fetchCart();
  }, []);

  const updateQuantity = (id, quantity) => {
    if (quantity < 1) return;
    fetch(`/api/cart/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ quantity })
    })
      .then(() => fetchCart())
      .catch(err => console.error(err));
  };

  const removeItem = (id) => {
    fetch(`/api/cart/${id}`, { method: 'DELETE' })
      .then(() => fetchCart())
      .catch(err => console.error(err));
  };

  // Handle both old flat structure and new nested structure
  const getProduct = (item) => item.product || item;
  
  const total = cartItems.reduce((sum, item) => {
    const product = getProduct(item);
    return sum + (product.price * item.quantity);
  }, 0);

  if (cartItems.length === 0) {
    return (
      <div className="container">
        <div className="empty-cart">
          <div className="empty-cart-emoji">🛒</div>
          <h2>Your cart is empty</h2>
          <p>Add some products to get started!</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <h2 style={{ marginBottom: '2rem', color: '#2c3e50' }}>Shopping Cart</h2>
      
      <div className="cart-items">
        {cartItems.map(item => {
          const product = getProduct(item);
          return (
            <div key={item.id} className="cart-item">
              <div className="cart-item-emoji">{product.emoji}</div>
              <div className="cart-item-info">
                <h3>{product.name}</h3>
                <p className="product-price">${product.price}</p>
              </div>
              <div className="cart-item-actions">
                <div className="quantity-selector">
                  <button onClick={() => updateQuantity(item.id, item.quantity - 1)}>-</button>
                  <input 
                    type="number" 
                    value={item.quantity}
                    onChange={(e) => updateQuantity(item.id, parseInt(e.target.value) || 1)}
                  />
                  <button onClick={() => updateQuantity(item.id, item.quantity + 1)}>+</button>
                </div>
                <button className="btn btn-danger" onClick={() => removeItem(item.id)}>
                  Remove
                </button>
              </div>
            </div>
          );
        })}
      </div>
      
      <div className="cart-summary">
        <h2>Order Summary</h2>
        <p>Items: {cartItems.length}</p>
        <p className="total">Total: ${total.toFixed(2)}</p>
        <button className="btn btn-primary" onClick={() => alert('Checkout functionality coming soon!')}>
          Proceed to Checkout
        </button>
      </div>
    </div>
  );
}

export default Cart;
