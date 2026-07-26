# ============ Base Image ============
# Official nginx on Alpine Linux (~40MB total — tiny compared to full OS images)
FROM nginx:1.27-alpine

# ============ Metadata ============
LABEL org.opencontainers.image.title="Docker Welcome Page"
LABEL org.opencontainers.image.description="A minimal static site served by nginx — the simplest way to see Docker in action"
LABEL org.opencontainers.image.version="1.0.0"

# ============ Copy Assets ============
# Copy the HTML file into nginx's default document root
# Nginx automatically serves index.html when a directory is requested
# Note: build from the repo root (not examples/):
#   docker build -t docker-welcome -f Docker_Learning/examples/Dockerfile .
COPY Docker_Learning/examples/index.html /usr/share/nginx/html/index.html
# Copy the Docker icon image one level up from the web root
# The HTML references it as ../images/docker-icon.png
COPY Docker_Learning/images/docker-icon.png /usr/share/nginx/images/docker-icon.png

# ============ Port ============
# Document the port the container listens on (informational only)
EXPOSE 80

# ============ Runtime ============
# nginx official images already use "daemon off;" as the default CMD,
# so we could omit this — included explicitly for clarity in this example.
# Running in the foreground keeps the container alive.
CMD ["nginx", "-g", "daemon off;"]
