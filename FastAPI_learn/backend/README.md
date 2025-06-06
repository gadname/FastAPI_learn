# Cat Management API

A FastAPI-based REST API for managing cat information.

## Project Structure

```
FastAPI_learn/backend/
├── alembic/
│   └── env.py
├── api/
│   └── v1/
│       └── endpoints/
│           └── cats.py
├── cruds/
│   └── cat.py
├── db/
│   ├── base_class.py
│   └── session.py
├── models/
│   └── cat.py
├── schemas/
│   └── cat.py
├── alembic.ini
├── main.py
├── requirements.txt
└── README.md
```

## Setup Instructions

1. Navigate to the backend directory:
```bash
cd /workspace/FastAPI_learn/backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
# Initialize Alembic (if not already done)
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```

5. Run the application:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access:
- Swagger UI documentation: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

## API Endpoints

### Cat Management

- `GET /api/v1/cats/` - List all cats
- `GET /api/v1/cats/{cat_id}` - Get a specific cat
- `POST /api/v1/cats/` - Create a new cat
- `PUT /api/v1/cats/{cat_id}` - Update a cat
- `DELETE /api/v1/cats/{cat_id}` - Delete a cat

### Example Requests

#### Create a new cat:
```bash
curl -X POST "http://localhost:8000/api/v1/cats/" \
     -H "Content-Type: application/json" \
     -d '{
           "name": "タマ",
           "breed": "雑種",
           "age": 3,
           "weight": 4.5
         }'
```

#### Get all cats:
```bash
curl "http://localhost:8000/api/v1/cats/"
```

#### Get a specific cat:
```bash
curl "http://localhost:8000/api/v1/cats/1"
```

#### Update a cat:
```bash
curl -X PUT "http://localhost:8000/api/v1/cats/1" \
     -H "Content-Type: application/json" \
     -d '{
           "name": "タマちゃん",
           "age": 4
         }'
```

#### Delete a cat:
```bash
curl -X DELETE "http://localhost:8000/api/v1/cats/1"
```

## Database

The application uses SQLite by default. The database file (`sql_app.db`) will be created in the backend directory.

To use a different database (e.g., PostgreSQL), update the `SQLALCHEMY_DATABASE_URL` in `db/session.py`.

## Development

For development, the application runs with auto-reload enabled. Any changes to the code will automatically restart the server.

## Production Considerations

For production deployment:

1. Use a production-grade database (PostgreSQL, MySQL, etc.)
2. Update CORS settings in `main.py` to restrict allowed origins
3. Use environment variables for sensitive configuration
4. Add proper authentication and authorization
5. Configure proper logging
6. Use a production ASGI server like Gunicorn with Uvicorn workers