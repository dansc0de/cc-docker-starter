# Docker Deep Dive

---

## Part 1: Connection to Fundamentals

### Whiteboard: Docker Architecture Stack

```mermaid
flowchart TB
    subgraph TODAY["Today: Docker CLI"]
        A["docker run nginx"]
    end
    
    subgraph DAEMON["Docker Daemon"]
        B["dockerd"]
    end
    
    subgraph CONTAINERD["containerd"]
        C["High-level runtime"]
    end
    
    subgraph RUNC["runc"]
        D["Low-level runtime"]
    end
    
    subgraph KERNEL["Kernel Features"]
        E["Namespaces + Cgroups + rootfs"]
    end
    
    TODAY --> DAEMON --> CONTAINERD --> RUNC --> KERNEL
    
    RUNC -.- NOTE1["Last lecture: you did this manually!"]
    KERNEL -.- NOTE2["Last lecture: kernel features"]
```

**Key point:** "Last week you created containers the hard way with unshare, cgroups, and runc. Docker automates all of that."

**Discussion (5 min):**
- Ask: "What did runc need to create a container?" (config.json + rootfs)
- Docker builds that config.json and rootfs for you from a Dockerfile

---

## Part 2: Docker Images and Layers

### Terminal Demo

```bash
# pull an image and watch the layers download
docker pull python:3.12-slim

# show local images
docker images

# inspect the layers
docker history python:3.12-slim

# show that images are just tarballs of layers
docker save python:3.12-slim -o python-image.tar
tar -tvf python-image.tar | head -20
```

### Whiteboard: The Layer Cake

```mermaid
flowchart TB
    subgraph IMAGE["Image Layers (Read-Only)"]
        direction TB
        L4["Layer 4: COPY app.py<br/>Your code"] --> L3
        L3["Layer 3: RUN pip install<br/>Dependencies"] --> L2
        L2["Layer 2: RUN apt-get<br/>System packages"] --> L1
        L1["Layer 1: python:3.12-slim<br/>Base image"]
    end
```

### Whiteboard: Container vs Image Layers

```mermaid
flowchart TB
    subgraph RUNNING["When Container Runs"]
        direction TB
        CL["Container Layer (R/W)<br/>Writable, ephemeral"]
        IL["Image Layers (Read-Only)<br/>Shared across containers"]
        CL --> IL
    end
```

**Key points to write:**
- Each Dockerfile instruction = new layer
- Layers are cached (fast rebuilds)
- Multiple containers share image layers
- Container layer is ephemeral (lost on rm)

**Discussion:**
- "Why would we want layers instead of one big file?"
- Caching, deduplication, efficient updates

---

## Part 3: Essential Docker Commands

### Terminal Demo - Running Containers

```bash
# run nginx in foreground
docker run nginx
# Ctrl+C to stop

# run detached with port mapping
docker run -d -p 8080:80 --name web nginx
curl localhost:8080

# list running containers
docker ps

# view logs
docker logs web
docker logs -f web  # follow

# execute command in running container
docker exec web ls /usr/share/nginx/html
docker exec -it web bash

# stop and remove
docker stop web
docker rm web

# shortcut: --rm removes container on exit
docker run --rm -d -p 8080:80 nginx
```

### Whiteboard: Port Mapping

```mermaid
flowchart LR
    subgraph LAPTOP["Your Laptop"]
        B["Browser<br/>:8080"]
    end
    
    subgraph CONTAINER["Container"]
        N["nginx<br/>:80"]
    end
    
    B -->|"-p 8080:80"| N
```

**Key point:** `docker run -p HOST:CONTAINER`

### Terminal Demo - Volumes

```bash
# create a simple HTML file
echo "<h1>Hello from mounted volume!</h1>" > index.html

# bind mount current directory
docker run --rm -d -p 8080:80 \
  -v $(pwd):/usr/share/nginx/html:ro \
  --name web nginx

curl localhost:8080

# edit file and refresh - changes appear immediately
echo "<h1>Updated!</h1>" > index.html
curl localhost:8080

docker stop web
```

---

## BREAK (10 min)

---

## Part 4: Writing Dockerfiles

**This is the whiteboard-heavy section.**

### Whiteboard: Build a Dockerfile Step by Step

Start with blank whiteboard. Ask students what we need for a Python Flask app.

Write as they suggest (guide them):

```dockerfile
# 1. what do we start from?
FROM python:3.12-slim

# 2. where does our code go?
WORKDIR /app

# 3. what files do we need?
COPY requirements.txt .

# 4. install dependencies
RUN pip install -r requirements.txt

# 5. copy our application
COPY app.py .

# 6. what port does Flask use?
EXPOSE 5000

# 7. how do we start it?
CMD ["python", "app.py"]
```

### Whiteboard: Cache Busting Problem

```mermaid
flowchart LR
    subgraph BAD["BAD ORDER"]
        direction TB
        B1["COPY . ."] --> B2["RUN pip install"]
        B2 --> B3["Change app.py..."]
        B3 --> B4["REINSTALLS ALL DEPS!"]
    end
    
    subgraph GOOD["GOOD ORDER"]
        direction TB
        G1["COPY requirements.txt"] --> G2["RUN pip install"]
        G2 --> G3["COPY app.py"]
        G3 --> G4["Change app.py..."]
        G4 --> G5["Cache preserved!"]
    end
```

**Red marker:** Circle COPY/RUN order - "What happens when we change app.py? Reinstalls ALL dependencies!"

**Blue marker:** Fix - Copy requirements first, install, THEN copy code

### Terminal Demo - Build and Test (10 min)

```bash
cd ~/docker-starter

# show the files
cat app.py
cat requirements.txt
cat Dockerfile

# build
docker build -t myapp:v1 .

# watch the layers being created
# point out "Using cache" on rebuilds

# run it
docker run --rm -d -p 5000:5000 --name myapp myapp:v1
curl localhost:5000/health

# make a code change
echo "# comment" >> app.py

# rebuild - show cache usage
docker build -t myapp:v2 .

docker stop myapp
```

### Whiteboard: Multi-Stage Builds (10 min)

```mermaid
flowchart LR
    subgraph SINGLE["SINGLE STAGE = 800MB"]
        S1["Build tools"]
        S2["Source code"]
        S3["Dependencies"]
        S4["Test files"]
    end
    
    subgraph MULTI["MULTI-STAGE"]
        subgraph BUILDER["Stage 1: builder"]
            M1["Build tools"]
            M2["Compile/build"]
        end
        
        subgraph FINAL["Stage 2: final = 150MB"]
            M4["Runtime only"]
            M5["No build tools"]
        end
        
        BUILDER -->|"COPY --from=builder"| FINAL
    end
```

---

## Part 5: OCI and Container Registries (20 min)

### Whiteboard: OCI Ecosystem

```mermaid
flowchart TB
    subgraph OCI["Open Container Initiative (OCI)"]
        direction TB
        
        RT["Runtime Spec<br/>How to RUN containers<br/>(runc implements this)"]
        
        IMG["Image Spec<br/>How to PACKAGE containers<br/>(layers, manifest, config)"]
        
        DIST["Distribution Spec<br/>How to SHARE containers<br/>(push/pull to registries)"]
    end
    
    WHY["Why it matters:<br/>Docker builds → Push to ECR → Run on Kubernetes<br/>Everything interoperable!"]
    
    OCI --> WHY
```

### Terminal Demo - Push to Registry

```bash
# tag for a registry (Docker Hub example)
docker tag myapp:v1 USERNAME/myapp:v1

# login
docker login

# push
docker push USERNAME/myapp:v1

# show manifest/layers in Docker Hub UI
# or for ECR:
# aws ecr get-login-password | docker login --username AWS --password-stdin ACCOUNT.dkr.ecr.REGION.amazonaws.com
```

---

## Part 6: Putting It Together - Live Build (15 min)

```bash
cd ~/docker-starter

# show the application structure
tree .

# walk through Dockerfile explaining each line
cat Dockerfile

# build with no cache to show full process
docker build --no-cache -t flask-api:v1 .

# run and test
docker run --rm -d -p 5000:5000 --name api flask-api:v1

# test endpoints
curl localhost:5000/
curl localhost:5000/health

# show logs
docker logs api

# exec into container to explore
docker exec -it api sh
ls -la
cat /etc/os-release
exit

# cleanup
docker stop api
```

---

## Part 7: Wrap-up and Assignment Preview

### Whiteboard: Docker Cheat Sheet

| Command | Description |
|---------|-------------|
| `docker build -t name:tag .` | Build image |
| `docker run -d -p H:C name` | Run container |
| `docker ps` | List running |
| `docker logs container` | View output |
| `docker exec -it container sh` | Get shell |
| `docker stop container` | Stop it |

### Whiteboard: Dockerfile Order

```mermaid
flowchart TB
    A["1. FROM"] --> B["2. WORKDIR"]
    B --> C["3. COPY requirements"]
    C --> D["4. RUN install deps"]
    D --> E["5. COPY app code"]
    E --> F["6. CMD"]
    
    C -.- N1["Changes rarely"]
    E -.- N2["Changes often"]
```
