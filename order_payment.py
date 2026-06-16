"""
Order and Payment Management Module
"""

from datetime import datetime
import uuid

class OrderManager:
    """Manages order operations"""
    
    def __init__(self, storage):
        self.storage = storage
    
    def place_order(self, user_id, cart, payment_mode):
        """Place a new order"""
        if not cart['products']:
            return None
        
        order_id = str(uuid.uuid4())[:8]
        
        order = {
            'order_id': order_id,
            'user_id': user_id,
            'products': cart['products'].copy(),
            'order_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'order_status': 'Pending',
            'total_amount': cart['total_amount'],
            'payment_mode': payment_mode
        }
        
        # Update stock
        for item in cart['products']:
            self.storage.update_product_stock(item['product_id'], item['quantity'])
        
        # Save order
        orders = self.storage.load_orders()
        orders.append(order)
        self.storage.save_orders(orders)
        
        # Update user order history
        users = self.storage.load_users()
        for user in users:
            if user['user_id'] == user_id:
                user['order_history'].append(order_id)
                self.storage.save_users(users)
                break
        
        return order
    
    def cancel_order(self, order_id, user_id):
        """Cancel an order"""
        orders = self.storage.load_orders()
        
        for order in orders:
            if order['order_id'] == order_id and order['user_id'] == user_id:
                if order['order_status'] == 'Delivered':
                    return False
                
                order['order_status'] = 'Cancelled'
                self.storage.save_orders(orders)
                return True
        return False
    
    def track_order(self, order_id, user_id):
        """Track order status"""
        orders = self.storage.load_orders()
        
        for order in orders:
            if order['order_id'] == order_id and order['user_id'] == user_id:
                return order['order_status']
        return None
    
    def get_order_details(self, order_id, user_id):
        """Get order details"""
        orders = self.storage.load_orders()
        
        for order in orders:
            if order['order_id'] == order_id and order['user_id'] == user_id:
                return order
        return None
    
    def get_user_orders(self, user_id):
        """Get all orders for a user"""
        orders = self.storage.load_orders()
        user_orders = []
        
        for order in orders:
            if order['user_id'] == user_id:
                user_orders.append(order)
        
        # Sort orders by date using lambda
        user_orders.sort(key=lambda x: x['order_date'], reverse=True)
        return user_orders
    
    def update_order_status(self, order_id, status):
        """Update order status"""
        orders = self.storage.load_orders()
        
        for order in orders:
            if order['order_id'] == order_id:
                order['order_status'] = status
                self.storage.save_orders(orders)
                return True
        return False

class PaymentManager:
    """Manages payment operations"""
    
    def __init__(self, storage):
        self.storage = storage
    
    def process_payment(self, order_id, amount, payment_mode):
        """Process payment for an order"""
        # Validate payment amount
        if amount <= 0:
            print("Invalid payment amount!")
            return None
        
        payment_id = str(uuid.uuid4())[:8]
        
        payment = {
            'payment_id': payment_id,
            'order_id': order_id,
            'payment_mode': payment_mode,
            'payment_status': 'Completed',
            'amount': amount,
            'payment_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        payments = self.storage.load_payments()
        payments.append(payment)
        self.storage.save_payments(payments)
        
        # Update order status
        orders = self.storage.load_orders()
        for order in orders:
            if order['order_id'] == order_id:
                order['order_status'] = 'Paid'
                self.storage.save_orders(orders)
                break
        
        return payment
    
    def verify_payment(self, payment_id):
        """Verify payment status"""
        payments = self.storage.load_payments()
        
        for payment in payments:
            if payment['payment_id'] == payment_id:
                return payment['payment_status']
        return None
    
    def generate_receipt(self, payment_id):
        """Generate payment receipt"""
        payments = self.storage.load_payments()
        
        for payment in payments:
            if payment['payment_id'] == payment_id:
                receipt = f"""
                ====================
                PAYMENT RECEIPT
                ====================
                Payment ID: {payment['payment_id']}
                Order ID: {payment['order_id']}
                Amount: ₹{payment['amount']}
                Mode: {payment['payment_mode']}
                Status: {payment['payment_status']}
                Date: {payment['payment_date']}
                ====================
                """
                return receipt
        return None
    
    def get_payment_history(self, user_id):
        """Get payment history for a user"""
        orders = self.storage.load_orders()
        payments = self.storage.load_payments()
        
        user_order_ids = [order['order_id'] for order in orders if order['user_id'] == user_id]
        
        history = []
        for payment in payments:
            if payment['order_id'] in user_order_ids:
                history.append(payment)
        
        return history