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
- **Method:** `POST`
- **URL:** `http://127.0.0.1:8000/signup`
- **Body:** `raw` (JSON)
    ```json
    {
        "name": "John Doe",
        "email": "john@example.com",
        "password": "secretpassword"
    }
    ```

### 2. Login
- **Method:** `POST`
- **URL:** `http://127.0.0.1:8000/login`
- **Body:** `raw` (JSON)
    ```json
    {
        "email": "john@example.com",
        "password": "secretpassword"
    }
    ```
- **Response:**
    ```json
    {
        "access_token": "eyJhbG...",
        "token_type": "bearer"
    }
    ```
    *Copy the `access_token` for authenticated requests.*

### 3. Create Class (Authenticated)
- **Method:** `POST`
- **URL:** `http://127.0.0.1:8000/classes`
- **Auth:** `Bearer Token` (Paste your access token)
- **Body:** `raw` (JSON)
    ```json
    {
        "name": "Power Yoga",
        "start_time": "2023-11-01T10:00:00",
        "duration": 60,
        "total_slots": 20
    }
    ```

### 4. Get All Classes
- **Method:** `GET`
- **URL:** `http://127.0.0.1:8000/classes`

### 5. Book a Class (Authenticated)
- **Method:** `POST`
- **URL:** `http://127.0.0.1:8000/book`
- **Auth:** `Bearer Token` (Paste your access token)
- **Body:** `raw` (JSON)
    ```json
    {
        "class_id": 1
    }
    ```

### 6. View My Bookings (Authenticated)
- **Method:** `GET`
- **URL:** `http://127.0.0.1:8000/bookings`
- **Auth:** `Bearer Token` (Paste your access token)

## Project Structure
- `main.py`: Main application and endpoints.
- `models.py`: Database models.
- `schemas.py`: Pydantic models for request/response.
- `database.py`: Database connection setup.
- `requirements.txt`: Python dependencies.
