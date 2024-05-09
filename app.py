import os
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from database import Database

load_dotenv()

app = Flask(__name__)
db = Database()

@app.route('/')
def welcome():
    return 'Orders'

@app.route('/orders', methods=['GET'])
def get_orders():
    all_orders = db.list_orders()
    result = []
    for order in all_orders:
        order_info = {
            'id': order.id,
            'id_usuario': order.id_usuario,
            'timestamp': order.timestamp,
            'productos': []
        }
        for product in order.products:
            product_info = {
                'id_producto': product.product_id,
                'cantidad': product.quantity
            }
            order_info['productos'].append(product_info)
        result.append(order_info)
    return jsonify(result), 200

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    new_order = db.add_order(data['id_usuario'])

    for product_data in data['productos']:
        db.add_order_products(
            order_id=new_order.id,
            product_id=product_data['id_producto'],
            quantity=product_data['cantidad']
        )

    return jsonify({'message': 'Pedido creado correctamente'}), 201

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = db.get_order(order_id)
    if order:
        order_info = {
            'id': order.id,
            'id_usuario': order.id_usuario,
            'timestamp': order.timestamp,
            'productos': []
        }
        for product in order.products:
            product_info = {
                'id_producto': product.product_id,
                'cantidad': product.quantity
            }
            order_info['productos'].append(product_info)
        return jsonify(order_info), 200
    else:
        return jsonify({'message': 'Pedido no encontrado'}), 404

@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    if db.delete_order(order_id):
        return jsonify({'message': 'Pedido eliminado correctamente'}), 204
    else:
        return jsonify({'message': 'Pedido no encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True)
