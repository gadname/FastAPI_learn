# FastAPI and Next.js Demo

This project includes a FastAPI backend and a Next.js frontend. Both services are started using Docker Compose.

## Development

```
docker-compose up --build
```

- FastAPI: http://localhost:8000
- Next.js: http://localhost:3000

The frontend has access to the backend via the `NEXT_PUBLIC_API_URL` environment variable.
