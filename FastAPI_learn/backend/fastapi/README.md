# Cat Management API

A FastAPI-based REST API for managing cat information.

## Setup Instructions

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize the database:
```bash
# Initialize Alembic
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```

4. Run the application:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access:
- Swagger UI documentation: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

## API Endpoints

- `GET /api/v1/cats/` - List all cats
- `GET /api/v1/cats/{cat_id}` - Get a specific cat
- `POST /api/v1/cats/` - Create a new cat
- `PUT /api/v1/cats/{cat_id}` - Update a cat
- `DELETE /api/v1/cats/{cat_id}` - Delete a cat

## Example Request

Creating a new cat:
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