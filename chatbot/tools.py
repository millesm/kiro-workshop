"""Custom tools for the Shopping Assistant Chatbot.

This module provides tools that allow the agent to interact with the backend e-commerce API.
"""

import logging
import requests
from typing import Dict, List, Any
from strands import tool
from chatbot.config import get_config

logger = logging.getLogger(__name__)


def _make_api_request(method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
    """Make an API request to the backend with error handling.
    
    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        endpoint: API endpoint path
        **kwargs: Additional arguments to pass to requests
    
    Returns:
        Dictionary containing the API response or error information
    """
    config = get_config()
    url = f"{config.backend_api_url}{endpoint}"
    
    try:
        logger.info(f"Making {method} request to {url}")
        response = requests.request(method, url, timeout=10, **kwargs)
        response.raise_for_status()
        
        # Return JSON response if available
        try:
            return response.json()
        except ValueError:
            return {"message": "Success", "status_code": response.status_code}
    
    except requests.exceptions.Timeout:
        error_msg = f"Request to {url} timed out"
        logger.error(error_msg)
        return {"error": error_msg, "error_type": "network"}
    
    except requests.exceptions.ConnectionError:
        error_msg = f"Could not connect to backend API at {url}"
        logger.error(error_msg)
        return {"error": error_msg, "error_type": "network"}
    
    except requests.exceptions.HTTPError as e:
        error_msg = f"API returned error: {e.response.status_code}"
        if e.response.text:
            try:
                error_data = e.response.json()
                error_msg = error_data.get('error', error_msg)
            except ValueError:
                error_msg = e.response.text
        
        logger.error(f"HTTP error: {error_msg}")
        return {"error": error_msg, "error_type": "api", "status_code": e.response.status_code}
    
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg, "error_type": "unknown"}


@tool
def list_products() -> str:
    """Get all available products from the catalog.
    
    Returns:
        A formatted string containing all products with their details.
    """
    logger.info("Tool invoked: list_products")
    
    result = _make_api_request('GET', '/api/products')
    
    if 'error' in result:
        return f"I'm sorry, I couldn't retrieve the products right now. Error: {result['error']}"
    
    if not result or len(result) == 0:
        return "There are currently no products available in the catalog."
    
    # Format products for display
    products_text = "Here are the available products:\n\n"
    for product in result:
        products_text += (
            f"{product.get('emoji', '📦')} {product.get('name', 'Unknown')} - "
            f"${product.get('price', 0):.2f}\n"
            f"   {product.get('description', 'No description available')}\n"
            f"   Product ID: {product.get('id')}\n\n"
        )
    
    return products_text


@tool
def get_product_details(product_id: int) -> str:
    """Get detailed information about a specific product including reviews.
    
    Args:
        product_id: The ID of the product to retrieve
    
    Returns:
        A formatted string containing product details and reviews.
    """
    logger.info(f"Tool invoked: get_product_details with product_id={product_id}")
    
    result = _make_api_request('GET', f'/api/products/{product_id}')
    
    if 'error' in result:
        if result.get('status_code') == 404:
            return f"I couldn't find a product with ID {product_id}. Please check the product ID and try again."
        return f"I'm sorry, I couldn't retrieve the product details. Error: {result['error']}"
    
    # Format product details
    product = result.get('product', {})
    reviews = result.get('reviews', [])
    
    details_text = (
        f"{product.get('emoji', '📦')} {product.get('name', 'Unknown Product')}\n\n"
        f"Price: ${product.get('price', 0):.2f}\n"
        f"Description: {product.get('description', 'No description available')}\n"
        f"Product ID: {product.get('id')}\n\n"
    )
    
    # Add reviews if available
    if reviews:
        details_text += f"Customer Reviews ({len(reviews)}):\n\n"
        for review in reviews:
            rating = '⭐' * review.get('rating', 0)
            details_text += (
                f"{rating} ({review.get('rating', 0)}/5) - {review.get('author', 'Anonymous')}\n"
                f"{review.get('comment', 'No comment')}\n\n"
            )
    else:
        details_text += "No customer reviews yet.\n"
    
    return details_text


@tool
def get_cart() -> str:
    """View the current shopping cart contents.
    
    Returns:
        A formatted string containing cart items with product details and quantities.
    """
    logger.info("Tool invoked: get_cart")
    
    result = _make_api_request('GET', '/api/cart')
    
    if 'error' in result:
        return f"I'm sorry, I couldn't retrieve your cart. Error: {result['error']}"
    
    if not result or len(result) == 0:
        return "Your shopping cart is empty."
    
    # Format cart items
    cart_text = "Your Shopping Cart:\n\n"
    total = 0.0
    
    for item in result:
        # Backend API returns product details directly in the item (flat structure)
        # Check if there's a nested 'product' object, otherwise use the item itself
        product = item.get('product', item)
        quantity = item.get('quantity', 0)
        price = product.get('price', 0)
        subtotal = price * quantity
        total += subtotal
        
        cart_text += (
            f"{product.get('emoji', '📦')} {product.get('name', 'Unknown')} x {quantity}\n"
            f"   ${price:.2f} each = ${subtotal:.2f}\n"
            f"   Cart Item ID: {item.get('id')}\n\n"
        )
    
    cart_text += f"Total: ${total:.2f}"
    
    return cart_text


@tool
def add_to_cart(product_id: int, quantity: int = 1) -> str:
    """Add a product to the shopping cart.
    
    Args:
        product_id: The ID of the product to add
        quantity: The quantity to add (default: 1)
    
    Returns:
        A confirmation message.
    """
    logger.info(f"Tool invoked: add_to_cart with product_id={product_id}, quantity={quantity}")
    
    if quantity <= 0:
        return "The quantity must be greater than 0."
    
    result = _make_api_request(
        'POST',
        '/api/cart',
        json={'product_id': product_id, 'quantity': quantity}
    )
    
    if 'error' in result:
        if result.get('status_code') == 404:
            return f"I couldn't find a product with ID {product_id}. Please check the product ID and try again."
        return f"I'm sorry, I couldn't add the item to your cart. Error: {result['error']}"
    
    return f"Successfully added {quantity} item(s) to your cart! (Product ID: {product_id})"


@tool
def update_cart_item(cart_item_id: int, quantity: int) -> str:
    """Update the quantity of an item in the shopping cart.
    
    Args:
        cart_item_id: The ID of the cart item to update
        quantity: The new quantity
    
    Returns:
        A confirmation message.
    """
    logger.info(f"Tool invoked: update_cart_item with cart_item_id={cart_item_id}, quantity={quantity}")
    
    if quantity <= 0:
        return "The quantity must be greater than 0. To remove an item, use the remove_from_cart function."
    
    result = _make_api_request(
        'PUT',
        f'/api/cart/{cart_item_id}',
        json={'quantity': quantity}
    )
    
    if 'error' in result:
        if result.get('status_code') == 404:
            return f"I couldn't find a cart item with ID {cart_item_id}. Please check your cart and try again."
        return f"I'm sorry, I couldn't update the cart item. Error: {result['error']}"
    
    return f"Successfully updated cart item {cart_item_id} to quantity {quantity}!"


@tool
def remove_from_cart(cart_item_id: int) -> str:
    """Remove an item from the shopping cart.
    
    Args:
        cart_item_id: The ID of the cart item to remove
    
    Returns:
        A confirmation message.
    """
    logger.info(f"Tool invoked: remove_from_cart with cart_item_id={cart_item_id}")
    
    result = _make_api_request('DELETE', f'/api/cart/{cart_item_id}')
    
    if 'error' in result:
        if result.get('status_code') == 404:
            return f"I couldn't find a cart item with ID {cart_item_id}. It may have already been removed."
        return f"I'm sorry, I couldn't remove the item from your cart. Error: {result['error']}"
    
    return f"Successfully removed item {cart_item_id} from your cart!"


# Export all tools as a list for easy registration
ALL_TOOLS = [
    list_products,
    get_product_details,
    get_cart,
    add_to_cart,
    update_cart_item,
    remove_from_cart
]
