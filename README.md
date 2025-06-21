# Amadeus Test API

A FastAPI project for testing the Amadeus API integration.

## Setup

1. Ensure Python 3.7+ is installed
2. Create a virtual environment (already done)
```
python -m venv venv
```

3. Activate the virtual environment
```
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

4. Install dependencies
```
pip install -r requirements.txt
```

## Running the application

```
uvicorn main:app --reload
```

The API will be available at http://127.0.0.1:8000

## API Documentation

FastAPI automatically generates API documentation:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Running with Docker

1.  **Build the Docker image:**
    ```bash
    docker build -t amadeus-fastapi-app .
    ```

2.  **Run the Docker container:**
    ```bash
    docker run -p 5660:5660 -v .:/app amadeus-fastapi-app
    ```

The application will be accessible at [http://localhost:5660](http://localhost:5660) and the API documentation at [http://localhost:5660/docs](http://localhost:5660/docs).
