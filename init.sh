#!/bin/bash

# Exit on any error
set -e

# Check if DynamoDB is Running
IMAGE="$(docker ps --format json | jq -r '.[0].Image')"

if [[ "$IMAGE" != *"amazon/dynamodb-local:latest"* ]]; then
  echo "Initializing DynamoDB locally using Docker Compose..."
  docker-compose up -d
  echo "DynamoDB initialized."
else
  echo "DynamoDB is already running."
fi

# Define the schema folder
SCHEMA_FOLDER="schemas"

# Check if the schema folder exists
if [[ ! -d "$SCHEMA_FOLDER" ]]; then
  echo "Error: Schema folder '$SCHEMA_FOLDER' not found!"
  exit 1
fi

# Process all JSON files in the schema folder
for FILE in "$SCHEMA_FOLDER"/*.json; do
  if [[ -f "$FILE" ]]; then
    echo "Processing file: $FILE"

    # Extract table name from the JSON file
    TABLE_NAME=$(jq -r '.TableName' "$FILE")
    if [[ -z "$TABLE_NAME" || "$TABLE_NAME" == "null" ]]; then
      echo "Error: TableName not found in $FILE. Skipping."
      continue
    fi

    # Check if the table exists
    echo "Checking if table '$TABLE_NAME' exists..."

    # Get the list of existing tables
    EXISTING_TABLES=$(aws dynamodb list-tables --endpoint-url http://localhost:8000 --query "TableNames[]" --output text)

    # Check if the table is in the list of existing tables
    if echo "$EXISTING_TABLES" | grep -qw "$TABLE_NAME"; then
      echo "Table '$TABLE_NAME' already exists. Skipping creation."
    else
      echo "Creating DynamoDB table: $TABLE_NAME"

      # Create the DynamoDB table using AWS CLI
      aws dynamodb create-table --endpoint-url http://localhost:8000 --cli-input-json file://"$FILE"

      echo "Table '$TABLE_NAME' creation initiated."
    fi
  else
    echo "No JSON files found in '$SCHEMA_FOLDER'. Skipping."
  fi
done

echo "All tables processed. Check AWS Management Console or use 'aws dynamodb list-tables' to verify."
