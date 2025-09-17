## URL Shortener

Simple URL shortener built with FastAPI and Redis. It exposes a minimal API to create short URLs and redirect users to the original long URL. The app is containerized and includes Docker Compose and Kubernetes manifests.

### Features
- **FastAPI** backend with two endpoints
- **Redis** for key-value storage of short codes → long URLs
- **Docker Compose** for local development
- **Kubernetes** manifests for deployment

### Tech Stack
- **Backend**: FastAPI, Uvicorn
- **Database/Cache**: Redis
- **Containerization**: Docker
- **Orchestration**: Docker Compose, Kubernetes

## Getting Started

### Prerequisites
- Docker and Docker Compose
- (Optional) Python 3.10+ if you prefer running locally without containers
- (Optional) kubectl and a Kubernetes cluster (e.g., kind, Minikube, Docker Desktop)

### Run with Docker Compose (recommended)
```bash
docker-compose up --build
```
App will be available at `http://localhost:8000` and Redis runs in a separate container. Data persists in a Docker volume named `redis_data`.

### Local Development (without Docker)
```bash
cd app
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export REDIS_HOST=localhost # Windows PowerShell: $env:REDIS_HOST = "localhost"
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
You must have a Redis instance running locally on port 6379.

## API

### Create Short URL
- **Endpoint**: `POST /shorten`
- **Body**: JSON `{ "url": "https://example.com" }`
- **Response**: `{ "short_url": "http://localhost:8000/Ab12Cd" }`

Example:
```bash
curl -X POST http://localhost:8000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'
```

### Redirect
- **Endpoint**: `GET /{short_code}`
- **Behavior**: 302 Redirects to the original URL
- **Errors**: 404 if code is not found

## Configuration

### Environment Variables
- **REDIS_HOST**: Hostname of the Redis server (default: `redis`). Docker Compose sets this automatically for the app container. For local development without Docker, set it to `localhost`.

## Docker

The application container is built from `app/Dockerfile` and uses `uvicorn` to serve FastAPI on port 8000.

Key commands:
```bash
# Build and run with compose
docker-compose up --build

# Stop containers
docker-compose down
```

## Kubernetes

Manifests are provided in the `k8s/` directory:
- `app-configmap.yaml`
- `app-deployment.yaml`
- `app-service.yaml`
- `redis-deployment.yaml`
- `redis-service.yaml`

Apply them in order (Redis first, then the app):
```bash
kubectl apply -f k8s/redis-deployment.yaml
kubectl apply -f k8s/redis-service.yaml
kubectl apply -f k8s/app-configmap.yaml
kubectl apply -f k8s/app-deployment.yaml
kubectl apply -f k8s/app-service.yaml
```

Port-forward the app service to access it locally:
```bash
kubectl port-forward svc/url-shortener-service 8000:8000
```
Then call the API at `http://localhost:8000`.

## Notes
- Short codes are randomly generated 6-character alphanumeric strings.
- The service prints the pod/container hostname when shortening URLs, useful for observing load distribution in Kubernetes.

## Project Structure
```
app/                  # FastAPI application
  Dockerfile
  main.py             # API endpoints and Redis integration
  requirements.txt
docker-compose.yml    # Local multi-container setup (app + redis)
k8s/                  # Kubernetes manifests for app and redis
README.md             # This file
```

