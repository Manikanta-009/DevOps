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
COPY index.html /usr/share/nginx/html/index.html

# ============ Port ============
# Document the port the container listens on (informational only)
EXPOSE 80

# ============ Runtime ============
# nginx official images already use "daemon off;" as the default CMD,
# so we could omit this — included explicitly for clarity in this example.
# Running in the foreground keeps the container alive.
CMD ["nginx", "-g", "daemon off;"]
