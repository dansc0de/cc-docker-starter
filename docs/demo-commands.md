# Docker Demo Commands

Commands used during the CS 1660/2060 Docker lecture. Follow along!

## Pulling and Inspecting Images

```bash
# pull an image
docker pull python:3.12-slim

# list local images
docker images

# see image layers
docker history python:3.12-slim

# detailed image info
docker inspect python:3.12-slim
```

## Running Containers

```bash
# run nginx in foreground (Ctrl+C to stop)
docker run nginx

# run detached with port mapping
docker run -d -p 8080:80 --name web nginx

# test it
curl localhost:8080

# list running containers
docker ps

# list all containers (including stopped)
docker ps -a

# view logs
docker logs web
docker logs -f web  # follow mode

# stop and remove
docker stop web
docker rm web

# shortcut: auto-remove on exit
docker run --rm -d -p 8080:80 nginx
```

## Executing Commands in Containers

```bash
# run a command
docker exec web ls /usr/share/nginx/html

# get interactive shell
docker exec -it web bash

# exit with: exit or Ctrl+D
```

## Volumes and Bind Mounts

```bash
# mount current directory (read-only)
docker run --rm -d -p 8080:80 \
  -v $(pwd):/usr/share/nginx/html:ro \
  nginx

# named volume
docker volume create mydata
docker run -v mydata:/app/data myapp
docker volume ls
```

## Building Images

```bash
# build from Dockerfile in current directory
docker build -t myapp:v1 .

# build with specific Dockerfile
docker build -f Dockerfile.multistage -t myapp:v1 .

# build with no cache (full rebuild)
docker build --no-cache -t myapp:v1 .

# see build output
docker build -t myapp:v1 . 2>&1 | tee build.log
```

## Building This App

```bash
# build the image
docker build -t flask-app:v1 .

# run it
docker run --rm -d -p 5000:5000 --name app flask-app:v1

# test endpoints
curl localhost:5000/
curl localhost:5000/health

# view logs
docker logs app

# get shell access
docker exec -it app sh

# stop
docker stop app
```

## Multi-Stage Build

```bash
# build with multi-stage Dockerfile
docker build -f Dockerfile.multistage -t flask-app:multistage .

# compare sizes
docker images | grep flask-app
```

## Cleanup Commands

```bash
# remove stopped containers
docker container prune

# remove unused images
docker image prune

# remove everything unused
docker system prune

# nuclear option (removes ALL)
docker system prune -a
```

## Useful Inspection Commands

```bash
# container details
docker inspect container_name

# get container IP
docker inspect -f '{{.NetworkSettings.IPAddress}}' container_name

# see port mappings
docker port container_name

# resource usage
docker stats
```

## Tagging and Pushing

```bash
# tag for Docker Hub
docker tag flask-app:v1 USERNAME/flask-app:v1

# login to Docker Hub
docker login

# push
docker push USERNAME/flask-app:v1

# tag for ECR
docker tag flask-app:v1 ACCOUNT.dkr.ecr.REGION.amazonaws.com/flask-app:v1
```
