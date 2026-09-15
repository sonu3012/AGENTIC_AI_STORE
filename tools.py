import sqlite3


DB_PATH = "data/store.db"


# --------------------------------------------------
# TOOL 1: Get order details
# --------------------------------------------------

def get_order(order_id):

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            order_id,
            product_id,
            quantity,
            status,
            expected_delivery
        FROM orders
        WHERE order_id = ?
    """, (order_id,))

    order = cursor.fetchone()

    connection.close()

    if order is None:
        return {
            "success": False,
            "message": "Order not found"
        }

    return {
        "success": True,
        "order_id": order[0],
        "product_id": order[1],
        "quantity": order[2],
        "status": order[3],
        "expected_delivery": order[4]
    }


# --------------------------------------------------
# TOOL 2: Search products
# --------------------------------------------------

def search_products(query):

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    search_term = f"%{query}%"

    cursor.execute("""
        SELECT
            product_id,
            name,
            category,
            price,
            stock,
            description
        FROM products
        WHERE
            name LIKE ?
            OR category LIKE ?
            OR description LIKE ?
    """, (search_term, search_term, search_term))

    products = cursor.fetchall()

    connection.close()

    if not products:
        return {
            "success": False,
            "message": "No products found"
        }

    results = []

    for product in products:
        results.append({
            "product_id": product[0],
            "name": product[1],
            "category": product[2],
            "price": product[3],
            "stock": product[4],
            "description": product[5]
        })

    return {
        "success": True,
        "products": results
    }


# --------------------------------------------------
# TOOL 3: Get product details
# --------------------------------------------------

def get_product(product_id):

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            product_id,
            name,
            category,
            price,
            stock,
            description
        FROM products
        WHERE product_id = ?
    """, (product_id,))

    product = cursor.fetchone()

    connection.close()

    if product is None:
        return {
            "success": False,
            "message": "Product not found"
        }

    return {
        "success": True,
        "product_id": product[0],
        "name": product[1],
        "category": product[2],
        "price": product[3],
        "stock": product[4],
        "description": product[5]
    }


# --------------------------------------------------
# TEST ALL TOOLS
# --------------------------------------------------

if __name__ == "__main__":

    print("\n--- TEST 1: GET ORDER ---")

    print(get_order("ORD-1002"))

    print("\n--- TEST 2: INVALID ORDER ---")

    print(get_order("ORD-9999"))

    print("\n--- TEST 3: SEARCH PRODUCTS ---")

    print(search_products("shoes"))

    print("\n--- TEST 4: EMPTY SEARCH ---")

    print(search_products("laptop"))

    print("\n--- TEST 5: GET PRODUCT ---")

    print(get_product("P101"))

    print("\n--- TEST 6: INVALID PRODUCT ---")

    print(get_product("P999"))