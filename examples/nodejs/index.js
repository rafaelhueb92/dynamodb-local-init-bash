const express = require('express');
const bodyParser = require('body-parser');
const AWS = require('aws-sdk');

// Initialize DynamoDB client
AWS.config.update({
  region: 'us-west-2',
  endpoint: 'http://localhost:8000',
});

const docClient = new AWS.DynamoDB.DocumentClient();

// Initialize Express app
const app = express();
const port = 3000;

// Middleware
app.use(bodyParser.json());

// Define table name
const tableName = 'MyTable';

// Create a new item
app.post('/items', async (req, res) => {
  const { ID, SORT_ID, data } = req.body;

  if (!ID || !SORT_ID || !data) {
    return res.status(400).json({ message: 'ID, SORT_ID, and data are required' });
  }

  const params = {
    TableName: tableName,
    Item: {
      ID,
      SORT_ID,
      data,
    },
  };

  try {
    await docClient.put(params).promise();
    res.status(201).json({ message: 'Item created successfully' });
  } catch (error) {
    res.status(500).json({ error: 'Failed to create item', details: error.message });
  }
});

// Read an item by ID and SORT_ID
app.get('/items/:ID/:SORT_ID', async (req, res) => {
  const { ID, SORT_ID } = req.params;

  const params = {
    TableName: tableName,
    Key: {
      ID,
      SORT_ID,
    },
  };

  try {
    const data = await docClient.get(params).promise();
    if (!data.Item) {
      return res.status(404).json({ message: 'Item not found' });
    }
    res.json(data.Item);
  } catch (error) {
    res.status(500).json({ error: 'Failed to get item', details: error.message });
  }
});

// Update an item by ID and SORT_ID
app.put('/items/:ID/:SORT_ID', async (req, res) => {
  const { ID, SORT_ID } = req.params;
  const { data } = req.body;

  if (!data) {
    return res.status(400).json({ message: 'Data is required' });
  }

  const params = {
    TableName: tableName,
    Key: {
      ID,
      SORT_ID,
    },
    UpdateExpression: 'set data = :data',
    ExpressionAttributeValues: {
      ':data': data,
    },
    ReturnValues: 'UPDATED_NEW',
  };

  try {
    const result = await docClient.update(params).promise();
    res.json({ message: 'Item updated successfully', updatedAttributes: result.Attributes });
  } catch (error) {
    res.status(500).json({ error: 'Failed to update item', details: error.message });
  }
});

// Delete an item by ID and SORT_ID
app.delete('/items/:ID/:SORT_ID', async (req, res) => {
  const { ID, SORT_ID } = req.params;

  const params = {
    TableName: tableName,
    Key: {
      ID,
      SORT_ID,
    },
  };

  try {
    await docClient.delete(params).promise();
    res.json({ message: 'Item deleted successfully' });
  } catch (error) {
    res.status(500).json({ error: 'Failed to delete item', details: error.message });
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
