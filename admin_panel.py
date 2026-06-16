"""
Simple Tkinter Admin Panel for E-Commerce Portal
- Add products
- Remove products
- Update quantities
- Change prices
All changes automatically reflect on the website
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

# Data directory (same as Flask web app)
DATA_DIR = 'web_data'
PRODUCTS_FILE = os.path.join(DATA_DIR, 'products.json')

def load_products():
    """Load products from JSON file"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    if os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, 'r') as f:
            return json.load(f)
    
    # Sample products if file doesn't exist
    sample_products = [
        {"id": "101", "name": "Gaming Laptop", "price": 89999, "stock": 10, "category": "Electronics", "image": "💻"},
        {"id": "102", "name": "Wireless Mouse", "price": 1299, "stock": 50, "category": "Electronics", "image": "🖱️"},
        {"id": "103", "name": "Cotton T-Shirt", "price": 999, "stock": 100, "category": "Clothing", "image": "👕"},
        {"id": "104", "name": "Studio Headphones", "price": 4999, "stock": 30, "category": "Electronics", "image": "🎧"},
        {"id": "105", "name": "Denim Jeans", "price": 2499, "stock": 40, "category": "Clothing", "image": "👖"},
        {"id": "106", "name": "Doraemon Plush Toy", "price": 1499, "stock": 25, "category": "Toys", "image": "🐱"},
        {"id": "107", "name": "Doraemon Gadget Watch", "price": 2999, "stock": 15, "category": "Accessories", "image": "⌚"},
        {"id": "108", "name": "Doraemon Graphic T-Shirt", "price": 1299, "stock": 35, "category": "Clothing", "image": "👕"},
        {"id": "109", "name": "Pikachu Soft Toy", "price": 1999, "stock": 20, "category": "Toys", "image": "🐭"},
        {"id": "110", "name": "Pikachu Backpack", "price": 3499, "stock": 12, "category": "Bags", "image": "🎒"},
        {"id": "111", "name": "Pikachu Hoodie", "price": 3999, "stock": 18, "category": "Clothing", "image": "👔"},
        {"id": "112", "name": "Niet Anime Bag", "price": 4499, "stock": 10, "category": "Bags", "image": "🎒"},
        {"id": "113", "name": "Dragon Ball Backpack", "price": 3999, "stock": 15, "category": "Bags", "image": "🎒"},
        {"id": "114", "name": "Anime Poster Set", "price": 999, "stock": 50, "category": "Accessories", "image": "🖼️"},
        {"id": "115", "name": "Naruto Headband", "price": 499, "stock": 60, "category": "Accessories", "image": "🎀"}
    ]
    save_products(sample_products)
    return sample_products

def save_products(products):
    """Save products to JSON file"""
    with open(PRODUCTS_FILE, 'w') as f:
        json.dump(products, f, indent=2)

class SimpleAdminPanel:
    """Simple Tkinter Admin Panel"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("ShopIndia - Admin Panel")
        self.root.geometry("1000x600")
        self.root.configure(bg='#f0f0f0')
        
        self.products = []
        self.selected_product_id = None
        
        self.load_data()
        self.create_widgets()
        self.refresh_table()
    
    def load_data(self):
        """Load products from file"""
        self.products = load_products()
    
    def save_data(self):
        """Save products to file"""
        save_products(self.products)
    
    def create_widgets(self):
        """Create UI widgets"""
        
        # Title
        title = tk.Label(self.root, text="🛍️ ShopIndia - Admin Panel", 
                        font=('Arial', 20, 'bold'), bg='#4f46e5', fg='white')
        title.pack(fill='x', pady=0)
        
        # Main frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Left Panel - Add/Edit Product
        left_panel = tk.Frame(main_frame, bg='white', relief='ridge', bd=1)
        left_panel.pack(side='left', fill='y', padx=(0, 20), pady=10)
        
        tk.Label(left_panel, text="Add / Edit Product", font=('Arial', 14, 'bold'),
                bg='white', fg='#4f46e5').pack(pady=10)
        
        # Form fields
        fields_frame = tk.Frame(left_panel, bg='white')
        fields_frame.pack(padx=20, pady=10)
        
        tk.Label(fields_frame, text="Product Name:", font=('Arial', 10), bg='white').grid(row=0, column=0, sticky='w', pady=5)
        self.name_entry = tk.Entry(fields_frame, font=('Arial', 10), width=25)
        self.name_entry.grid(row=0, column=1, pady=5, padx=5)
        
        tk.Label(fields_frame, text="Category:", font=('Arial', 10), bg='white').grid(row=1, column=0, sticky='w', pady=5)
        self.category_entry = tk.Entry(fields_frame, font=('Arial', 10), width=25)
        self.category_entry.grid(row=1, column=1, pady=5, padx=5)
        self.category_entry.insert(0, "Electronics")
        
        tk.Label(fields_frame, text="Price (₹):", font=('Arial', 10), bg='white').grid(row=2, column=0, sticky='w', pady=5)
        self.price_entry = tk.Entry(fields_frame, font=('Arial', 10), width=25)
        self.price_entry.grid(row=2, column=1, pady=5, padx=5)
        
        tk.Label(fields_frame, text="Stock Quantity:", font=('Arial', 10), bg='white').grid(row=3, column=0, sticky='w', pady=5)
        self.stock_entry = tk.Entry(fields_frame, font=('Arial', 10), width=25)
        self.stock_entry.grid(row=3, column=1, pady=5, padx=5)
        
        tk.Label(fields_frame, text="Product ID (auto-generated):", font=('Arial', 9), bg='white', fg='gray').grid(row=4, column=0, sticky='w', pady=5)
        self.id_label = tk.Label(fields_frame, text="New", font=('Arial', 9), bg='white', fg='gray')
        self.id_label.grid(row=4, column=1, sticky='w', pady=5)
        
        # Buttons
        btn_frame = tk.Frame(left_panel, bg='white')
        btn_frame.pack(pady=20)
        
        self.add_btn = tk.Button(btn_frame, text="➕ Add Product", font=('Arial', 11, 'bold'),
                                bg='#4f46e5', fg='white', padx=20, pady=8,
                                command=self.add_product)
        self.add_btn.pack(pady=5)
        
        self.update_btn = tk.Button(btn_frame, text="✏️ Update Selected", font=('Arial', 11, 'bold'),
                                   bg='#f59e0b', fg='white', padx=20, pady=8,
                                   command=self.update_product, state='disabled')
        self.update_btn.pack(pady=5)
        
        # Fixed: Changed '#gray' to '#cccccc' (valid color)
        self.clear_btn = tk.Button(btn_frame, text="🗑️ Clear Form", font=('Arial', 10),
                                  bg='#cccccc', fg='#333', padx=20, pady=5,
                                  command=self.clear_form)
        self.clear_btn.pack(pady=5)
        
        # Right Panel - Product List
        right_panel = tk.Frame(main_frame, bg='white', relief='ridge', bd=1)
        right_panel.pack(side='right', fill='both', expand=True)
        
        tk.Label(right_panel, text="📦 Product List", font=('Arial', 14, 'bold'),
                bg='white', fg='#4f46e5').pack(pady=10)
        
        # Search bar
        search_frame = tk.Frame(right_panel, bg='white')
        search_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(search_frame, text="Search:", font=('Arial', 10), bg='white').pack(side='left')
        self.search_entry = tk.Entry(search_frame, font=('Arial', 10), width=30)
        self.search_entry.pack(side='left', padx=5)
        self.search_entry.bind('<KeyRelease>', self.search_products)
        
        # Treeview (Table)
        table_frame = tk.Frame(right_panel, bg='white')
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('ID', 'Name', 'Category', 'Price', 'Stock', 'Actions')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=18)
        
        self.tree.heading('ID', text='ID')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Category', text='Category')
        self.tree.heading('Price', text='Price (₹)')
        self.tree.heading('Stock', text='Stock')
        self.tree.heading('Actions', text='Actions')
        
        self.tree.column('ID', width=60)
        self.tree.column('Name', width=180)
        self.tree.column('Category', width=100)
        self.tree.column('Price', width=100)
        self.tree.column('Stock', width=80)
        self.tree.column('Actions', width=100)
        
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        # Bottom Status Bar
        self.status_bar = tk.Label(self.root, text="Ready", bd=1, relief='sunken',
                                   anchor='w', font=('Arial', 9), bg='#e0e0e0')
        self.status_bar.pack(side='bottom', fill='x')
    
    def refresh_table(self):
        """Refresh the product table"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for product in self.products:
            self.tree.insert('', 'end', values=(
                product.get('id', ''),
                product.get('name', ''),
                product.get('category', ''),
                f"₹{product.get('price', 0):,}",
                product.get('stock', 0),
                "🗑️ Delete"
            ), tags=(product.get('id', ''),))
        
        self.update_status(f"Loaded {len(self.products)} products")
    
    def search_products(self, event=None):
        """Search products by name"""
        search_term = self.search_entry.get().lower()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        filtered = [p for p in self.products if search_term in p.get('name', '').lower()]
        
        for product in filtered:
            self.tree.insert('', 'end', values=(
                product.get('id', ''),
                product.get('name', ''),
                product.get('category', ''),
                f"₹{product.get('price', 0):,}",
                product.get('stock', 0),
                "🗑️ Delete"
            ), tags=(product.get('id', ''),))
        
        self.update_status(f"Found {len(filtered)} products")
    
    def on_select(self, event):
        """Handle product selection from table"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = selection[0]
        values = self.tree.item(item, 'values')
        if not values:
            return
        
        product_id = values[0]
        # Remove ₹ symbol from price for editing
        price_str = values[3].replace('₹', '').replace(',', '')
        
        product = next((p for p in self.products if p.get('id') == product_id), None)
        
        if product:
            self.selected_product_id = product_id
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, product.get('name', ''))
            self.category_entry.delete(0, tk.END)
            self.category_entry.insert(0, product.get('category', ''))
            self.price_entry.delete(0, tk.END)
            self.price_entry.insert(0, str(product.get('price', 0)))
            self.stock_entry.delete(0, tk.END)
            self.stock_entry.insert(0, str(product.get('stock', 0)))
            self.id_label.config(text=product_id)
            
            self.add_btn.config(state='disabled')
            self.update_btn.config(state='normal')
    
    def clear_form(self):
        """Clear the form"""
        self.name_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.category_entry.insert(0, "Electronics")
        self.price_entry.delete(0, tk.END)
        self.stock_entry.delete(0, tk.END)
        self.id_label.config(text="New")
        self.selected_product_id = None
        
        self.add_btn.config(state='normal')
        self.update_btn.config(state='disabled')
    
    def add_product(self):
        """Add new product"""
        name = self.name_entry.get().strip()
        category = self.category_entry.get().strip()
        price_str = self.price_entry.get().strip()
        stock_str = self.stock_entry.get().strip()
        
        if not all([name, category, price_str, stock_str]):
            messagebox.showerror("Error", "Please fill all fields")
            return
        
        try:
            price = float(price_str)
            stock = int(stock_str)
        except ValueError:
            messagebox.showerror("Error", "Invalid price or stock value")
            return
        
        # Generate new ID
        existing_ids = [int(p.get('id', '100')) for p in self.products if p.get('id', '').isdigit()]
        new_id = str(max(existing_ids, default=100) + 1)
        
        new_product = {
            "id": new_id,
            "name": name,
            "category": category,
            "price": price,
            "stock": stock,
            "image": "📦"
        }
        
        self.products.append(new_product)
        self.save_data()
        self.refresh_table()
        self.clear_form()
        self.update_status(f"Added product: {name} (ID: {new_id})")
        messagebox.showinfo("Success", f"Product '{name}' added! ID: {new_id}")
    
    def update_product(self):
        """Update selected product"""
        if not self.selected_product_id:
            messagebox.showerror("Error", "No product selected")
            return
        
        name = self.name_entry.get().strip()
        category = self.category_entry.get().strip()
        price_str = self.price_entry.get().strip()
        stock_str = self.stock_entry.get().strip()
        
        if not all([name, category, price_str, stock_str]):
            messagebox.showerror("Error", "Please fill all fields")
            return
        
        try:
            price = float(price_str)
            stock = int(stock_str)
        except ValueError:
            messagebox.showerror("Error", "Invalid price or stock value")
            return
        
        # Find and update product
        for product in self.products:
            if product.get('id') == self.selected_product_id:
                product['name'] = name
                product['category'] = category
                product['price'] = price
                product['stock'] = stock
                break
        
        self.save_data()
        self.refresh_table()
        self.clear_form()
        self.update_status(f"Updated product: {name}")
        messagebox.showinfo("Success", f"Product '{name}' updated!")
    
    def delete_product(self, product_id):
        """Delete a product"""
        product = next((p for p in self.products if p.get('id') == product_id), None)
        if messagebox.askyesno("Confirm Delete", f"Delete product '{product.get('name')}'?"):
            self.products = [p for p in self.products if p.get('id') != product_id]
            self.save_data()
            self.refresh_table()
            self.clear_form()
            self.update_status(f"Deleted product: {product.get('name', product_id)}")
            messagebox.showinfo("Success", "Product deleted!")
    
    def update_status(self, message):
        """Update status bar"""
        self.status_bar.config(text=f" {datetime.now().strftime('%H:%M:%S')} - {message}")
        self.root.update_idletasks()


def main():
    root = tk.Tk()
    app = SimpleAdminPanel(root)
    
    # Bind delete action to click on Actions column
    def on_tree_click(event):
        region = app.tree.identify_region(event.x, event.y)
        if region == "cell":
            column = app.tree.identify_column(event.x)
            if column == '#6':  # Actions column
                item = app.tree.identify_row(event.y)
                if item:
                    values = app.tree.item(item, 'values')
                    if values:
                        product_id = values[0]
                        app.delete_product(product_id)
    
    app.tree.bind('<ButtonRelease-1>', on_tree_click)
    
    root.mainloop()

if __name__ == "__main__":
    main()