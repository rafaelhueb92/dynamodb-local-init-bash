 <h1>Project Setup - DynamoDB Local with Schema Files</h1>
    
 <h2>Project Overview</h2>
    <p>
        This project sets up DynamoDB locally using Docker Compose, processes schema files in the <code>schemas</code> folder, and uses a Bash script to create DynamoDB tables based on those schema files. 
        The script ensures that the tables are only created if they do not already exist in the local DynamoDB instance.
    </p>
    
<h2>Project Structure</h2>
    <pre>
    .
    ├── docker-compose.yml       # Docker Compose file to run DynamoDB locally
    ├── schemas/                 # Folder containing JSON schema files
    │   ├── table1-schema.json   # Example schema file for table1
    ├── init.sh                  # Bash script to init Docker Compose and create tables in DynamoDB if necessary
    └── README.html              # This file
    </pre>

<h2>Prerequisites</h2>
    <ul>
        <li><strong>Docker:</strong> Ensure Docker is installed and running on your machine.</li>
        <li><strong>AWS CLI:</strong> Ensure AWS CLI is configured to interact with DynamoDB locally.</li>
    </ul>

<h2>Setup Instructions</h2>

<h3>1. Clone the Repository</h3>
    <pre>
    git clone <your-repository-url>
    cd <your-repository-name>
    </pre>

<h3>2. Docker Compose Setup</h3>
    <p>
        The project uses Docker Compose to spin up DynamoDB locally. The <code>docker-compose.yml</code> file is configured to pull the official Amazon DynamoDB Local image.
    </p>
    <pre>
    services:
     dynamodb-local:
      command: "-jar DynamoDBLocal.jar -sharedDb -dbPath ./data"
      image: "amazon/dynamodb-local:latest"
      container_name: dynamodb-local
      ports:
       - "8000:8000"
      volumes:
       - "./docker/dynamodb:/home/dynamodblocal/data"
      working_dir: /home/dynamodblocal
    </pre>

<h3>3. Organize Schema Files</h3>
    <p>
        Place your DynamoDB table schema files in the <code>schemas</code> folder. Each schema file should be a JSON file with the table definition. The <code>TableName</code> attribute in each JSON file will be used to check if the table already exists.
    </p>
    <p>Example schema file (table1-schema.json):</p>
    <pre>
    {
        "TableName": "MyTable",
        "KeySchema": [
            { "AttributeName": "ID", "KeyType": "HASH" }
        ],
        "AttributeDefinitions": [
            { "AttributeName": "ID", "AttributeType": "S" }
        ],
        "ProvisionedThroughput": {
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5
        }
    }
    </pre>

<h3>4. Run Docker Compose</h3>
    <p>
        Use the following command to bring up the DynamoDB local container:
    </p>
    <pre>
    docker-compose up -d
    </pre>
    <p>
        This will start the DynamoDB local instance, which will be accessible at <code>http://localhost:8000</code>.
    </p>

<h3>5. Run the Bash Script</h3>
    <p>
        The <code>init.sh</code> script will read all JSON schema files in the <code>schemas</code> folder and create DynamoDB tables locally if they do not already exist.
    </p>
    <pre>
    bash init.sh
    </pre>
    <p>
        The script will:
        <ul>
            <li>Check if DynamoDB is running.</li>
            <li>Process each schema file in the <code>schemas</code> folder.</li>
            <li>Check if the table already exists in the local DynamoDB instance.</li>
            <li>Create the table if it does not already exist.</li>
        </ul>
    </p>

<h3>6. Verify the Tables</h3>
    <p>
        After running the script, you can verify the tables by running the following command:
    </p>
    <pre>
    aws dynamodb list-tables --endpoint-url http://localhost:8000
    </pre>

<h2>Notes</h2>
    <ul>
        <li>This setup is for local development and testing only.</li>
        <li>The tables created will be available only on the local DynamoDB instance.</li>
        <li>Ensure your AWS CLI is configured to point to the local DynamoDB instance using the <code>--endpoint-url http://localhost:8000</code> option.</li>
    </ul>

<h2>Contributing</h2>
    <p>
        Feel free to fork this repository, make improvements, and create pull requests. Any contributions are welcome!
    </p>

<h2>License</h2>
    <p>
        This project is open-source and available under the MIT License.
    </p>