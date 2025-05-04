# Online Bookstore Microservices

A scalable online bookstore built with microservices, using FastAPI, PostgreSQL, MongoDB, Kafka, Redis, and Kubernetes.

## Services
- **Book Info**: Manages books/authors (MongoDB, Redis).
- **Order**: Handles orders (PostgreSQL, Kafka).
- **Cart**: Manages carts (PostgreSQL, Redis).
- **Wishlist**: Manages wishlists (PostgreSQL, Redis).
- **Payment**: Processes payments (PostgreSQL, Kafka).

## Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd online-bookstore
   ```
2. Local development:
   - Copy `.env.example` to `.env` in each service.
   - Run:
     ```bash
     docker-compose up --build
     ```
   - Access APIs at `http://localhost:8000/docs` (book-info), etc.
3. Kubernetes deployment:
   - Build/push images:
     ```bash
     ./scripts/deploy.sh
     ```
   - Apply manifests:
     ```bash
     kubectl apply -f k8s/
     ```
4. Run tests:
   ```bash
   ./scripts/test.sh
   ```

## Requirements
- Docker
- Kubernetes
- Python 3.11