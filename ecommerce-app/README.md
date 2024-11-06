E-Commerce Microservices Application
This project demonstrates a simplified e-commerce order processing system using microservices and an event-driven architecture. The system is built using Python Flask for the services, PostgreSQL for databases, Redis for the message broker, and Docker/Kubernetes for containerization.

Architecture Overview:
This application follows a microservice-based architecture with each service owning its database. The services communicate asynchronously using events published via Redis, acting as the message broker.

Product Service: Manages the product catalog (CRUD operations).
Order Service: Processes orders and checks product availability via the Inventory Service.
Inventory Service: Manages inventory levels and handles stock updates when orders are placed.

Services:
1. Product Service
Purpose: Handles product catalog management (CRUD).
Database: PostgreSQL (product_db).
API Endpoints:
    GET /products - List all products.
    POST /products - Add a new product.
    GET /products/{id} - Get product details.
    PUT /products/{id} - Update product details.
    DELETE /products/{id} - Delete a product.

2. Order Service
Purpose: Handles order placement and status updates. Communicates with the Inventory Service.
Database: PostgreSQL (order_db).
API Endpoints:
    POST /orders - Place an order.
    GET /orders/{id} - Get order status.

3. Inventory Service
Purpose: Manages stock levels and responds to the Order Service for availability checks.
Database: PostgreSQL (inventory_db).
API Endpoints:
    POST /inventory - Update stock levels.
    GET /inventory/{productId} - Get stock details for a product.

Prerequisites:
- Ensure you have the following tools installed on your machine:
- Docker (version 20.10 or later)
- Docker Compose (version 1.29 or later)
- Python 3.8+ (for running locally without Docker)
- Redis (used for message brokering)
- PostgreSQL (version 11 or later for the databases)

Installation:
- Clone the Repository

Build the Docker Images: 
- Navigate to the project root and build the Docker images using Docker Compose.
   "docker-compose up --build"

Running the Application:
- Once the application has been built, you can run it using Docker Compose.
    "docker-compose up"
- This will start all three services:
    Product Service (accessible at localhost:5005)
    Order Service (accessible at localhost:5007)
    Inventory Service (accessible at localhost:5006)

Loading Fixtures:
- To load initial data into the services (for testing purposes), you can run the fixture script:
    "sh scripts/load_fixtures.sh"
- This script will add sample products to the Product Service, some initial orders to the Order Service, and stock levels to the Inventory Service.

Running Tests:
- Each service comes with its own set of unit tests. You can run the tests for each service inside the Docker container:

Order Service: (tests are still wip)
- Follow below commands
    "docker exec -it order-service bash"
    "python -m unittest discover tests"
Inventory Service:
- Follow below commands
    "docker exec -it inventory-service bash"
    "python -m unittest discover tests"
Product Service:
- Follow below commands
    "docker exec -it product-service bash"
    "python -m unittest discover tests"

Docker and Kubernetes:
Docker:
- All services are containerized and built with Docker. The Dockerfile for each service defines the environment, dependencies, and startup command.
- The docker-compose.yml file defines how these services are orchestrated, along with the PostgreSQL databases and Redis.

Kubernetes:
- This project can be deployed on Kubernetes. You can use kubectl commands to create deployments, services, and pods for each service.
    For a basic Kubernetes setup:
    - Create a Kubernetes cluster using minikube or any cloud provider.
    - Define Deployment and Service YAML files for each microservice.
    - Deploy Redis as a separate service.
    - Use kubectl to apply your deployment configurations.

Explanation:
    Product Service:
    - Manages products and product catalog (CRUD operations).
    - Sends product details to Order Service when required.

    Order Service:
    - Receives orders from the client.
    - Publishes OrderCreated event to Redis when an order is placed.
  
    Inventory Service:
    - Subscribes to OrderCreated events from Redis.
    - Checks stock availability and updates the inventory.
 
    Redis:
    - Acts as the message broker for the event-driven communication between services.

Conclusion:
- This project demonstrates how to implement a simplified e-commerce system using microservices and an event-driven architecture. Each service is isolated with its own database and communicates asynchronously via Redis. You can scale and test individual services without impacting the whole system.

Testing final apis:

Step 1: Add Products
First, let's add a product to the product service.

Add a New Product
    "curl -X POST http://localhost:5005/products -H "Content-Type: application/json" -d '{"name": "Test Product", "price": 50.00, "in_stock": 100}'"

Step 2: Add Inventory
- Add Inventory for the Product. This also triggers a redis ebvent to update in_stock option for the given product_id.
  "curl -X POST http://localhost:5006/inventory -H "Content-Type: application/json" -d '{"product_id": 1, "quantity": 100}'"

Step 3: Check Initial Inventory and Product Status
    Check Product:
    "curl -X GET http://localhost:5005/products/1"

    Check Inventory:
    "curl -X GET http://localhost:5006/inventory/1"

Step 4: Place an Order
Create an Order:
    "curl -X POST http://localhost:5007/orders -H "Content-Type: application/json" -d '{"product_id": 1, "quantity": 2, "total_price": 100.00}'"

Step 5: Check Inventory After Order
- After placing the order, check the inventory to see if it has been updated correctly.
- Check Updated Inventory
    "curl -X GET http://localhost:5006/inventory/1"

Step 6: Check Product After Order
- Finally, check the product details to confirm any necessary updates.
    "curl -X GET http://localhost:5005/products/1"

Summary of Expected Outcomes:
- After adding the product, you should see the product listed when you check all products.
- After adding inventory, the inventory should reflect the added quantity, this also updates product service as well.
- Upon placing an order, the inventory quantity should decrease by the quantity of the order (in this case, from 100 to 98).
- The product service should reflect any changes if necessary, but since you're not updating the product directly in this example, it may remain unchanged unless explicitly updated.