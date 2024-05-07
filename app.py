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
    result = [{'id': order['id'], 'cantidad': order['cantidad']} for order in all_orders]
    return jsonify(result), 200

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    new_order_data = {
        'id_usuario': data['id_usuario'],
        'timestamp': data['timestamp'],
        'pedido_producto': data['pedido_producto'],
        'id_pedido': data['id_pedido'],
        'id_producto': data['id_producto'],
        'cantidad': data['cantidad']
    }
    db.add_order(new_order_data)
    return jsonify({'message': 'Pedido creado correctamente'}), 201

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = db.get_order(order_id)
    if order:
        return jsonify({'id': order['id'], 'cantidad': order['cantidad']}), 200
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
