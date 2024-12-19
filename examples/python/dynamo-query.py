import boto3

# Create a DynamoDB resource
dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

# Reference the table
table = dynamodb.Table('MyTable')

# Perform the query
response = table.query(
    KeyConditionExpression="ID = :ID AND begins_with(SORT_ID, :SORT_ID)",
    ExpressionAttributeValues={
        ':ID': 'DS#dc938a23-c7cc-4e8f-8c82-3bac27f67fe4',
        ':SORT_ID': 'TP'
    }
)

# Print the items
items = response.get('Items', [])
print(items)
