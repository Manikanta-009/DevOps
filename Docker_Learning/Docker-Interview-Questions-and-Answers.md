# Docker Interview Questions and Answers

---

## Basic Questions

### 1. What is Docker and why is it used?

Docker is a containerization platform that packages applications and their dependencies into lightweight, portable containers. It's used to:

- Ensure consistency across development, testing, and production environments ("works on my machine" problem)
- Isolate applications without the overhead of full virtual machines
- Enable microservices architecture
- Simplify CI/CD pipelines
- Improve resource utilization on servers

---

### 2. What is the difference between a Docker image and a container?

| Image | Container |
|-------|-----------|
| A read-only template with instructions for creating a container | A running instance of an image |
| Built from a Dockerfile | Created from an image using `docker run` |
| Stored in registries | Runs on a Docker host |
| Immutable | Has a writable layer on top |
| One image can produce many containers | Each container is a separate, isolated instance |

**Analogy:** An image is like a class; a container is like an object (instance of that class).

---

### 3. What is a Dockerfile?

A Dockerfile is a text file containing a sequence of instructions that Docker uses to build an image. Each instruction creates a new layer in the image. Key instructions include `FROM`, `RUN`, `COPY`, `CMD`, `ENTRYPOINT`, `ENV`, `EXPOSE`, and `WORKDIR`.

---

### 4. Explain Docker architecture.

Docker uses a client-server architecture:

- **Docker Client** — The CLI (`docker` command) that users interact with. Sends commands to the daemon via REST API.
- **Docker Daemon (dockerd)** — Runs on the host, manages building images, running containers, and managing networks/volumes.
- **containerd** — Container runtime that manages the lifecycle of containers.
- **runc** — Low-level OCI-compliant runtime that creates container processes using Linux kernel features (namespaces, cgroups).
- **Docker Registry** — Stores images (Docker Hub is the default public registry).

---

### 5. What are Docker namespaces?

Namespaces provide isolation for containers. Each container gets its own:

- **PID namespace** — Process isolation (container sees its own PID 1)
- **NET namespace** — Network isolation (own IP, ports, routing)
- **MNT namespace** — Filesystem mount isolation
- **UTS namespace** — Hostname isolation
- **IPC namespace** — Inter-process communication isolation
- **USER namespace** — User/group ID mapping

---

### 6. What are cgroups in Docker?

Control Groups (cgroups) limit and monitor the resources a container can use:

- CPU (time, cores)
- Memory (RAM, swap)
- Disk I/O (read/write bandwidth)
- Network bandwidth

Example: `docker run --memory 512m --cpus 1.5 myapp` limits the container to 512MB RAM and 1.5 CPU cores.

---

## Intermediate Questions

### 7. What is the difference between CMD and ENTRYPOINT?

| Feature | CMD | ENTRYPOINT |
|---------|-----|------------|
| Purpose | Default command/arguments | Fixed executable |
| Override behavior | Fully replaced by `docker run` arguments | Arguments appended; need `--entrypoint` to override |
| Best use | Default parameters that users might change | The primary executable of the container |

**Best practice:** Use together — ENTRYPOINT for the command, CMD for default arguments:
```dockerfile
ENTRYPOINT ["python", "app.py"]
CMD ["--port", "8000"]
```

---

### 8. What is a multistage build and why use it?

A multistage build uses multiple `FROM` statements in a single Dockerfile. Each `FROM` starts a new build stage. You can selectively copy artifacts from one stage to the next.

**Benefits:**
- Final image contains only runtime dependencies (no compilers, build tools)
- Dramatically smaller images (often 10x smaller)
- Smaller attack surface (fewer packages = fewer vulnerabilities)
- Single Dockerfile for the entire build pipeline

```dockerfile
FROM node:20 AS builder
WORKDIR /app
COPY . .
RUN npm ci && npm run build

FROM node:20-alpine
COPY --from=builder /app/dist ./dist
CMD ["node", "dist/index.js"]
```

---

### 9. Explain Docker networking types.

| Network Type | Description | Use Case |
|-------------|-------------|----------|
| **bridge** | Default. Creates an isolated virtual network on the host | Single-host container-to-container communication |
| **host** | Container shares the host's network stack directly | Performance-critical apps; no port mapping needed |
| **none** | No networking at all | Completely isolated/batch processing containers |
| **overlay** | Spans multiple Docker hosts | Multi-host (Docker Swarm) |
| **macvlan** | Assigns a real MAC address; container appears as physical device on LAN | Legacy apps requiring layer 2 connectivity |

Custom bridge networks provide automatic DNS resolution between containers by name.

---

### 10. What are Docker volumes? How do they differ from bind mounts?

| Feature | Volumes | Bind Mounts |
|---------|---------|-------------|
| Managed by | Docker | User (host filesystem) |
| Location | `/var/lib/docker/volumes/` | Any host path |
| Portability | Portable across hosts | Tied to specific host path |
| Backup | Via `docker volume` commands | Standard file system tools |
| Performance | Optimized by Docker | Depends on host filesystem |
| Best for | Production data persistence | Development (live code reload) |

---

### 11. What is Docker Compose?

Docker Compose is a tool for defining and running multi-container applications using a YAML file (`docker-compose.yml`). It allows you to:

- Define multiple services, networks, and volumes in one file
- Start/stop the entire application stack with one command
- Manage service dependencies and startup order
- Scale services horizontally
- Share environment configurations

---

### 12. How does Docker layer caching work?

Docker caches each layer during a build. When rebuilding, Docker checks if each instruction and its context have changed:

- If unchanged, the cached layer is reused (fast)
- If changed, that layer and ALL subsequent layers are rebuilt

**Optimization tip:** Order Dockerfile instructions from least to most frequently changing:
```dockerfile
FROM python:3.11         # Rarely changes
COPY requirements.txt . # Changes occasionally
RUN pip install -r ...   # Rebuilt only when requirements change
COPY . .                 # Changes frequently (source code)
```

---

### 13. What is the difference between COPY and ADD?

| Feature | COPY | ADD |
|---------|------|-----|
| Local files | Yes | Yes |
| Remote URLs | No | Yes (downloads from URL) |
| Tar extraction | No | Yes (auto-extracts .tar files) |
| Recommended | Yes (explicit, predictable) | Only when you need tar extraction |

**Best practice:** Always use `COPY` unless you specifically need ADD's tar extraction feature. Use `curl` or `wget` in a `RUN` step for downloads (allows cache control).

---

### 14. How do you reduce Docker image size?

1. **Use slim/alpine base images** — `python:3.11-slim` vs `python:3.11`
2. **Multistage builds** — Separate build and runtime stages
3. **Minimize layers** — Combine RUN commands with `&&`
4. **Clean up in the same layer** — `RUN apt-get install ... && rm -rf /var/lib/apt/lists/*`
5. **Use .dockerignore** — Exclude unnecessary files from build context
6. **Don't install unnecessary packages** — Use `--no-install-recommends`
7. **Order instructions by change frequency** — Maximize cache hits

---

### 15. What is a .dockerignore file?

Similar to `.gitignore`, it tells Docker which files/directories to exclude from the build context. This:

- Speeds up builds (less data sent to daemon)
- Prevents sensitive files from being included
- Avoids cache invalidation from irrelevant changes

```
node_modules
.git
.env
*.log
__pycache__
.pytest_cache
dist
build
```

---

## Advanced Questions

### 16. How do you handle secrets in Docker?

**Bad practices (never do this):**
- Hardcoding secrets in Dockerfile or image
- Passing via `ENV` (visible in `docker inspect`)
- Baking secrets into image layers

**Good practices:**
- **Docker Secrets** (Swarm mode) — Mounted as files in `/run/secrets/`
- **Runtime environment variables** — Passed at `docker run` time via `--env-file`
- **Secret management tools** — HashiCorp Vault, AWS Secrets Manager
- **BuildKit secrets** — `RUN --mount=type=secret,id=mysecret` (not stored in layers)

```dockerfile
# BuildKit secret (never persisted in image)
RUN --mount=type=secret,id=npm_token \
    NPM_TOKEN=$(cat /run/secrets/npm_token) npm ci
```

---

### 17. Explain Docker health checks.

Health checks let Docker monitor whether a container is functioning correctly:

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=60s \
  CMD curl -f http://localhost:8080/health || exit 1
```

Container states: `starting` → `healthy` → `unhealthy`

Used by:
- Docker Compose `depends_on` with `condition: service_healthy`
- Orchestrators (Swarm, Kubernetes) for restart/replacement decisions
- Load balancers for routing traffic

---

### 18. What are Docker container restart policies?

| Policy | Behavior |
|--------|----------|
| `no` | Never restart (default) |
| `always` | Always restart, regardless of exit code |
| `on-failure[:max]` | Restart only on non-zero exit code, with optional max retries |
| `unless-stopped` | Always restart unless explicitly stopped by user |

```bash
docker run --restart unless-stopped myapp
```

---

### 19. How does Docker handle logging?

Docker captures stdout/stderr from container processes. Logging drivers determine where logs go:

| Driver | Destination |
|--------|-------------|
| `json-file` | Local JSON files (default) |
| `syslog` | Syslog daemon |
| `journald` | systemd journal |
| `fluentd` | Fluentd collector |
| `awslogs` | AWS CloudWatch Logs |
| `gcplogs` | Google Cloud Logging |
| `none` | No logging |

```bash
docker run --log-driver=awslogs --log-opt awslogs-group=myapp myapp
```

**Best practice:** Applications should log to stdout/stderr; let Docker route logs to the appropriate destination.

---

### 20. What is the difference between Docker Swarm and Kubernetes?

| Feature | Docker Swarm | Kubernetes |
|---------|-------------|------------|
| Complexity | Simple, easy setup | Complex, steep learning curve |
| Scaling | Manual scaling only | Advanced auto-scaling (HPA, VPA) |
| Networking | Built-in overlay | CNI plugins (Calico, Flannel, etc.) |
| Load balancing | Built-in | Ingress controllers |
| Community | Smaller | Very large, industry standard |
| Best for | Small-medium deployments | Large, complex production systems |

---

### 21. How do you debug a container that won't start?

```bash
# Check logs
docker logs <container>

# Run interactively to see errors
docker run -it <image> bash

# Inspect the container config
docker inspect <container>

# Check events
docker events --filter container=<name>

# Override entrypoint to get a shell
docker run -it --entrypoint /bin/sh <image>

# Check resource constraints
docker stats <container>
```

---

### 22. What are Docker security best practices?

1. **Run as non-root** — Use `USER` instruction in Dockerfile
2. **Use minimal base images** — Alpine or distroless
3. **Scan images for vulnerabilities** — `docker scout`, Trivy, Snyk
4. **Don't store secrets in images** — Use runtime injection or secret mounts
5. **Use read-only filesystem** — `docker run --read-only`
6. **Drop capabilities** — `docker run --cap-drop ALL --cap-add NET_BIND_SERVICE`
7. **Set resource limits** — Prevent DoS via `--memory` and `--cpus`
8. **Keep images updated** — Regularly rebuild with latest base images
9. **Use content trust** — `DOCKER_CONTENT_TRUST=1` for signed images
10. **Network segmentation** — Use custom networks; limit exposure

---

### 23. Explain Docker content trust and image signing.

Docker Content Trust (DCT) uses digital signatures to verify image integrity and publisher identity:

```bash
export DOCKER_CONTENT_TRUST=1
docker pull myregistry/myapp:1.0   # Only pulls if signed
docker push myregistry/myapp:1.0   # Signs on push
```

This prevents:
- Pulling tampered images
- Man-in-the-middle attacks on image distribution
- Running images from unauthorized publishers

---

### 24. What happens when you run `docker run hello-world`?

1. Docker client sends the command to the Docker daemon
2. Daemon checks if the `hello-world` image exists locally
3. If not found, pulls it from Docker Hub (default registry)
4. Daemon creates a new container from the image
5. Daemon allocates a read-write filesystem layer
6. Daemon creates a network interface and assigns an IP
7. Daemon starts the container and executes the default command
8. The process outputs text to stdout (captured by Docker)
9. The process exits; container enters "stopped" state

---

### 25. How do you optimize Docker builds for CI/CD?

1. **Leverage BuildKit** — `DOCKER_BUILDKIT=1` for parallel stage builds and better caching
2. **Use cache mounts** — `RUN --mount=type=cache,target=/root/.cache pip install`
3. **Multi-stage builds** — Build and test in early stages, slim runtime in final stage
4. **External cache sources** — `docker build --cache-from myregistry/myapp:cache`
5. **Minimize build context** — Proper `.dockerignore`
6. **Pin base image digests** — Reproducible builds: `FROM python@sha256:abc123...`
7. **Parallel builds** — Build independent services concurrently
8. **Layer ordering** — Dependencies before source code

```bash
# BuildKit with registry cache
docker buildx build \
  --cache-from type=registry,ref=myregistry/myapp:cache \
  --cache-to type=registry,ref=myregistry/myapp:cache \
  -t myapp:latest .
```

---

### 26. What is the difference between `docker stop` and `docker kill`?

| Command | Signal | Behavior |
|---------|--------|----------|
| `docker stop` | SIGTERM, then SIGKILL after timeout (10s default) | Graceful shutdown; allows cleanup |
| `docker kill` | SIGKILL (immediate) | Immediate termination; no cleanup |

Always prefer `docker stop` for graceful shutdown. Use `docker kill` only when a container is unresponsive.

---

### 27. How do containers communicate in Docker Compose?

In Docker Compose, services on the same network communicate using:

- **Service name as hostname** — `http://web:8000` from another service
- **Automatic DNS resolution** — Compose creates a default network and registers service names
- **Custom networks** — For isolation between service groups
- **Service aliases** — Alternative DNS names for a service

```yaml
services:
  web:
    networks:
      backend:
        aliases:
          - api
  db:
    networks:
      - backend

networks:
  backend:
```

The `web` service is reachable as both `web` and `api` from other services on the `backend` network.

---

### 28. What is Docker BuildKit?

BuildKit is Docker's next-generation build engine (default since Docker 23.0):

- **Parallel execution** — Independent build stages run concurrently
- **Better caching** — More granular cache invalidation
- **Secret mounts** — `RUN --mount=type=secret` (not stored in layers)
- **SSH forwarding** — `RUN --mount=type=ssh` for private repo access
- **Cache mounts** — `RUN --mount=type=cache` for package manager caches
- **Build output** — Export to OCI, tarball, or directly to registry

```bash
# Enable BuildKit (default in newer Docker versions)
DOCKER_BUILDKIT=1 docker build .

# Or use buildx
docker buildx build --platform linux/amd64,linux/arm64 -t myapp .
```

---

### 29. How do you handle container orchestration?

Container orchestration automates deployment, scaling, networking, and management of containerized applications:

- **Docker Swarm** — Built into Docker, simpler, good for smaller deployments
- **Kubernetes** — Industry standard, complex but powerful, managed options (EKS, GKE, AKS)
- **Amazon ECS** — AWS-native, integrates with AWS services

Key orchestration features:
- Service discovery and load balancing
- Rolling updates and rollbacks
- Self-healing (restart failed containers)
- Horizontal scaling
- Secret and config management
- Resource scheduling

---

### 30. What is a dangling image and how do you clean it up?

A dangling image is an untagged image that is no longer referenced by any container or other image. These accumulate during builds when new images replace old ones.

```bash
# List dangling images
docker images -f "dangling=true"

# Remove dangling images
docker image prune

# Remove ALL unused images (not just dangling)
docker image prune -a

# Nuclear option: clean everything unused
docker system prune -a --volumes
```

---

## Scenario-Based Questions

### 31. A container is consuming too much memory. How do you handle it?

```bash
# Check current usage
docker stats <container>

# Set memory limits
docker run --memory 512m --memory-swap 1g myapp

# Update running container limits
docker update --memory 512m <container>

# In Docker Compose
services:
  web:
    deploy:
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M
```

Investigate the cause: check for memory leaks, inefficient caching, or under-provisioning.

---

### 32. How would you migrate a Docker application to production?

1. **Optimize the Dockerfile** — Multistage build, minimal base image, non-root user
2. **Externalize configuration** — Environment variables, config files mounted at runtime
3. **Set up health checks** — In Dockerfile and orchestrator
4. **Configure logging** — Send to centralized logging (CloudWatch, ELK, etc.)
5. **Set resource limits** — Memory and CPU constraints
6. **Enable restart policies** — `unless-stopped` or orchestrator-managed
7. **Scan for vulnerabilities** — Integrate into CI pipeline
8. **Use a private registry** — ECR, GCR, or self-hosted
9. **Implement CI/CD** — Automated build, test, scan, deploy pipeline
10. **Plan for monitoring** — Metrics, alerts, dashboards

---

### 33. Your Docker build is slow. How do you speed it up?

1. **Fix layer ordering** — Put rarely-changing instructions first
2. **Use .dockerignore** — Exclude unnecessary files from build context
3. **Leverage BuildKit** — Parallel stage execution, cache mounts
4. **Use multistage builds** — Avoid re-downloading in test/lint stages
5. **Cache package manager** — `RUN --mount=type=cache,target=/root/.cache/pip`
6. **Use registry cache** — `--cache-from` for CI environments
7. **Minimize context size** — Only send necessary files to daemon
8. **Combine RUN commands** — Fewer layers, but balance with cache granularity
9. **Use specific base image tags** — Avoid re-pulling `:latest`

---

### 34. How do you handle database migrations in Docker?

Common approaches:

1. **Init scripts** — Mount SQL files to `/docker-entrypoint-initdb.d/` (first run only)
2. **Entrypoint wrapper** — Script that runs migrations before starting the app
3. **Separate migration container** — Run as a one-off job before deploying the app
4. **Compose depends_on** — Ensure DB is healthy before migration runs

```yaml
services:
  migrate:
    image: myapp
    command: ["python", "manage.py", "migrate"]
    depends_on:
      db:
        condition: service_healthy

  web:
    image: myapp
    depends_on:
      migrate:
        condition: service_completed_successfully
```

---

### 35. How do you run Docker in production securely?

- Use orchestration (Kubernetes/ECS) for high availability
- Enable Docker Content Trust for image verification
- Run containers as non-root with minimal capabilities
- Use read-only root filesystem where possible
- Implement network policies to restrict inter-container traffic
- Regularly patch and update base images
- Use image scanning in CI/CD pipelines
- Set resource limits to prevent resource exhaustion
- Separate sensitive services into isolated networks
- Enable audit logging on the Docker daemon
- Use secrets management (not environment variables) for credentials
