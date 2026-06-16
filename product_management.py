"""
Product Management Module - Handles product inventory operations
"""

from abc import ABC, abstractmethod
import uuid

# Global counter for sequential product IDs
product_counter = 100

def get_next_product_id():
    """Generate sequential product ID like 101, 102, 103"""
    global product_counter
    product_counter += 1
    return str(product_counter)

# Abstract Class
class Product(ABC):
    """Abstract Product class"""
    
    def __init__(self, product_id, name, price, stock, category):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock
        self.category = category
    
    @abstractmethod
    def display_product(self):
        """Abstract method to display product"""
        pass
    
    @abstractmethod
    def calculate_discount(self):
        """Abstract method to calculate discount"""
        pass
    
    def update_stock(self, quantity):
        """Update stock quantity"""
        self.stock -= quantity
        return self.stock

# Derived Class - Electronics
class Electronics(Product):
    """Electronics product class"""
    
    def __init__(self, product_id, name, price, stock, brand, warranty, model):
        super().__init__(product_id, name, price, stock, "Electronics")
        self.brand = brand
        self.warranty = warranty
        self.model = model
    
    def display_product(self):
        """Display electronics product details"""
        return f"{self.name} - Brand: {self.brand}, Model: {self.model}, Price: ₹{self.price}"
    
    def calculate_discount(self):
        """Calculate discount for electronics - 10%"""
        return self.price * 0.10

# Derived Class - Clothing
class Clothing(Product):
    """Clothing product class"""
    
    def __init__(self, product_id, name, price, stock, size, color, material):
        super().__init__(product_id, name, price, stock, "Clothing")
        self.size = size
        self.color = color
        self.material = material
    
    def display_product(self):
        """Display clothing product details"""
        return f"{self.name} - Size: {self.size}, Color: {self.color}, Price: ₹{self.price}"
    
    def calculate_discount(self):
        """Calculate discount for clothing - 20%"""
        return self.price * 0.20

class ProductManager:
    """Manages all product operations"""
    
    def __init__(self, storage):
        self.storage = storage
    
    def add_product(self, name, price, stock, category, brand=None, size=None):
        """Add new product with sequential ID"""
        product_id = get_next_product_id()
        
        product = {
            'product_id': product_id,
            'name': name,
            'price': price,
            'stock': stock,
            'category': category,
            'brand': brand,
            'size': size
        }
        
        products = self.storage.load_products()
        products.append(product)
        self.storage.save_products(products)
        return product_id
    
    def update_product(self, product_id):
        """Update product details"""
        products = self.storage.load_products()
        
        for product in products:
            if product['product_id'] == product_id:
                print("Enter new details (leave blank to keep current):")
                
                name = input(f"Name ({product['name']}): ")
                if name:
                    product['name'] = name
                
                price = input(f"Price (₹{product['price']}): ")
                if price:
                    product['price'] = float(price)
                
                stock = input(f"Stock ({product['stock']}): ")
                if stock:
                    product['stock'] = int(stock)
                
                self.storage.save_products(products)
                return True
        return False
    
    def delete_product(self, product_id):
        """Delete product"""
        products = self.storage.load_products()
        
        for i, product in enumerate(products):
            if product['product_id'] == product_id:
                products.pop(i)
                self.storage.save_products(products)
                return True
        return False
    
    def search_products(self, keyword):
        """Search products by keyword"""
        products = self.storage.load_products()
        keyword = keyword.lower()
        
        results = []
        for product in products:
            if (keyword in product['name'].lower() or 
                keyword in product['category'].lower()):
                results.append(product)
        return results
    
    def recursive_search_by_category(self, category, products=None, index=0):
        """Recursive function to search products by category"""
        if products is None:
            products = self.storage.load_products()
        
        if index >= len(products):
            return []
        
        result = []
        if products[index]['category'].lower() == category.lower():
            result.append(products[index])
        
        result.extend(self.recursive_search_by_category(category, products, index + 1))
        return result
    
    def get_all_products(self):
        """Get all products"""
        return self.storage.load_products()
    
    def get_product(self, product_id):
        """Get product by ID"""
        products = self.storage.load_products()
        
        for product in products:
            if product['product_id'] == product_id:
                return product
        return None
    
    def update_stock(self, product_id, quantity):
        """Update product stock"""
        products = self.storage.load_products()
        
        for product in products:
            if product['product_id'] == product_id:
                if product['stock'] >= quantity:
                    product['stock'] -= quantity
                    self.storage.save_products(products)
                    return True
        return False