# blog-post-service
Service for managing blog posts


https://github.com/Kludex/fastapi-tips
https://github.com/zhanymkanov/fastapi-best-practices
## How to Use Docker Setup

This project is configured with Docker to simplify development and deployment. The setup includes separate configurations for development and production environments.

## Setup
- `pre-commit install`



## Run local server
`fastapi dev src/main.py`
spins up dev server with auto reload

## Test
`pytest`

## Prod deploy notes
`fastapi run src/main.py` include uvicorn


## Code Linting and Formatting
Ruff is used for linting and formatting.
https://docs.astral.sh/ruff/

configured as a pre-commit hook