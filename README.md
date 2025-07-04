# FastAPI and Next.js Demo

This project includes a FastAPI backend and a Next.js frontend. Both services are started using Docker Compose.

## Authentication

This application now features user authentication. To access the main functionalities, users must first register and then log in.

**Registration:**
1.  Navigate to the `/register` page on the frontend (e.g., `http://localhost:3000/register`).
2.  Provide a unique username and a password.
3.  Upon successful registration, you will be redirected to the login page.

**Login:**
1.  Navigate to the `/login` page (e.g., `http://localhost:3000/login`).
2.  Enter your registered username and password.
3.  On successful login, you will be granted access to the application's main features and redirected to the homepage.

**Authentication API Endpoints:**
For developers interacting directly with the API, the following authentication endpoints are available:
*   `POST /api/v1/auth/register`: Creates a new user. Requires `username` and `password` in the request body.
*   `POST /api/v1/auth/login`: Authenticates a user. Requires `username` and `password` as form data. Returns an access token.
*   `GET /api/v1/auth/users/me`: Retrieves the details of the currently authenticated user. Requires a valid JWT in the Authorization header.

## Development

```
docker-compose up --build
```

- FastAPI: http://localhost:8000
- Next.js: http://localhost:3000

The frontend has access to the backend via the `NEXT_PUBLIC_API_URL` environment variable.

**Note:** After starting the application, you will need to register a new user and log in to access protected routes and features. The main page will redirect to `/login` if you are not authenticated.

## Running Tests

**Backend Tests:**
To run the backend tests (unit and integration tests for FastAPI):
1. Ensure you are in the `backend/fastapi` directory.
2. Make sure development dependencies are installed (e.g., `poetry install --with dev`).
3. Run pytest:
   ```bash
   poetry run pytest
   ```
   Or, if your environment is already activated:
   ```bash
   pytest
   ```
The tests utilize an in-memory SQLite database by default for isolated testing.
