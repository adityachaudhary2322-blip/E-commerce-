"""
Invoice and Reports Management Module
"""

from datetime import datetime
import uuid
import csv
import os

class InvoiceManager:
    """Manages invoice operations"""
    
    def __init__(self, storage):
        self.storage = storage
    
    def generate_invoice(self, order_id, order):
        """Generate invoice for an order"""
        invoice_id = str(uuid.uuid4())[:8]
        
        invoice = {
            'invoice_id': invoice_id,
            'order_id': order_id,
            'invoice_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'total_amount': order['total_amount'],
            'products': order['products'],
            'user_id': order['user_id']
        }
        
        invoices = self.storage.load_invoices()
        invoices.append(invoice)
        self.storage.save_invoices(invoices)
        
        return invoice
    
    def get_invoice(self, invoice_id):
        """Get invoice by ID"""
        invoices = self.storage.load_invoices()
        
        for invoice in invoices:
            if invoice['invoice_id'] == invoice_id:
                return invoice
        return None
    
    def get_order_invoice(self, order_id):
        """Get invoice for an order"""
        invoices = self.storage.load_invoices()
        
        for invoice in invoices:
            if invoice['order_id'] == order_id:
                return invoice
        return None
    
    def export_invoice(self, invoice):
        """Export invoice to CSV file"""
        filename = f"reports/invoice_{invoice['invoice_id']}.csv"
        
        # Ensure reports directory exists
        os.makedirs('reports', exist_ok=True)
        
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['INVOICE'])
            writer.writerow(['Invoice ID:', invoice['invoice_id']])
            writer.writerow(['Order ID:', invoice['order_id']])
            writer.writerow(['Date:', invoice['invoice_date']])
            writer.writerow(['Total Amount:', f"${invoice['total_amount']}"])
            writer.writerow([])
            writer.writerow(['Product Name', 'Quantity', 'Price', 'Subtotal'])
            
            for product in invoice['products']:
                writer.writerow([product['name'], product['quantity'], 
                               f"${product['price']}", f"${product['subtotal']}"])
        
        print(f"Invoice exported to: {filename}")

class ReportGenerator:
    """Generates various reports"""
    
    def __init__(self, storage):
        self.storage = storage
    
    def generate_sales_report(self):
        """Generate sales report CSV"""
        orders = self.storage.load_orders()
        payments = self.storage.load_payments()
        
        filename = "reports/sales_report.csv"
        os.makedirs('reports', exist_ok=True)
        
        # Calculate total sales
        total_sales = sum(payment['amount'] for payment in payments)
        
        # Count orders by status using list comprehension
        order_statuses = [order['order_status'] for order in orders]
        pending_count = len([s for s in order_statuses if s == 'Pending'])
        paid_count = len([s for s in order_statuses if s == 'Paid'])
        delivered_count = len([s for s in order_statuses if s == 'Delivered'])
        cancelled_count = len([s for s in order_statuses if s == 'Cancelled'])
        
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['SALES REPORT'])
            writer.writerow(['Generated:', datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
            writer.writerow(['Total Sales:', f"${total_sales}"])
            writer.writerow(['Total Orders:', len(orders)])
            writer.writerow([])
            writer.writerow(['Order Status Summary'])
            writer.writerow(['Status', 'Count'])
            writer.writerow(['Pending', pending_count])
            writer.writerow(['Paid', paid_count])
            writer.writerow(['Delivered', delivered_count])
            writer.writerow(['Cancelled', cancelled_count])
            writer.writerow([])
            writer.writerow(['Recent Orders'])
            writer.writerow(['Order ID', 'Date', 'Amount', 'Status'])
            
            # Sort orders by date using lambda
            sorted_orders = sorted(orders, key=lambda x: x['order_date'], reverse=True)
            for order in sorted_orders[:10]:  # Show last 10 orders
                writer.writerow([order['order_id'], order['order_date'], 
                               f"${order['total_amount']}", order['order_status']])
        
        print(f"Sales report generated: {filename}")
    
    def generate_order_report(self):
        """Generate order report CSV"""
        orders = self.storage.load_orders()
        
        filename = "reports/order_report.csv"
        os.makedirs('reports', exist_ok=True)
        
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ORDER REPORT'])
            writer.writerow(['Generated:', datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
            writer.writerow([])
            writer.writerow(['Order ID', 'User ID', 'Date', 'Total Amount', 'Status', '# Products'])
            
            for order in orders:
                writer.writerow([order['order_id'], order['user_id'], 
                               order['order_date'], f"${order['total_amount']}", 
                               order['order_status'], len(order['products'])])
        
        print(f"Order report generated: {filename}")
    
    def generate_inventory_report(self):
        """Generate inventory report CSV"""
        products = self.storage.load_products()
        
        filename = "reports/inventory_report.csv"
        os.makedirs('reports', exist_ok=True)
        
        # Get unique categories using set
        categories = set(product['category'] for product in products)
        
        # Calculate total stock value
        total_value = sum(product['price'] * product['stock'] for product in products)
        
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['INVENTORY REPORT'])
            writer.writerow(['Generated:', datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
            writer.writerow(['Total Products:', len(products)])
            writer.writerow(['Total Inventory Value:', f"${total_value}"])
            writer.writerow(['Categories:', ', '.join(categories)])
            writer.writerow([])
            writer.writerow(['Product ID', 'Name', 'Category', 'Price', 'Stock', 'Value'])
            
            # Sort products by price using lambda
            sorted_products = sorted(products, key=lambda x: x['price'], reverse=True)
            
            for product in sorted_products:
                value = product['price'] * product['stock']
                writer.writerow([product['product_id'], product['name'], 
                               product['category'], f"${product['price']}", 
                               product['stock'], f"${value}"])
            
            writer.writerow([])
            writer.writerow(['Low Stock Items (< 10 units)'])
            low_stock = [p for p in products if p['stock'] < 10]
            for product in low_stock:
                writer.writerow([product['name'], f"Stock: {product['stock']}"])
        
        print(f"Inventory report generated: {filename}")