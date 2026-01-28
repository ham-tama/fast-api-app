# FastAPI Project with Docker

A simple FastAPI application that returns a greeting message. This project includes Docker configuration for easy containerization and deployment.

## Project Structure

```
.
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker configuration
├── .dockerignore        # Files to exclude from Docker build
├── .gitignore          # Files to exclude from git
└── README.md           # This file
```

## Prerequisites

- Docker and Docker Compose (optional for compose-based setup)
- Python 3.9+ (if running locally without Docker)

## Quick Start with Docker

### 1. Build the Docker Image

```bash
docker build -t fastapi-app .
```

This command builds a Docker image named `fastapi-app` using the Dockerfile in the current directory.

### 2. Run the Container

```bash
docker run -d -p 8000:8000 --name my-fastapi-container fastapi-app
```

**Flags explanation:**
- `-d`: Run the container in detached mode (background)
- `-p 8000:8000`: Map port 8000 on your host to port 8000 in the container
- `--name my-fastapi-container`: Give the container a friendly name

### 3. Access the Application

Once the container is running, you can access the API at:

```
http://localhost:8000
```

### 4. View API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Docker Commands Reference

### View Running Containers

```bash
docker ps
```

### View All Containers (including stopped)

```bash
docker ps -a
```

### Stop a Container

```bash
docker stop my-fastapi-container
```

### Start a Stopped Container

```bash
docker start my-fastapi-container
```

### Remove a Container

```bash
docker rm my-fastapi-container
```

### View Container Logs

```bash
docker logs my-fastapi-container
```

### View Live Logs

```bash
docker logs -f my-fastapi-container
```

### Remove the Docker Image

```bash
docker rmi fastapi-app
```

## Running Without Docker (Local Development)

### 1. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The `--reload` flag enables auto-restart when code changes (useful for development).

## API Endpoints

- `GET /`: Returns a greeting message

Example response:
```json
{
  "Hello": "World"
}
```

## Troubleshooting

### Port Already in Use

If port 8000 is already in use, map to a different port:

```bash
docker run -d -p 8001:8000 --name my-fastapi-container fastapi-app
```

Then access at `http://localhost:8001`

### Container Exits Immediately

Check the logs:

```bash
docker logs my-fastapi-container
```

### Permission Denied Errors

On Linux/Mac, you may need to prefix commands with `sudo`:

```bash
sudo docker build -t fastapi-app .
sudo docker run -d -p 8000:8000 --name my-fastapi-container fastapi-app
```

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Uvicorn Documentation](https://www.uvicorn.org/)
