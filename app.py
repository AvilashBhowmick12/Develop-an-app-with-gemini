"""
A sample Hello World server.
"""
import os

from flask import Flask, render_template, jsonify
from inventory import inventory

# pylint: disable=C0103
app = Flask(__name__)


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    message = "It's running!"

    """Get Cloud Run environment variables."""
    service = os.environ.get('K_SERVICE', 'Unknown service')
    revision = os.environ.get('K_REVISION', 'Unknown revision')

    return render_template('index.html',
        message=message,
        Service=service,
        Revision=revision)

@app.route('/inventory', methods=['GET'])
def inventory_list():
    """Return a list of inventory items in JSON format."""
    return jsonify(inventory)

# Generate an App route to get a product from the list of inventory items given the productID.
# Use the GET method.
# If there is an invalid productID, return a 404 error with an error message in the JSON.
# Return the product in JSON format.
# Example:
# GET /inventory/1
# Response:
# {
#   "productid": "1",
#   "onhandqty": "10"
# }
# GET /inventory/4
# Response:
# {
#   "error": "Invalid productID"
# }
@app.route('/inventory/<productid>', methods=['GET'])
def get_product(productid):
    """Return a product from the list of inventory items given the productID."""
    for product in inventory:
        if product['productid'] == productid:
            return jsonify(product)
    return jsonify({'error': 'Invalid productID'}), 404
# End of code.

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')
