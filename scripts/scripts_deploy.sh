#!/bin/bash
echo "Building and pushing Docker images..."
for service in book-info-service order-service cart-service wishlist-service payment-service; do
  docker build -t bookstore-$service:latest ./$service
  docker push bookstore-$service:latest
done
echo "Deploying to Kubernetes..."
kubectl apply -f k8s/
echo "Deployment complete."