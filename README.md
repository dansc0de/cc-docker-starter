# Docker Starter

CS 1660/2060 - Introduction to Cloud Computing

A simple Flask application for learning Docker fundamentals.

## Quick Start

```bash
# build the image
docker build -t flask-app .

# run the container
docker run --rm -p 5000:5000 flask-app

# test it
curl localhost:5000/
curl localhost:5000/health
```

## Files

| File                    | Description |
|-------------------------|-------------|
| `app/app.py`            | Simple Flask API with health endpoint |
| `app/requirements.txt`  | Python dependencies |
| `Dockerfile`            | Basic single-stage Dockerfile |
| `Dockerfile.multistage` | Advanced multi-stage example |
| `.dockerignore`         | Files excluded from build context |
| `docs/demo-commands.md` | All commands from lecture |

## Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | Welcome message with hostname |
| `GET /health` | Health check with timestamp |

## Build Variants

### Basic Build
```bash
docker build -t flask-app:basic .
```

### Multi-Stage Build
```bash
docker build -f Dockerfile.multistage -t flask-app:multi .
```

### Compare Sizes
```bash
docker images | grep flask-app
```

## Development with Live Reload

Mount your code for development:

```bash
docker run --rm -p 5000:5000 \
  -v $(pwd)/app.py:/app/app.py:ro \
  flask-app
```

Note: Flask debug mode should be enabled for auto-reload.
