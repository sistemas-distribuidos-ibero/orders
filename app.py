import os
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from database import Database, Order

load_dotenv()

app = Flask(__name__)
db = Database()

@app.route('/')
def welcome():
    return 'Welcome to the Order Management System!'


@app.route('/orders', methods=['GET'])
def get_orders():
    try:

        all_orders = db.list_orders()
        result = []

        for order in all_orders:
            order_info = {
                'id': order.id,
                'user_id': order.id_user,
                'price': order.price,
                'created_at': order.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                'products': []
            }
            for product in order.products:
                product_info = {
                    'product_id': product.id_product,  
                    'quantity': product.quantity
                }
                order_info['products'].append(product_info)
            result.append(order_info)

        return jsonify(result), 200

    except Exception as e:
        # Manejo genérico de excepciones
        return jsonify({
            'message': 'Error del servidor',
            'error': str(e)
        }), 500


@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    try:
        new_order = Order(id_user=data['user_id'], price=data['price'])
        db.add_order(new_order)
        id_order = new_order.id

        for product_data in data['products']:
            db.add_order_products(
                order_id=id_order,
                product_id=product_data['product_id'],
                quantity=product_data['quantity']
            )

        return jsonify({'order_id': id_order}), 201

    except KeyError as ke:
        return jsonify({'message': f'Error de datos: Falta {str(ke)}'}), 400
    except Exception as e:
        return jsonify({'message': f'Error del servidor: {str(e)}'}), 500

if __name__ == '__main__':
    debug = os.getenv('DEBUG') == '1'
    app.run(debug=debug, port=os.getenv('PORT'), host=os.getenv('HOST'))
