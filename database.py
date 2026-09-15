import sqlite3
import os


# Database location
DB_PATH = "data/store.db"


def create_database():
    # Create data folder if it doesn't exist
    os.makedirs("data", exist_ok=True)

    # Connect to SQLite database
    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    # Create products table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL,
            description TEXT
        )
    """)

    # Create orders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            product_id TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            status TEXT NOT NULL,
            expected_delivery TEXT,
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    """)

    # Sample products
    products = [
        (
            "P101",
            "Nike Running Shoes",
            "shoes",
            2999,
            15,
            "Comfortable running shoes for daily use"
        ),
        (
            "P102",
            "Adidas Sports Shoes",
            "shoes",
            2499,
            10,
            "Lightweight sports shoes"
        ),
        (
            "P103",
            "Puma Casual Shoes",
            "shoes",
            1999,
            20,
            "Casual shoes for everyday wear"
        ),
        (
            "P104",
            "Men's Cotton T-Shirt",
            "clothing",
            799,
            30,
            "Comfortable cotton t-shirt"
        ),
        (
            "P105",
            "Blue Denim Jeans",
            "clothing",
            1499,
            12,
            "Regular fit blue denim jeans"
        )
    ]

    # Insert products
    cursor.executemany("""
        INSERT OR IGNORE INTO products
        (product_id, name, category, price, stock, description)
        VALUES (?, ?, ?, ?, ?, ?)
    """, products)

    # Sample orders
    orders = [
        (
            "ORD-1001",
            "P101",
            1,
            "Delivered",
            "2026-09-05"
        ),
        (
            "ORD-1002",
            "P101",
            1,
            "Shipped",
            "2026-09-15"
        ),
        (
            "ORD-1003",
            "P104",
            2,
            "Processing",
            "2026-09-18"
        ),
        (
            "ORD-1004",
            "P105",
            1,
            "Delivered",
            "2026-09-02"
        )
    ]

    # Insert orders
    cursor.executemany("""
        INSERT OR IGNORE INTO orders
        (order_id, product_id, quantity, status, expected_delivery)
        VALUES (?, ?, ?, ?, ?)
    """, orders)

    connection.commit()
    connection.close()

    print("Database created successfully!")


if __name__ == "__main__":
    create_database()

    