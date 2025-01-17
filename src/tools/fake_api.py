import sqlite3
import os

# Inicializar la base de datos y las tablas necesarias
def init_db(db_dir="src/data"):
    """
    Crea la base de datos y las tablas necesarias si no existen.

    Args:
        db_dir (str): Directorio donde se guardará la base de datos.
    """
    # Asegurarse de que el directorio existe
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    # Ruta completa de la base de datos
    db_path = os.path.join(db_dir, "inventory.db")

    # Conectar a la base de datos
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Tabla de inventario
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL
        )
    """)

    # Tabla de compras
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            date TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

def add_purchase(product_name, quantity, price):
    """
    Registra una compra y actualiza el inventario.
    
    Parámetros:
        product_name (str): Nombre del producto comprado.
        quantity (int): Cantidad comprada.
        price (float): Precio unitario del producto.
    
    Retorno:
        dict: Mensaje de confirmación con los detalles de la compra.
    """
    conn = sqlite3.connect("src/data/inventory.db")
    cursor = conn.cursor()

    # Registrar la compra
    cursor.execute("""
        INSERT INTO purchases (product_name, quantity, price)
        VALUES (?, ?, ?)
    """, (product_name.upper(), quantity, price))

    # Verificar si el producto ya existe en el inventario
    cursor.execute("SELECT id, quantity FROM products WHERE name = ?", (product_name.upper(),))
    product = cursor.fetchone()

    if product:
        # Actualizar la cantidad y el precio en el inventario
        product_id, current_quantity = product
        new_quantity = current_quantity + quantity
        cursor.execute("""
            UPDATE products
            SET quantity = ?, price = ?
            WHERE id = ?
        """, (new_quantity, price, product_id))
    else:
        # Agregar un nuevo producto al inventario
        cursor.execute("""
            INSERT INTO products (name, quantity, price)
            VALUES (?, ?, ?)
        """, (product_name.upper(), quantity, price))

    conn.commit()
    conn.close()
    
    return {"message": "Purchase added and inventory updated", "product": product_name, "quantity": quantity, "price": price}

def get_all_purchases():
    """
    Devuelve todas las compras realizadas.

    Retorno:
        list: Lista de diccionarios con los detalles de las compras.
    """
    conn = sqlite3.connect("src/data/inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, product_name, quantity, price, date FROM purchases")
    rows = cursor.fetchall()
    conn.close()

    return [{"id": row[0], "product_name": row[1], "quantity": row[2], "price": row[3], "date": row[4]} for row in rows]

def search_product_by_name(product_name):
    """
    Busca un producto por su nombre en el inventario.
    
    Parámetros:
        product_name (str): Nombre del producto a buscar.

    Retorno:
        dict: Detalles del producto si existe, o un mensaje indicando que no se encontró.
    """
    conn = sqlite3.connect("src/data/inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, quantity, price FROM products WHERE name = ?", (product_name,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {"id": row[0], "name": row[1], "quantity": row[2], "price": row[3]}
    else:
        return {"error": "Product not found"}

def fake_request(method, url, data=None):
    """
    Simula una solicitud HTTP para interactuar con el sistema de compras.

    Parámetros:
        method (str): Método HTTP simulado ('GET' o 'POST').
        url (str): Ruta del recurso, como '/purchases' o '/purchases/add'.
        data (dict, opcional): Datos enviados en el cuerpo de la solicitud (solo para POST).

    Retorno:
        dict o list: Respuesta simulada basada en el método y la ruta proporcionados.
    """
    if method == "GET":
        if url == "/purchases":
            return get_all_purchases()
        elif url.startswith("/products/search/"):
            product_name = url.split("/")[-1].replace("%20", " ").upper()  # Reemplazar espacios codificados
            return search_product_by_name(product_name)
        else:
            return {"error": "Invalid endpoint"}
    elif method == "POST":
        if url == "/purchases/add" and data:
            return add_purchase(data["product_name"], data["quantity"], data["price"])
        else:
            return {"error": "Invalid request or missing data"}
    else:
        return {"error": "Unsupported method"}