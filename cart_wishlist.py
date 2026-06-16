"""
Cart and Wishlist Management Module
"""

import uuid

class CartManager:
    """Manages shopping cart operations"""
    
    def __init__(self, storage):
        self.storage = storage
    
    def get_cart(self, user_id):
        """Get user's cart"""
        carts = self.storage.load_carts()
        
        for cart in carts:
            if cart['user_id'] == user_id:
                # Calculate total
                total = sum(item['subtotal'] for item in cart['products'])
                cart['total_amount'] = total
                return cart
        
        # Create new cart if doesn't exist
        new_cart = {
            'cart_id': str(uuid.uuid4())[:8],
            'user_id': user_id,
            'products': [],
            'total_amount': 0
        }
        carts.append(new_cart)
        self.storage.save_carts(carts)
        return new_cart
    
    def add_to_cart(self, user_id, product_id, quantity):
        """Add product to cart"""
        cart = self.get_cart(user_id)
        products = self.storage.load_products()
        
        # Find product
        product = None
        for p in products:
            if p['product_id'] == product_id:
                product = p
                break
        
        if not product:
            return False
        
        if product['stock'] < quantity:
            print(f"Only {product['stock']} items available!")
            return False
        
        # Check if product already in cart
        carts = self.storage.load_carts()
        for c in carts:
            if c['cart_id'] == cart['cart_id']:
                found = False
                for item in c['products']:
                    if item['product_id'] == product_id:
                        item['quantity'] += quantity
                        item['subtotal'] = item['quantity'] * item['price']
                        found = True
                        break
                
                if not found:
                    c['products'].append({
                        'product_id': product_id,
                        'name': product['name'],
                        'price': product['price'],
                        'quantity': quantity,
                        'subtotal': product['price'] * quantity
                    })
                
                self.storage.save_carts(carts)
                return True
        
        return False
    
    def remove_from_cart(self, user_id, product_id):
        """Remove product from cart"""
        carts = self.storage.load_carts()
        
        for cart in carts:
            if cart['user_id'] == user_id:
                for i, item in enumerate(cart['products']):
                    if item['product_id'] == product_id:
                        cart['products'].pop(i)
                        self.storage.save_carts(carts)
                        return True
        return False
    
    def update_quantity(self, user_id, product_id, quantity):
        """Update product quantity in cart"""
        carts = self.storage.load_carts()
        
        for cart in carts:
            if cart['user_id'] == user_id:
                for item in cart['products']:
                    if item['product_id'] == product_id:
                        if quantity <= 0:
                            return self.remove_from_cart(user_id, product_id)
                        
                        # Check stock
                        products = self.storage.load_products()
                        for p in products:
                            if p['product_id'] == product_id:
                                if p['stock'] >= quantity:
                                    item['quantity'] = quantity
                                    item['subtotal'] = item['price'] * quantity
                                    self.storage.save_carts(carts)
                                    return True
                                else:
                                    print(f"Only {p['stock']} items available!")
                                    return False
        return False
    
    def clear_cart(self, user_id):
        """Clear user's cart"""
        carts = self.storage.load_carts()
        
        for cart in carts:
            if cart['user_id'] == user_id:
                cart['products'] = []
                cart['total_amount'] = 0
                self.storage.save_carts(carts)
                return True
        return False

class WishlistManager:
    """Manages wishlist operations"""
    
    def __init__(self, storage):
        self.storage = storage
    
    def get_wishlist(self, user_id):
        """Get user's wishlist"""
        wishlists = self.storage.load_wishlists()
        
        for wishlist in wishlists:
            if wishlist['user_id'] == user_id:
                return wishlist
        
        # Create new wishlist
        new_wishlist = {
            'wishlist_id': str(uuid.uuid4())[:8],
            'user_id': user_id,
            'products': []
        }
        wishlists.append(new_wishlist)
        self.storage.save_wishlists(wishlists)
        return new_wishlist
    
    def add_to_wishlist(self, user_id, product_id):
        """Add product to wishlist"""
        wishlist = self.get_wishlist(user_id)
        products = self.storage.load_products()
        
        # Find product
        product = None
        for p in products:
            if p['product_id'] == product_id:
                product = p
                break
        
        if not product:
            return False
        
        wishlists = self.storage.load_wishlists()
        for w in wishlists:
            if w['wishlist_id'] == wishlist['wishlist_id']:
                # Check if already in wishlist
                for item in w['products']:
                    if item['product_id'] == product_id:
                        return True
                
                w['products'].append({
                    'product_id': product_id,
                    'name': product['name'],
                    'price': product['price']
                })
                
                self.storage.save_wishlists(wishlists)
                return True
        
        return False
    
    def remove_from_wishlist(self, user_id, product_id):
        """Remove product from wishlist"""
        wishlists = self.storage.load_wishlists()
        
        for wishlist in wishlists:
            if wishlist['user_id'] == user_id:
                for i, item in enumerate(wishlist['products']):
                    if item['product_id'] == product_id:
                        wishlist['products'].pop(i)
                        self.storage.save_wishlists(wishlists)
                        return True
        return False
    
    def move_to_cart(self, user_id, product_id, cart_manager):
        """Move product from wishlist to cart"""
        # Get wishlist item
        wishlist = self.get_wishlist(user_id)
        
        for item in wishlist['products']:
            if item['product_id'] == product_id:
                # Add to cart with quantity 1
                if cart_manager.add_to_cart(user_id, product_id, 1):
                    # Remove from wishlist
                    self.remove_from_wishlist(user_id, product_id)
                    return True
        return False