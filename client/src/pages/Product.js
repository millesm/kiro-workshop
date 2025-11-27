import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

function Product() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [product, setProduct] = useState(null);
  const [quantity, setQuantity] = useState(1);

  useEffect(() => {
    fetch(`/api/products/${id}`)
      .then(res => res.json())
      .then(data => setProduct(data))
      .catch(err => console.error(err));
  }, [id]);

  const handleAddToCart = () => {
    fetch('/api/cart', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ product_id: id, quantity })
    })
      .then(() => {
        alert('Added to cart!');
        navigate('/cart');
      })
      .catch(err => console.error(err));
  };

  if (!product) return <div className="container">Loading...</div>;

  return (
    <div className="container">
      <div className="product-detail">
        <div className="product-detail-header">
          <div className="product-detail-emoji">{product.emoji}</div>
          <div className="product-detail-info">
            <h2>{product.name}</h2>
            <p className="product-price">${product.price}</p>
            <p style={{ color: '#7f8c8d', margin: '1rem 0' }}>{product.description}</p>
            
            <div className="quantity-selector">
              <label>Quantity:</label>
              <button onClick={() => setQuantity(Math.max(1, quantity - 1))}>-</button>
              <input 
                type="number" 
                value={quantity} 
                onChange={(e) => setQuantity(Math.max(1, parseInt(e.target.value) || 1))}
              />
              <button onClick={() => setQuantity(quantity + 1)}>+</button>
            </div>
            
            <button className="btn btn-primary" onClick={handleAddToCart}>
              Add to Cart
            </button>
          </div>
        </div>
        
        <div className="reviews">
          <h3>Customer Reviews</h3>
          {product.reviews && product.reviews.map(review => (
            <div key={review.id} className="review">
              <div className="review-header">
                <strong>{review.author}</strong>
                <span className="rating">{'⭐'.repeat(review.rating)}</span>
              </div>
              <p>{review.comment}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Product;
