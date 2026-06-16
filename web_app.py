"""
E-COMMERCE WEB APPLICATION - Flask Version
Complete with all API endpoints for the website
"""

from flask import Flask, render_template, jsonify, request, session
import json
import os
import uuid
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'ecommerce_secret_key_2024'

# Disable caching
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

# ==================== DATA STORAGE ====================

DATA_DIR = 'web_data'

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def load_json(filename):
    ensure_data_dir()
    filepath = os.path.join(DATA_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return []

def save_json(filename, data):
    ensure_data_dir()
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

# ==================== PRODUCTS ====================

def get_products():
    products = load_json('products.json')
    if not products:
        products = [
            {"id": "101", "name": "Gaming Laptop", "price": 89999, "stock": 10, "category": "Electronics", "image": "💻"},
            {"id": "102", "name": "Wireless Mouse", "price": 1299, "stock": 50, "category": "Electronics", "image": "🖱️"},
            {"id": "103", "name": "Cotton T-Shirt", "price": 999, "stock": 100, "category": "Clothing", "image": "👕"},
            {"id": "104", "name": "Studio Headphones", "price": 4999, "stock": 30, "category": "Electronics", "image": "🎧"},
            {"id": "105", "name": "Denim Jeans", "price": 2499, "stock": 40, "category": "Clothing", "image": "👖"},
            {"id": "106", "name": "Doraemon Plush Toy", "price": 1499, "stock": 25, "category": "Toys", "image": "🐱"},
            {"id": "107", "name": "Doraemon Gadget Watch", "price": 2999, "stock": 15, "category": "Accessories", "image": "⌚"},
            {"id": "108", "name": "Doraemon T-Shirt", "price": 1299, "stock": 35, "category": "Clothing", "image": "👕"},
            {"id": "109", "name": "Pikachu Soft Toy", "price": 1999, "stock": 20, "category": "Toys", "image": "🐭"},
            {"id": "110", "name": "Pikachu Backpack", "price": 3499, "stock": 12, "category": "Bags", "image": "🎒"},
            {"id": "111", "name": "Pikachu Hoodie", "price": 3999, "stock": 18, "category": "Clothing", "image": "👔"},
            {"id": "112", "name": "Niet Anime Bag", "price": 4499, "stock": 10, "category": "Bags", "image": "🎒"},
            {"id": "113", "name": "Dragon Ball Backpack", "price": 3999, "stock": 15, "category": "Bags", "image": "🎒"},
            {"id": "114", "name": "Anime Poster Set", "price": 999, "stock": 50, "category": "Accessories", "image": "🖼️"},
            {"id": "115", "name": "Naruto Headband", "price": 499, "stock": 60, "category": "Accessories", "image": "🎀"}
        ]
        save_json('products.json', products)
    
    for p in products:
        p['product_id'] = p['id']
    return products

# ==================== CART ====================

def get_cart(user_id):
    carts = load_json('carts.json')
    for cart in carts:
        if cart['user_id'] == user_id:
            return cart
    return {'user_id': user_id, 'products': [], 'total_amount': 0}

def save_cart(user_id, cart_data):
    carts = load_json('carts.json')
    found = False
    for i, cart in enumerate(carts):
        if cart['user_id'] == user_id:
            carts[i] = cart_data
            found = True
            break
    if not found:
        carts.append(cart_data)
    save_json('carts.json', carts)

# ==================== ORDERS ====================

def get_orders(user_id):
    orders = load_json('orders.json')
    return [o for o in orders if o.get('user_id') == user_id]

def save_order(order):
    orders = load_json('orders.json')
    orders.append(order)
    save_json('orders.json', orders)

# ==================== FLASK ROUTES ====================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/products')
def api_products():
    products = get_products()
    return jsonify(products)

@app.route('/api/cart')
def api_cart():
    user_id = session.get('user_id', 'guest_' + str(uuid.uuid4())[:8])
    if 'user_id' not in session:
        session['user_id'] = user_id
    
    cart = get_cart(user_id)
    cart['total_amount'] = sum(item['price'] * item['quantity'] for item in cart.get('products', []))
    return jsonify(cart)

@app.route('/api/add-to-cart', methods=['POST'])
def api_add_to_cart():
    user_id = session.get('user_id', 'guest_' + str(uuid.uuid4())[:8])
    if 'user_id' not in session:
        session['user_id'] = user_id
    
    data = request.json
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    products = get_products()
    product = None
    for p in products:
        if p['id'] == product_id:
            product = p
            break
    
    if not product:
        return jsonify({'success': False, 'error': 'Product not found'})
    
    if product['stock'] < quantity:
        return jsonify({'success': False, 'error': f'Only {product["stock"]} items available'})
    
    cart = get_cart(user_id)
    
    found = False
    for item in cart.get('products', []):
        if item['id'] == product_id:
            item['quantity'] += quantity
            found = True
            break
    
    if not found:
        cart['products'].append({
            'id': product_id,
            'name': product['name'],
            'price': product['price'],
            'quantity': quantity,
            'image': product.get('image', '📦')
        })
    
    save_cart(user_id, cart)
    return jsonify({'success': True})

@app.route('/api/update-cart', methods=['POST'])
def api_update_cart():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False})
    
    data = request.json
    product_id = data.get('product_id')
    quantity = data.get('quantity', 0)
    
    cart = get_cart(user_id)
    
    if quantity <= 0:
        cart['products'] = [item for item in cart.get('products', []) if item['id'] != product_id]
    else:
        for item in cart.get('products', []):
            if item['id'] == product_id:
                item['quantity'] = quantity
                break
    
    save_cart(user_id, cart)
    return jsonify({'success': True})

@app.route('/api/place-order', methods=['POST'])
def api_place_order():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'error': 'Please login'})
    
    data = request.json
    payment_method = data.get('payment_method', 'COD')
    
    cart = get_cart(user_id)
    
    if not cart.get('products'):
        return jsonify({'success': False, 'error': 'Cart is empty'})
    
    total = sum(item['price'] * item['quantity'] for item in cart['products'])
    order_id = 'ORD' + datetime.now().strftime('%Y%m%d%H%M%S')
    
    # Update stock
    products = get_products()
    for cart_item in cart['products']:
        for product in products:
            if product['id'] == cart_item['id']:
                product['stock'] -= cart_item['quantity']
                break
    save_json('products.json', products)
    
    order = {
        'id': order_id,
        'user_id': user_id,
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'items': cart['products'].copy(),
        'total': total,
        'payment_method': payment_method,
        'status': 'Confirmed'
    }
    
    save_order(order)
    
    cart['products'] = []
    save_cart(user_id, cart)
    
    return jsonify({'success': True, 'order_id': order_id})

@app.route('/api/orders')
def api_orders():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify([])
    
    orders = get_orders(user_id)
    return jsonify(orders)

# ==================== ADMIN API ENDPOINTS ====================

@app.route('/api/admin/products', methods=['GET'])
def admin_get_products():
    products = get_products()
    return jsonify(products)

@app.route('/api/admin/add-product', methods=['POST'])
def admin_add_product():
    data = request.json
    
    name = data.get('name')
    price = data.get('price')
    stock = data.get('stock')
    category = data.get('category')
    
    if not all([name, price, stock, category]):
        return jsonify({'success': False, 'error': 'Missing fields'})
    
    products = get_products()
    
    existing_ids = [int(p.get('id', '100')) for p in products if str(p.get('id', '')).isdigit()]
    new_id = str(max(existing_ids, default=100) + 1)
    
    new_product = {
        "id": new_id,
        "name": name,
        "price": float(price),
        "stock": int(stock),
        "category": category,
        "image": "📦"
    }
    
    products.append(new_product)
    save_json('products.json', products)
    
    return jsonify({'success': True, 'product': new_product})

@app.route('/api/admin/update-product/<product_id>', methods=['PUT'])
def admin_update_product(product_id):
    data = request.json
    new_stock = data.get('stock')
    new_price = data.get('price')
    
    products = get_products()
    product = None
    for p in products:
        if p['id'] == product_id:
            product = p
            break
    
    if not product:
        return jsonify({'success': False, 'error': 'Product not found'})
    
    if new_stock is not None:
        product['stock'] = int(new_stock)
    if new_price is not None:
        product['price'] = float(new_price)
    
    save_json('products.json', products)
    return jsonify({'success': True, 'product': product})

@app.route('/api/admin/delete-product/<product_id>', methods=['DELETE'])
def admin_delete_product(product_id):
    products = get_products()
    products = [p for p in products if p['id'] != product_id]
    save_json('products.json', products)
    return jsonify({'success': True})

if __name__ == '__main__':
    print("=" * 50)
    print("   E-COMMERCE WEB PORTAL")
    print("=" * 50)
    print("Starting server at: http://127.0.0.1:5000")
    print("All API endpoints ready")
    print("Press Ctrl+C to stop")
    print("=" * 50)
    app.run(debug=True, host='127.0.0.1', port=5000)