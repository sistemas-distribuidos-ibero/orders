import os
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from database import Database

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configuración de la aplicación Flask
app = Flask(__name__)
db = Database()

# Definición del modelo de Pedido
class Order:
    def __init__(self, id, id_usuario, timestamp, pedido_producto, id_pedido, id_producto, cantidad):
        self.id = id
        self.id_usuario = id_usuario
        self.timestamp = timestamp
        self.pedido_producto = pedido_producto
        self.id_pedido = id_pedido
        self.id_producto = id_producto
        self.cantidad = cantidad

@app.route('/')
def welcome():
    return 'Orders'

# Endpoint para obtener todos los pedidos
@app.route('/orders', methods=['GET'])
def get_orders():
    all_orders = db.list_orders()
    result = [{'id': order.id, 'cantidad': order.cantidad} for order in all_orders]
    return jsonify(result), 200

# Endpoint para crear un nuevo pedido
@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    new_order = Order(
        id=None,
        id_usuario=data['id_usuario'],
        timestamp=data['timestamp'],
        pedido_producto=data['pedido_producto'],
        id_pedido=data['id_pedido'],
        id_producto=data['id_producto'],
        cantidad=data['cantidad']
    )
    db.add_order(new_order)
    return jsonify({'message': 'Pedido creado correctamente'}), 201

# Endpoint para obtener detalles de un pedido específico
@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = db.get_order(order_id)
    if order:
        return jsonify({'id': order.id, 'cantidad': order.cantidad}), 200
    else:
        return jsonify({'message': 'Pedido no encontrado'}), 404

# Endpoint para actualizar detalles de un pedido
@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.json
    updated_order = Order(id=order_id, cantidad=data['cantidad'])  # Puedes modificar aquí según lo necesites
    if db.update_order(updated_order):
        return jsonify({'message': 'Pedido actualizado correctamente'}), 200
    else:
        return jsonify({'message': 'Pedido no encontrado'}), 404

# Endpoint para eliminar un pedido
@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    if db.delete_order(order_id):
        return jsonify({'message': 'Pedido eliminado correctamente'}), 204
    else:
        return jsonify({'message': 'Pedido no encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True)
