import os
import pymysql

class Database:
    def __init__(self):
        self.connection = pymysql.connect(host=os.getenv('MYSQL_HOST'),
                                          user=os.getenv('MYSQL_USER'),
                                          password=os.getenv('MYSQL_PASSWORD'),
                                          database=os.getenv('MYSQL_DATABASE'),
                                          cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                id_usuario INT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                pedido_producto_id INT,
                id_pedido INT,
                id_producto INT,
                cantidad INT
            )
            """
        )
        self.connection.commit()

    def list_orders(self):
        self.cursor.execute("SELECT * FROM orders")
        return self.cursor.fetchall()

    def add_order(self, id_usuario, pedido_producto_id, id_pedido, id_producto, cantidad):
        sql = "INSERT INTO orders (id_usuario, pedido_producto_id, id_pedido, id_producto, cantidad) VALUES (%s, %s, %s, %s, %s)"
        values = (id_usuario, pedido_producto_id, id_pedido, id_producto, cantidad)
        self.cursor.execute(sql, values)
        self.connection.commit()
        return True

