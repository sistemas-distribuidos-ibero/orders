import os
from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv
from database import Database

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configuración de la aplicación Flask
app = Flask(__name__)
db = Database()

# Inicializar la extensión Marshmallow
ma = Marshmallow(app)

# Definición del modelo de Pedido
class Order:
    def __init__(self, id, cantidad):
        self.id = id
        self.cantidad = cantidad

class OrderSchema(ma.Schema):
    class Meta:
        fields = ('id', 'cantidad')

# Inicializar los esquemas
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

@app.route('/')
def welcome():
    return 'Orders'

# Endpoint para obtener todos los pedidos
@app.route('/orders', methods=['GET'])
def get_orders():
    all_orders = db.list_orders()
    result = orders_schema.dump(all_orders)
    return jsonify(result), 200

# Endpoint para crear un nuevo pedido
@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    new_order = Order(id=None, cantidad=data['cantidad'])  # Puedes modificar aquí según lo necesites
    db.add_order(new_order)
    return order_schema.jsonify(new_order), 201

# Endpoint para obtener detalles de un pedido específico
@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = db.get_order(order_id)
    return order_schema.jsonify(order), 200

# Endpoint para actualizar detalles de un pedido
@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.json
    updated_order = Order(id=order_id, cantidad=data['cantidad'])  # Puedes modificar aquí según lo necesites
    db.update_order(updated_order)
    return order_schema.jsonify(updated_order), 200

# Endpoint para eliminar un pedido
@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    db.delete_order(order_id)
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)

