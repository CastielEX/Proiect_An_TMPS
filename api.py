from flask import Flask, jsonify, request

app = Flask(__name__)


categories = [
    {
        "id": 1,
        "title": "Books",
        "description": "Stephen King Collection"
    },
    {
        "id": 2,
        "title": "PC",
        "description": "NVIDIA AND AMD"
    },
    {
        "id": 3,
        "title": "Cloths",
        "description": "PUMA"
    }
]

products = [
    {
        "id": 1,
        "category_id": 1,
        "name": "The Catcher in the Rye",
        "price": 10.99,
        "description": "A novel by J.D. Salinger"
    },
    {
        "id": 2,
        "category_id": 1,
        "name": "1984",
        "price": 8.99,
        "description": "A dystopian novel by George Orwell"
    },
    {
        "id": 3,
        "category_id": 2,
        "name": "iPhone X",
        "price": 799.99,
        "description": "A high-end smartphone by Apple"
    },
    {
        "id": 4,
        "category_id": 3,
        "name": "Jeans",
        "price": 49.99,
        "description": "A pair of denim jeans"
    },
    {
        "id": 5,
        "category_id": 3,
        "name": "T-Shirt",
        "price": 19.99,
        "description": "A cotton t-shirt"
    }
]


@app.route('/categories', methods=['GET'])
def get_categories():
    return jsonify(categories)

@app.route('/categories/<int:category_id>', methods=['PATCH'])
def update_category(category_id):
    category = next((c for c in categories if c["id"] == category_id), None)
    if category is not None:
        data = request.get_json()
        category["title"] = data["title"]
        return jsonify(category)
    else:
        return jsonify({'message': 'Category not found'}), 404


@app.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = next((c for c in categories if c["id"] == category_id), None)
    if category is not None:
        return jsonify(category)
    else:
        return jsonify({'message': 'Category not found'}), 404


@app.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    category = {
        "id": len(categories) + 1,
        "title": data["title"],
        "description": data["description"]
    }
    categories.append(category)
    return jsonify(category), 201


@app.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    category = next((c for c in categories if c["id"] == category_id), None)
    if category is not None:
        categories.remove(category)
        return '', 204
    else:
        return jsonify({'message': 'Category not found'}), 404


@app.route('/categories/<int:category_id>/products', methods=['POST'])
def create_product(category_id):
    category = next((c for c in categories if c["id"] == category_id), None)
    if category is not None:
        data = request.get_json()
        product = {
            "id": len(products) + 1,
            "category_id": category_id,
            "name": data["name"],
            "price": data["price"],
            "description": data["description"]
        }
        products.append(product)
        return jsonify(product), 201
    else:
        return jsonify({'message': 'Category not found'}), 404


@app.route('/categories/<int:category_id>/products', methods=['GET'])
def get_products(category_id):
    category = next((c for c in categories if c["id"] == category_id), None)
    if category is not None:
        products_in_category = [p for p in products if p["category_id"] == category_id]
        return jsonify(products_in_category)
    else:
        return jsonify({'message': 'Category not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)