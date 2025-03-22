# blog-post-service
Service for managing blog posts


https://github.com/Kludex/fastapi-tips
https://github.com/zhanymkanov/fastapi-best-practices
## How to Use Docker Setup

This project is configured with Docker to simplify development and deployment. The setup includes separate configurations for development and production environments.

## Setup
- `pre-commit install`

### Code Linting and Formatting
Ruff is used for linting and formatting.
https://docs.astral.sh/ruff/


### Development

1. **Start the development server** with hot-reloading:
   ```bash
   docker-compose up --build dev-server
   ```
   This will start the FastAPI application at http://localhost:8000 with auto-reload enabled.

2. **Run tests**:
   ```bash
   docker compose run --build --rm test
   ```

3. **Run linting**:
   ```bash
   docker compose run --build --rm lint
   ```

4. **Run a custom command** in the development container:
   ```bash
   docker compose run --build --rm dev-server <command>
   ```
   For example:
   ```bash
   docker compose run --build --rm dev-server python -m src.some_script
   ```

### Production

Build and run the production-ready server:
```bash
docker compose build server
docker compose up prod`
```
> **Note**: The production service is configured without development dependencies and doesn't mount local files as volumes, making it suitable for deployment.

### Docker Configuration

- **Multi-stage builds**: The Dockerfile uses multi-stage builds to create efficient images
  - `base`: Contains common Python dependencies
  - `development`: Includes development tools and testing libraries
  - `server`: Clean production image without dev dependencies

- **Volume mounting**: In development mode, your local code is mounted into the container, allowing for instant code changes without rebuilding.

### Project Structure

- `src/`: Application source code
- `requirements.txt`: Production dependencies
- `requirements-dev.txt`: Development dependencies