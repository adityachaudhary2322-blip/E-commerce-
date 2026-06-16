"""
Utility Functions - Decorators, helper functions, and common utilities
"""

from datetime import datetime
import functools

# Decorator for logging actions
def log_action(func):
    """Decorator to log function calls"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] {datetime.now().strftime('%H:%M:%S')} - Executing: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"[LOG] Completed: {func.__name__}")
        return result
    return wrapper

# Decorator for login required
def login_required(func):
    """Decorator to check if user is logged in"""
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.current_user is None:
            print("❌ Please login first!")
            return None
        return func(self, *args, **kwargs)
    return wrapper

# Tax calculation - static method style
class TaxCalculator:
    """Utility class for tax calculations"""
    
    @staticmethod
    def calculate_tax(amount, tax_rate=0.10):
        """Calculate tax on amount"""
        return amount * tax_rate
    
    @staticmethod
    def calculate_total_with_tax(amount, tax_rate=0.10):
        """Calculate total including tax"""
        return amount + (amount * tax_rate)

# Class method example
class SalesStatistics:
    """Class for generating sales statistics"""
    
    total_sales = 0
    total_orders = 0
    
    @classmethod
    def update_statistics(cls, amount):
        """Update overall sales statistics"""
        cls.total_sales += amount
        cls.total_orders += 1
    
    @classmethod
    def get_statistics(cls):
        """Get current statistics"""
        return {
            'total_sales': cls.total_sales,
            'total_orders': cls.total_orders,
            'average_order': cls.total_sales / cls.total_orders if cls.total_orders > 0 else 0
        }

# Product catalog using tuple for fixed specifications
PRODUCT_CATEGORIES = (
    'Electronics',
    'Clothing',
    'Books',
    'Home & Garden',
    'Sports',
    'Toys'
)

# Generator for invoice generation
def invoice_generator(invoices):
    """Generator to yield invoices one at a time"""
    for invoice in invoices:
        yield invoice

# List comprehension helper - get products in stock
def get_products_in_stock(products):
    """Return list of products with stock > 0 using list comprehension"""
    return [product for product in products if product['stock'] > 0]

# Exception classes
class InvalidProductIDError(Exception):
    """Raised when product ID is invalid"""
    pass

class InvalidLoginError(Exception):
    """Raised when login fails"""
    pass

class ProductOutOfStockError(Exception):
    """Raised when product is out of stock"""
    pass

class InvalidPaymentAmountError(Exception):
    """Raised when payment amount is invalid"""
    pass

class DuplicateUserError(Exception):
    """Raised when user already exists"""
    pass

class FileNotFoundError(Exception):
    """Raised when file is not found"""
    pass

class InvalidInputError(Exception):
    """Raised when user input is invalid"""
    pass

# Exception handler decorator
def handle_exceptions(func):
    """Decorator to handle common exceptions"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except InvalidProductIDError as e:
            print(f"❌ Invalid Product ID: {e}")
        except InvalidLoginError as e:
            print(f"❌ Invalid Login: {e}")
        except ProductOutOfStockError as e:
            print(f"❌ Product Out of Stock: {e}")
        except InvalidPaymentAmountError as e:
            print(f"❌ Invalid Payment Amount: {e}")
        except DuplicateUserError as e:
            print(f"❌ Duplicate User: {e}")
        except FileNotFoundError as e:
            print(f"❌ File Not Found: {e}")
        except InvalidInputError as e:
            print(f"❌ Invalid Input: {e}")
        except Exception as e:
            print(f"❌ Unexpected Error: {e}")
        return None
    return wrapper