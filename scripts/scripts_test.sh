#!/bin/bash
echo "Running tests..."
for service in book-info-service order-service cart-service wishlist-service payment-service; do
  cd $service
  pytest
  cd ..
done
echo "Tests complete."