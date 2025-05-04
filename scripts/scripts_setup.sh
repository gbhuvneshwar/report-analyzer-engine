#!/bin/bash
echo "Setting up project..."
# Install dependencies
for service in book-info-service order-service cart-service wishlist-service payment-service; do
  cd $service
  pip install -r requirements.txt
  cd ..
done
echo "Setup complete."