"""
E-COMMERCE SHOPPING PORTAL - Main Entry Point
"""

from user_management import UserManager
from product_management import ProductManager
from cart_wishlist import CartManager, WishlistManager
from order_payment import OrderManager, PaymentManager
from invoice_reports import InvoiceManager, ReportGenerator
from data_storage import DataStorage
from utils import login_required, log_action
from datetime import datetime
import time

class EcommercePortal:
    """Main application class"""
    
    def __init__(self):
        self.storage = DataStorage()
        self.user_manager = UserManager(self.storage)
        self.product_manager = ProductManager(self.storage)
        self.cart_manager = CartManager(self.storage)
        self.wishlist_manager = WishlistManager(self.storage)
        self.order_manager = OrderManager(self.storage)
        self.payment_manager = PaymentManager(self.storage)
        self.invoice_manager = InvoiceManager(self.storage)
        self.report_generator = ReportGenerator(self.storage)
        self.current_user = None
    
    def wait_for_user(self):
        """Wait for user to press Enter"""
        input("\nPress Enter to continue...")
    
    def register_user(self):
        """Register a new user"""
        print("\n=== USER REGISTRATION ===")
        
        name = input("Enter Name: ")
        email = input("Enter Email: ")
        password = input("Enter Password: ")
        
        user_id = self.user_manager.register(name, email, password)
        if user_id:
            print(f"✅ Registration successful! Your User ID is: {user_id}")
        else:
            print("❌ Registration failed! Email may already exist.")
        
        self.wait_for_user()
    
    def login_user(self):
        """Login existing user"""
        print("\n=== USER LOGIN ===")
        
        email = input("Enter Email: ")
        password = input("Enter Password: ")
        
        user = self.user_manager.login(email, password)
        if user:
            self.current_user = user
            print(f"✅ Welcome back, {user['name']}!")
            self.wait_for_user()
            return True
        else:
            print("❌ Invalid email or password!")
            self.wait_for_user()
            return False
    
    @login_required
    def view_profile(self):
        """View current user profile"""
        print("\n=== USER PROFILE ===")
        print(f"User ID: {self.current_user['user_id']}")
        print(f"Name: {self.current_user['name']}")
        print(f"Email: {self.current_user['email']}")
        print(f"Member Since: {self.current_user['registered_date']}")
        self.wait_for_user()
    
    @login_required
    def view_order_history(self):
        """View user's order history"""
        print("\n=== ORDER HISTORY ===")
        orders = self.order_manager.get_user_orders(self.current_user['user_id'])
        
        if not orders:
            print("No orders found.")
        else:
            for order in orders:
                print(f"Order #{order['order_id']} | Date: {order['order_date']} | Status: {order['order_status']} | Total: ₹{order['total_amount']}")
        
        self.wait_for_user()
    
    @login_required
    def view_all_products(self):
        """View all products"""
        products = self.product_manager.get_all_products()
        if products:
            print("\n" + "="*75)
            print("                ALL PRODUCTS (Prices in ₹)")
            print("="*75)
            print(f"{'ID':<6} {'Name':<25} {'Price':<12} {'Stock':<8} {'Category':<12}")
            print("-"*75)
            for product in products:
                print(f"{product['product_id']:<6} {product['name']:<25} ₹{product['price']:<11} {product['stock']:<8} {product['category']:<12}")
            print("="*75)
        else:
            print("\n❌ No products available!")
        
        self.wait_for_user()
    
    @login_required
    def add_product(self):
        """Add new product"""
        print("\n--- Add New Product ---")
        name = input("Product Name: ")
        price = float(input("Price (₹): "))
        stock = int(input("Stock Quantity: "))
        category = input("Category (Electronics/Clothing/Toys/Bags/Accessories): ")
        
        product_id = self.product_manager.add_product(name, price, stock, category)
        if product_id:
            print(f"✅ Product added! Product ID: {product_id}")
        else:
            print("❌ Failed to add product!")
        
        self.wait_for_user()
    
    @login_required
    def add_to_cart(self):
        """Add product to cart"""
        self.view_all_products()
        product_id = input("\nEnter Product ID to add: ")
        quantity = int(input("Enter quantity: "))
        
        if self.cart_manager.add_to_cart(self.current_user['user_id'], product_id, quantity):
            print("✅ Product added to cart!")
        else:
            print("❌ Failed to add product!")
        
        self.wait_for_user()
    
    @login_required
    def view_cart(self):
        """View shopping cart"""
        print("\n=== SHOPPING CART ===")
        cart = self.cart_manager.get_cart(self.current_user['user_id'])
        
        if cart['products']:
            print("\n" + "-"*45)
            for item in cart['products']:
                print(f"  {item['name']}")
                print(f"    Quantity: {item['quantity']} x ₹{item['price']} = ₹{item['subtotal']}")
            print("-"*45)
            print(f"  TOTAL AMOUNT: ₹{cart['total_amount']}")
            print("-"*45)
        else:
            print("Cart is empty!")
        
        self.wait_for_user()
    
    @login_required
    def add_to_wishlist(self):
        """Add product to wishlist"""
        self.view_all_products()
        product_id = input("\nEnter Product ID to add to wishlist: ")
        
        if self.wishlist_manager.add_to_wishlist(self.current_user['user_id'], product_id):
            print("✅ Product added to wishlist!")
        else:
            print("❌ Failed to add to wishlist!")
        
        self.wait_for_user()
    
    @login_required
    def view_wishlist(self):
        """View wishlist"""
        print("\n=== WISHLIST ===")
        wishlist = self.wishlist_manager.get_wishlist(self.current_user['user_id'])
        
        if wishlist['products']:
            print("\n" + "-"*40)
            for i, item in enumerate(wishlist['products'], 1):
                print(f"  {i}. {item['name']} - ₹{item['price']}")
            print("-"*40)
            
            move = input("\nMove any item to cart? Enter Product ID (or press Enter to skip): ")
            if move:
                if self.wishlist_manager.move_to_cart(self.current_user['user_id'], move, self.cart_manager):
                    print("✅ Moved to cart!")
                else:
                    print("❌ Failed to move!")
        else:
            print("Wishlist is empty!")
        
        self.wait_for_user()
    
    @login_required
    def place_order(self):
        """Place a new order"""
        print("\n=== PLACE ORDER ===")
        cart = self.cart_manager.get_cart(self.current_user['user_id'])
        
        if not cart['products']:
            print("Cart is empty! Cannot place order.")
            self.wait_for_user()
            return
        
        print(f"Total Amount: ₹{cart['total_amount']}")
        
        confirm = input("Confirm order? (y/n): ")
        if confirm.lower() != 'y':
            print("Order cancelled.")
            self.wait_for_user()
            return
        
        print("\n--- Payment Details ---")
        print("1. Credit Card")
        print("2. Debit Card")
        print("3. UPI")
        print("4. Cash on Delivery")
        
        payment_mode = input("Select payment mode: ")
        payment_modes = {'1': 'Credit Card', '2': 'Debit Card', '3': 'UPI', '4': 'COD'}
        mode = payment_modes.get(payment_mode, 'COD')
        
        order = self.order_manager.place_order(self.current_user['user_id'], cart, mode)
        
        if order:
            print(f"\n✅ Order placed successfully!")
            print(f"Order ID: {order['order_id']}")
            
            payment = self.payment_manager.process_payment(order['order_id'], cart['total_amount'], mode)
            if payment:
                print(f"✅ Payment processed! Payment ID: {payment['payment_id']}")
                
                invoice = self.invoice_manager.generate_invoice(order['order_id'], order)
                if invoice:
                    print(f"✅ Invoice generated! Invoice ID: {invoice['invoice_id']}")
                    self.cart_manager.clear_cart(self.current_user['user_id'])
                    print("\n🎉 Thank you for your purchase!")
            else:
                print("❌ Payment failed!")
        else:
            print("❌ Failed to place order!")
        
        self.wait_for_user()
    
    @login_required
    def track_order(self):
        """Track order status"""
        order_id = input("Enter Order ID: ")
        status = self.order_manager.track_order(order_id, self.current_user['user_id'])
        
        if status:
            print(f"\nOrder #{order_id} Status: {status}")
        else:
            print("Order not found!")
        
        self.wait_for_user()
    
    @login_required
    def cancel_order(self):
        """Cancel an order"""
        order_id = input("Enter Order ID to cancel: ")
        
        if self.order_manager.cancel_order(order_id, self.current_user['user_id']):
            print("✅ Order cancelled successfully!")
        else:
            print("❌ Cannot cancel order! Order may be already delivered or not found.")
        
        self.wait_for_user()
    
    @login_required
    def view_order_details(self):
        """View order details"""
        order_id = input("Enter Order ID: ")
        order = self.order_manager.get_order_details(order_id, self.current_user['user_id'])
        
        if order:
            print(f"\n=== ORDER DETAILS ===")
            print(f"Order ID: {order['order_id']}")
            print(f"Date: {order['order_date']}")
            print(f"Status: {order['order_status']}")
            print(f"Total Amount: ₹{order['total_amount']}")
            print("\nProducts:")
            for product in order['products']:
                print(f"  {product['name']} x{product['quantity']} = ₹{product['subtotal']}")
        else:
            print("Order not found!")
        
        self.wait_for_user()
    
    @login_required
    def generate_invoice(self):
        """Generate invoice for an order"""
        order_id = input("Enter Order ID: ")
        order = self.order_manager.get_order_details(order_id, self.current_user['user_id'])
        
        if order:
            invoice = self.invoice_manager.generate_invoice(order_id, order)
            if invoice:
                print(f"\n✅ Invoice Generated!")
                print(f"Invoice ID: {invoice['invoice_id']}")
                print(f"Invoice Date: {invoice['invoice_date']}")
                print(f"Total Amount: ₹{invoice['total_amount']}")
        else:
            print("Order not found!")
        
        self.wait_for_user()
    
    def save_data(self):
        """Save all data to files"""
        self.storage.save_all_data()
        print("✅ All data saved!")
    
    def load_data(self):
        """Load all data from files"""
        self.storage.load_all_data()
        print("✅ Data loaded!")
    
    def run(self):
        """Main application loop"""
        print("=" * 50)
        print("   WELCOME TO E-COMMERCE SHOPPING PORTAL")
        print("=" * 50)
        
        # Load data
        self.load_data()
        
        # Add sample products with FUN ITEMS if none exist
        if not self.product_manager.get_all_products():
            print("\n📦 Adding awesome products...")
            
            # Regular items
            self.product_manager.add_product("Laptop", 89999, 10, "Electronics")
            self.product_manager.add_product("Mouse", 1299, 50, "Electronics")
            self.product_manager.add_product("T-Shirt", 999, 100, "Clothing")
            self.product_manager.add_product("Headphones", 4999, 30, "Electronics")
            self.product_manager.add_product("Jeans", 2499, 40, "Clothing")
            
            # FUN ITEMS - Doraemon
            self.product_manager.add_product("Doraemon Plush Toy", 1499, 25, "Toys")
            self.product_manager.add_product("Doraemon Gadget Watch", 2999, 15, "Accessories")
            self.product_manager.add_product("Doraemon T-Shirt", 1299, 35, "Clothing")
            
            # FUN ITEMS - Pikachu
            self.product_manager.add_product("Pikachu Soft Toy", 1999, 20, "Toys")
            self.product_manager.add_product("Pikachu Backpack", 3499, 12, "Bags")
            self.product_manager.add_product("Pikachu Hoodie", 3999, 18, "Clothing")
            
            # Anime Bags & Accessories
            self.product_manager.add_product("Niet_ECE_Bag", 154499, 10, "Bags")
            self.product_manager.add_product("Dragon Ball Z Backpack", 3999, 15, "Bags")
            self.product_manager.add_product("Anime Poster Set", 999, 50, "Accessories")
            self.product_manager.add_product("Naruto Headband", 499, 60, "Accessories")
            
            print("✅ 15 products added! (Including Doraemon, Pikachu & Anime items)")
            print("   All prices in Indian Rupees (₹)")
            time.sleep(2)
        
        while True:
            if not self.current_user:
                print("\n" + "="*40)
                print("        MAIN MENU")
                print("="*40)
                print("1. Register")
                print("2. Login")
                print("3. Exit")
                print("="*40)
                
                choice = input("Enter choice: ").strip()
                
                if choice == '1':
                    self.register_user()
                elif choice == '2':
                    self.login_user()
                elif choice == '3':
                    self.save_data()
                    print("\n👋 Thank you for visiting! Goodbye!")
                    break
                else:
                    print("❌ Invalid choice! Please enter 1, 2, or 3.")
                    time.sleep(1)
            else:
                print("\n" + "="*50)
                print(f"   MAIN MENU - Logged in as: {self.current_user['name']}")
                print("="*50)
                print("1.  👤 View Profile")
                print("2.  📜 View Order History")
                print("3.  📦 View All Products")
                print("4.  ➕ Add Product")
                print("5.  🛒 Add to Cart")
                print("6.  🛍️ View Cart")
                print("7.  💝 Add to Wishlist")
                print("8.  ❤️ View Wishlist")
                print("9.  💰 Place Order")
                print("10. 📍 Track Order")
                print("11. ❌ Cancel Order")
                print("12. 📄 View Order Details")
                print("13. 🧾 Generate Invoice")
                print("14. 💾 Save Data")
                print("15. 🚪 Logout")
                print("16. ❌ Exit")
                print("="*50)
                
                choice = input("Enter choice (1-16): ").strip()
                
                if choice == '1':
                    self.view_profile()
                elif choice == '2':
                    self.view_order_history()
                elif choice == '3':
                    self.view_all_products()
                elif choice == '4':
                    self.add_product()
                elif choice == '5':
                    self.add_to_cart()
                elif choice == '6':
                    self.view_cart()
                elif choice == '7':
                    self.add_to_wishlist()
                elif choice == '8':
                    self.view_wishlist()
                elif choice == '9':
                    self.place_order()
                elif choice == '10':
                    self.track_order()
                elif choice == '11':
                    self.cancel_order()
                elif choice == '12':
                    self.view_order_details()
                elif choice == '13':
                    self.generate_invoice()
                elif choice == '14':
                    self.save_data()
                    self.wait_for_user()
                elif choice == '15':
                    self.current_user = None
                    print("✅ Logged out successfully!")
                    self.wait_for_user()
                elif choice == '16':
                    self.save_data()
                    print("\n👋 Thank you for visiting! Goodbye!")
                    break
                else:
                    print("❌ Invalid choice! Please enter a number between 1 and 16.")
                    time.sleep(1)

if __name__ == "__main__":
    portal = EcommercePortal()
    portal.run()