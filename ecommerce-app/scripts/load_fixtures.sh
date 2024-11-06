
#!/bin/bash

echo "Loading Product Service fixtures..."
docker-compose exec product-service python fixtures.py

echo "Loading Order Service fixtures..."
docker-compose exec order-service python fixtures.py

echo "Loading Inventory Service fixtures..."
docker-compose exec inventory-service python fixtures.py

echo "All fixtures loaded successfully!"
