# Fitness Studio Booking API

This is a simple Booking API for a fitness studio built with Python and FastAPI.

## Tech Stack
- **Language:** Python
- **Framework:** FastAPI
- **Database:** SQLite
- **Authentication:** JWT (JSON Web Tokens)

## Setup Instructions

1. **Install Python** (if not installed).
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   (Note: You might need to create a virtual environment first: `python -m venv .venv` and activate it)

## How to Run

1. **Start the Server**:
   ```bash
   uvicorn main:app --reload
   ```
   The API will be running at `http://127.0.0.1:8000`.

2. **Seed Data (Optional)**:
   You can run the seed script to create a test user and some classes:
   ```bash
   python seed.py
   ```
   Test Credentials: `test@example.com` / `password123`

3. **Access Documentation**:
   Go to `http://127.0.0.1:8000/docs` to use the interactive Swagger UI.

## API Usage

### 1. Signup
**cURL:**
```bash
curl -X POST "http://127.0.0.1:8000/signup" -H "Content-Type: application/json" -d "{\"name\": \"John Doe\", \"email\": \"john@example.com\", \"password\": \"secretpassword\"}"
```

### 2. Login
**cURL:**
```bash
curl -X POST "http://127.0.0.1:8000/login" -H "Content-Type: application/json" -d "{\"email\": \"john@example.com\", \"password\": \"secretpassword\"}"
```
**Response:**
```json
{
  "access_token": "eyJhbG...",
  "token_type": "bearer"
}
```

### 3. View Classes
**cURL:**
```bash
curl -X GET "http://127.0.0.1:8000/classes"
```

### 4. Create Class (Authenticated)
Replace `TOKEN` with your access token.
**cURL:**
```bash
curl -X POST "http://127.0.0.1:8000/classes" -H "Authorization: Bearer TOKEN" -H "Content-Type: application/json" -d "{\"name\": \"Power Yoga\", \"start_time\": \"2023-11-01T10:00:00\", \"duration\": 60, "total_slots": 20}"
```

### 5. Book a Class (Authenticated)
**cURL:**
```bash
curl -X POST "http://127.0.0.1:8000/book" -H "Authorization: Bearer TOKEN" -H "Content-Type: application/json" -d "{\"class_id\": 1}"
```

### 6. View My Bookings (Authenticated)
**cURL:**
```bash
curl -X GET "http://127.0.0.1:8000/bookings" -H "Authorization: Bearer TOKEN"
```

## Project Structure
- `main.py`: Main application and endpoints.
- `models.py`: Database models.
- `schemas.py`: Pydantic models for request/response.
- `database.py`: Database connection setup.
- `requirements.txt`: Python dependencies.
