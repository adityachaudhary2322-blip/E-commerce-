"""
Simple Data Storage Module - Using only TXT files
"""

import os

class DataStorage:
    """Handles all file storage operations using simple text files"""
    
    def __init__(self):
        self.data_dir = 'data'
        self.ensure_data_directory()
    
    def ensure_data_directory(self):
        """Ensure data directory exists"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        # Initialize empty files if they don't exist
        files = ['users.txt', 'products.txt', 'carts.txt', 
                 'wishlists.txt', 'orders.txt', 'payments.txt', 'invoices.txt']
        
        for file in files:
            filepath = os.path.join(self.data_dir, file)
            if not os.path.exists(filepath):
                with open(filepath, 'w') as f:
                    f.write("")  # Empty file
    
    # User operations - Simple pipe-delimited format
    def load_users(self):
        """Load users from TXT file"""
        users = []
        try:
            with open(os.path.join(self.data_dir, 'users.txt'), 'r') as f:
                for line in f:
                    if line.strip():
                        parts = line.strip().split('|')
                        if len(parts) >= 5:
                            user = {
                                'user_id': parts[0],
                                'name': parts[1],
                                'email': parts[2],
                                'password': parts[3],
                                'registered_date': parts[4],
                                'order_history': parts[5].split(',') if len(parts) > 5 and parts[5] else []
                            }
                            users.append(user)
        except FileNotFoundError:
            pass
        return users
    
    def save_users(self, users):
        """Save users to TXT file"""
        with open(os.path.join(self.data_dir, 'users.txt'), 'w') as f:
            for user in users:
                order_history = ','.join(user.get('order_history', []))
                f.write(f"{user['user_id']}|{user['name']}|{user['email']}|{user['password']}|{user['registered_date']}|{order_history}\n")
    
    # Product operations
    def load_products(self):
        """Load products from TXT file"""
        products = []
        try:
            with open(os.path.join(self.data_dir, 'products.txt'), 'r') as f:
                for line in f:
                    if line.strip():
                        parts = line.strip().split('|')
                        if len(parts) >= 6:
                            product = {
                                'product_id': parts[0],
                                'name': parts[1],
                                'price': float(parts[2]),
                                'stock': int(parts[3]),
                                'category': parts[4],
                                'brand': parts[5] if len(parts) > 5 and parts[5] != 'None' else None,
                                'size': parts[6] if len(parts) > 6 and parts[6] != 'None' else None
                            }
                            products.append(product)
        except FileNotFoundError:
            pass
        return products
    
    def save_products(self, products):
        """Save products to TXT file"""
        with open(os.path.join(self.data_dir, 'products.txt'), 'w') as f:
            for product in products:
                brand = product.get('brand', 'None')
                size = product.get('size', 'None')
                f.write(f"{product['product_id']}|{product['name']}|{product['price']}|{product['stock']}|{product['category']}|{brand}|{size}\n")
    
    def update_product_stock(self, product_id, quantity):
        """Update product stock"""
        products = self.load_products()
        for product in products:
            if product['product_id'] == product_id:
                product['stock'] -= quantity
                self.save_products(products)
                return True
        return False
    
    # Cart operations
    def load_carts(self):
        """Load carts from TXT file"""
        carts = []
        try:
            with open(os.path.join(self.data_dir, 'carts.txt'), 'r') as f:
                for line in f:
                    if line.strip():
                        parts = line.strip().split('|')
                        if len(parts) >= 3:
                            cart = {
                                'cart_id': parts[0],
                                'user_id': parts[1],
                                'products': [],
                                'total_amount': float(parts[3]) if len(parts) > 3 else 0
                            }
                            # Parse products (format: product_id:name:price:quantity:subtotal;...)
                            if len(parts) > 2 and parts[2]:
                                for item_str in parts[2].split(';'):
                                    if item_str:
                                        item_parts = item_str.split(':')
                                        if len(item_parts) == 5:
                                            cart['products'].append({
                                                'product_id': item_parts[0],
                                                'name': item_parts[1],
                                                'price': float(item_parts[2]),
                                                'quantity': int(item_parts[3]),
                                                'subtotal': float(item_parts[4])
                                            })
                            carts.append(cart)
        except FileNotFoundError:
            pass
        return carts
    
    def save_carts(self, carts):
        """Save carts to TXT file"""
        with open(os.path.join(self.data_dir, 'carts.txt'), 'w') as f:
            for cart in carts:
                # Format products
                products_str = ''
                for product in cart.get('products', []):
                    products_str += f"{product['product_id']}:{product['name']}:{product['price']}:{product['quantity']}:{product['subtotal']};"
                
                f.write(f"{cart['cart_id']}|{cart['user_id']}|{products_str}|{cart.get('total_amount', 0)}\n")
    
    # Wishlist operations
    def load_wishlists(self):
        """Load wishlists from TXT file"""
        wishlists = []
        try:
            with open(os.path.join(self.data_dir, 'wishlists.txt'), 'r') as f:
                for line in f:
                    if line.strip():
                        parts = line.strip().split('|')
                        if len(parts) >= 3:
                            wishlist = {
                                'wishlist_id': parts[0],
                                'user_id': parts[1],
                                'products': []
                            }
                            if parts[2]:
                                for item_str in parts[2].split(';'):
                                    if item_str:
                                        item_parts = item_str.split(':')
                                        if len(item_parts) == 3:
                                            wishlist['products'].append({
                                                'product_id': item_parts[0],
                                                'name': item_parts[1],
                                                'price': float(item_parts[2])
                                            })
                            wishlists.append(wishlist)
        except FileNotFoundError:
            pass
        return wishlists
    
    def save_wishlists(self, wishlists):
        """Save wishlists to TXT file"""
        with open(os.path.join(self.data_dir, 'wishlists.txt'), 'w') as f:
            for wishlist in wishlists:
                products_str = ''
                for product in wishlist.get('products', []):
                    products_str += f"{product['product_id']}:{product['name']}:{product['price']};"
                
                f.write(f"{wishlist['wishlist_id']}|{wishlist['user_id']}|{products_str}\n")
    
    # Order operations
    def load_orders(self):
        """Load orders from TXT file"""
        orders = []
        try:
            with open(os.path.join(self.data_dir, 'orders.txt'), 'r') as f:
                for line in f:
                    if line.strip():
                        parts = line.strip().split('|')
                        if len(parts) >= 7:
                            order = {
                                'order_id': parts[0],
                                'user_id': parts[1],
                                'products': [],
                                'order_date': parts[2],
                                'order_status': parts[3],
                                'total_amount': float(parts[4]),
                                'payment_mode': parts[5]
                            }
                            # Parse products
                            if parts[6]:
                                for item_str in parts[6].split(';'):
                                    if item_str:
                                        item_parts = item_str.split(':')
                                        if len(item_parts) == 5:
                                            order['products'].append({
                                                'product_id': item_parts[0],
                                                'name': item_parts[1],
                                                'price': float(item_parts[2]),
                                                'quantity': int(item_parts[3]),
                                                'subtotal': float(item_parts[4])
                                            })
                            orders.append(order)
        except FileNotFoundError:
            pass
        return orders
    
    def save_orders(self, orders):
        """Save orders to TXT file"""
        with open(os.path.join(self.data_dir, 'orders.txt'), 'w') as f:
            for order in orders:
                products_str = ''
                for product in order.get('products', []):
                    products_str += f"{product['product_id']}:{product['name']}:{product['price']}:{product['quantity']}:{product['subtotal']};"
                
                f.write(f"{order['order_id']}|{order['user_id']}|{order['order_date']}|{order['order_status']}|{order['total_amount']}|{order['payment_mode']}|{products_str}\n")
    
    # Payment operations
    def load_payments(self):
        """Load payments from TXT file"""
        payments = []
        try:
            with open(os.path.join(self.data_dir, 'payments.txt'), 'r') as f:
                for line in f:
                    if line.strip():
                        parts = line.strip().split('|')
                        if len(parts) == 6:
                            payment = {
                                'payment_id': parts[0],
                                'order_id': parts[1],
                                'payment_mode': parts[2],
                                'payment_status': parts[3],
                                'amount': float(parts[4]),
                                'payment_date': parts[5]
                            }
                            payments.append(payment)
        except FileNotFoundError:
            pass
        return payments
    
    def save_payments(self, payments):
        """Save payments to TXT file"""
        with open(os.path.join(self.data_dir, 'payments.txt'), 'w') as f:
            for payment in payments:
                f.write(f"{payment['payment_id']}|{payment['order_id']}|{payment['payment_mode']}|{payment['payment_status']}|{payment['amount']}|{payment['payment_date']}\n")
    
    # Invoice operations
    def load_invoices(self):
        """Load invoices from TXT file"""
        invoices = []
        try:
            with open(os.path.join(self.data_dir, 'invoices.txt'), 'r') as f:
                for line in f:
                    if line.strip():
                        parts = line.strip().split('|')
                        if len(parts) >= 6:
                            invoice = {
                                'invoice_id': parts[0],
                                'order_id': parts[1],
                                'invoice_date': parts[2],
                                'total_amount': float(parts[3]),
                                'user_id': parts[4],
                                'products': []
                            }
                            # Parse products
                            if len(parts) > 5 and parts[5]:
                                for item_str in parts[5].split(';'):
                                    if item_str:
                                        item_parts = item_str.split(':')
                                        if len(item_parts) == 5:
                                            invoice['products'].append({
                                                'product_id': item_parts[0],
                                                'name': item_parts[1],
                                                'price': float(item_parts[2]),
                                                'quantity': int(item_parts[3]),
                                                'subtotal': float(item_parts[4])
                                            })
                            invoices.append(invoice)
        except FileNotFoundError:
            pass
        return invoices
    
    def save_invoices(self, invoices):
        """Save invoices to TXT file"""
        with open(os.path.join(self.data_dir, 'invoices.txt'), 'w') as f:
            for invoice in invoices:
                products_str = ''
                for product in invoice.get('products', []):
                    products_str += f"{product['product_id']}:{product['name']}:{product['price']}:{product['quantity']}:{product['subtotal']};"
                
                f.write(f"{invoice['invoice_id']}|{invoice['order_id']}|{invoice['invoice_date']}|{invoice['total_amount']}|{invoice['user_id']}|{products_str}\n")
    
    def save_all_data(self):
        """Save all data message"""
        print("✅ All data saved to TXT files!")
    
    def load_all_data(self):
        """Load all data message"""
        print("✅ All data loaded from TXT files!")