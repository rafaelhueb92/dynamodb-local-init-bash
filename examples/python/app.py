from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import ClientError

# Initialize Flask app
app = Flask(__name__)

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
table = dynamodb.Table('MyTable')

class DynamoDBCRUD:
    def __init__(self):
        self.table = table

    def create_item(self, ID, SORT_ID, data):
        try:
            response = self.table.put_item(
                Item={
                    'ID': ID,
                    'SORT_ID': SORT_ID,
                    'data': data
                }
            )
            return response
        except ClientError as e:
            return {"error": str(e)}

    def get_item(self, ID, SORT_ID):
        try:
            response = self.table.get_item(
                Key={
                    'ID': ID,
                    'SORT_ID': SORT_ID
                }
            )
            return response.get('Item', None)
        except ClientError as e:
            return {"error": str(e)}

    def update_item(self, ID, SORT_ID, data):
        try:
            response = self.table.update_item(
                Key={
                    'ID': ID,
                    'SORT_ID': SORT_ID
                },
                UpdateExpression="set data = :data",
                ExpressionAttributeValues={
                    ':data': data
                },
                ReturnValues="UPDATED_NEW"
            )
            return response
        except ClientError as e:
            return {"error": str(e)}

    def delete_item(self, ID, SORT_ID):
        try:
            response = self.table.delete_item(
                Key={
                    'ID': ID,
                    'SORT_ID': SORT_ID
                }
            )
            return response
        except ClientError as e:
            return {"error": str(e)}

# Create an instance of DynamoDBCRUD class
dynamodb_crud = DynamoDBCRUD()

# Route to create an item
@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    ID = data.get('ID')
    SORT_ID = data.get('SORT_ID')
    data_value = data.get('data')

    if not ID or not SORT_ID or not data_value:
        return jsonify({"error": "ID, SORT_ID, and data are required"}), 400

    response = dynamodb_crud.create_item(ID, SORT_ID, data_value)
    return jsonify(response), 201

# Route to read an item
@app.route('/items/<ID>/<SORT_ID>', methods=['GET'])
def get_item(ID, SORT_ID):
    response = dynamodb_crud.get_item(ID, SORT_ID)
    if not response:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(response), 200

# Route to update an item
@app.route('/items/<ID>/<SORT_ID>', methods=['PUT'])
def update_item(ID, SORT_ID):
    data = request.get_json()
    data_value = data.get('data')

    if not data_value:
        return jsonify({"error": "Data is required"}), 400

    response = dynamodb_crud.update_item(ID, SORT_ID, data_value)
    return jsonify(response), 200

# Route to delete an item
@app.route('/items/<ID>/<SORT_ID>', methods=['DELETE'])
def delete_item(ID, SORT_ID):
    response = dynamodb_crud.delete_item(ID, SORT_ID)
    return jsonify(response), 200

if __name__ == '__main__':
    port = 3000
    app.run(debug=True, port=port)
    print(f"Running on http://localhost:{port}")
