from flask import Flask, request, jsonify

app = Flask(__name__)

# Dummy data
products = [{"id": 1, "name": "product1", "status": "active"}]
users = [{"id": 1, "name": "admin", "role": "admin"}]


@app.route('/products', methods=['GET', 'POST'])
def manage_products():
    if request.method == 'GET':
        return jsonify(products)
    else:  # POST
        new_product = request.json
        products.append(new_product)
        return jsonify(new_product), 201


@app.route('/products/<int:product_id>', methods=['PUT', 'DELETE'])
def modify_product(product_id):
    global products
    if request.method == 'DELETE':
        products = [p for p in products if p['id'] != product_id]
        return '', 204
    elif request.method == 'PUT':
        for product in products:
            if product['id'] == product_id:
                product.update(request.json)
                return jsonify(product)
    return jsonify({"error": "Not found"}), 404


@app.route('/users', methods=['GET', 'POST'])
def manage_users():
    if request.method == 'GET':
        return jsonify(users)
    else:  # POST
        new_user = request.json
        users.append(new_user)
        return jsonify(new_user), 201


# Execute the application
if __name__ == '__main__':
    app.run(port=5000)
