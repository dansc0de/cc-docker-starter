# OCI (Open Container Initiative) - Whiteboard Lesson Plan

## Part 1: The Problem

### Whiteboard: The 2014 Container World

```mermaid
flowchart TD
    subgraph world2014["2014: Docker's World"]
        A[Docker builds images] --> B[Docker Hub]
        B --> C[Docker runs containers]
    end
    
    D["Everything is Docker.<br/>What if Docker goes away?<br/>What if we want alternatives?"]
    
    world2014 --> D
```

**Discussion questions:**
- "What happens if you build with Docker but want to run on something else?"
- "Can Google's container tools read Docker's format?"
- "This is vendor lock-in"

**Key point to write:**

> 2015: Docker donates their formats to create open standards

---

## Part 2: The Three OCI Specs

### Whiteboard: OCI Specifications

```mermaid
flowchart TB
    subgraph OCI["Open Container Initiative (Linux Foundation, 2015)"]
        direction TB
        
        subgraph Runtime["RUNTIME SPEC - How to RUN"]
            R1["config.json + rootfs"]
            R2["You saw this with runc!"]
            R3["Implementations: runc, crun, youki"]
        end
        
        subgraph Image["IMAGE SPEC - How to PACKAGE"]
            I1["Layers - the layer cake"]
            I2["Manifest - list of layers"]
            I3["Config - env vars, cmd, entrypoint"]
        end
        
        subgraph Distribution["DISTRIBUTION SPEC - How to SHARE"]
            D1["Push/pull API"]
            D2["Content addressing with SHA256"]
            D3["Registries: Docker Hub, ECR, GCR, Harbor"]
        end
    end
```

### Whiteboard: The Interoperability Flow

```mermaid
flowchart LR
    A["Build with<br/>Docker"] --> B["Push to<br/>ECR"]
    B --> C["Run on<br/>Kubernetes"]
    
    A -.- A1["Image Spec"]
    B -.- B1["Distribution Spec"]
    C -.- C1["Runtime Spec"]
```

**Key point to write in different color:**

> ALL INTEROPERABLE because of OCI!

---

## Part 3: Distribution Spec Deep Dive

### Whiteboard: Push Flow

```mermaid
sequenceDiagram
    participant C as Client
    participant R as Registry
    
    Note over C,R: docker push myapp:v1
    
    C->>R: 1. POST /v2/myapp/blobs/uploads/
    Note right of R: "I want to upload"
    
    C->>R: 2. PUT layer-1 (sha256:abc123)
    Note right of R: Upload each layer
    
    C->>R: 3. PUT layer-2 (sha256:def456)
    Note right of R: Only if not exists!
    
    C->>R: 4. PUT manifest (links layers)
    Note right of R: "Here's how they connect"
```

### Whiteboard: Pull Flow

```mermaid
sequenceDiagram
    participant C as Client
    participant R as Registry
    
    Note over C,R: docker pull myapp:v1
    
    C->>R: 1. GET /v2/myapp/manifests/v1
    Note right of R: "What layers do I need?"
    R-->>C: manifest.json
    
    C->>R: 2. GET /v2/myapp/blobs/sha256:abc
    Note right of R: Download only layers not cached
    R-->>C: layer-1 data
```

### Whiteboard: Content Addressing

```mermaid
flowchart LR
    A["Layer Contents"] --> B["SHA256 Hash"]
    B --> C["sha256:abc123def456..."]
    
    C --> D["Same content = Same hash"]
    D --> E["No re-upload needed!"]
    D --> F["Integrity verification built-in"]
```

**Key insight to write:**

- Layer identified by hash of contents
- Same content = same hash = no re-upload
- Integrity verification built-in

**Discussion:** "What happens if you push the same image twice?" (Nothing uploads, layers already exist)

---

## Part 4: Why This Matters

### Whiteboard: The Ecosystem

```mermaid
flowchart LR
    subgraph Build["BUILD WITH"]
        B1[Docker]
        B2[Podman]
        B3[Buildah]
        B4[GitHub Actions]
    end
    
    subgraph Store["STORE IN"]
        S1[Docker Hub]
        S2[AWS ECR]
        S3[Google GCR]
        S4[Azure ACR]
        S5[Harbor]
    end
    
    subgraph Run["RUN ON"]
        R1[Docker]
        R2[Kubernetes]
        R3[containerd]
        R4[Podman]
    end
    
    Build --> Store --> Run
```

**Final key point:**

> OCI = The reason containers became an industry standard, not just "Docker"
>
> ALL COMPATIBLE! No vendor lock-in.

---

## Demo

```bash
# Show that an image is just a manifest + layers
docker pull nginx:alpine
docker inspect nginx:alpine | jq '.[0].RootFS.Layers'

# See the manifest
docker manifest inspect nginx:alpine

# Show content-addressable storage
ls -la /var/lib/docker/image/overlay2/layerdb/sha256/
```
