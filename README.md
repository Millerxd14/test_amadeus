# Class Scheduling System (Test)

This project is an API backend developed with FastAPI as a test system for class scheduling.

## Description

The system manages class scheduling and is based on three main models:

*   **Teacher**: Manages teacher information.
*   **Student**: Manages student information.
*   **ClassSchedule**: Represents a scheduled class between a teacher and a student.

Each model has its own CRUD (Create, Read, Update, Delete) operations.

---

## Authentication

To perform any operation on the API (except for login), **authentication is mandatory**. The system uses JWT-based authentication.

### Test Users

To facilitate testing, the following users have been created. The username corresponds to the document number.

*   **Teacher User**:
    *   **Username**: `19988022`
    *   **Password**: `123456`
*   **Student User**:
    *   **Username**: `1007708719`
    *   **Password**: `123456`

---

## Accessing the Application

*   **API Documentation (Swagger UI)**: The interactive documentation is available at the `/docs` path.
    *   URL: [http://localhost:5660/docs](http://localhost:5660/docs)
*   **Frontend (Login)**: The user interface for logging in is available at the `/static/videos/index.html` path.
    *   URL: [http://localhost:5660/static/videos/index.html](http://localhost:5660/static/videos/index.html)

---

## How to Run the Project

### Option 1: Using Docker (Recommended)

1.  **Build the Docker image:**
    ```bash
    docker build -t amadeus-fastapi-app .
    ```

2.  **Run the container:**
    ```bash
    docker run -p 5660:5660 amadeus-fastapi-app
    ```

3.  **(Optional) Run with Hot-Reload:**
    If you want code changes to be reflected automatically without rebuilding the image, mount a volume:
    ```bash
    docker run -p 5660:5660 -v .:/app amadeus-fastapi-app
    ```

### Option 2: Local Environment

1.  **Create and activate a virtual environment** (if you haven't already).
    ```bash
    # Create environment
    python -m venv venv
    # Activate on macOS/Linux
    source venv/bin/activate
    # Activate on Windows
    # venv\Scripts\activate
    ```

2.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Uvicorn server:**
    From the project root, run the following command:
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 5660 --reload --log-level info
    ```

---

## Testing

The project includes a test suite developed with `pytest`.

1.  **Test Location:**
    The tests are located in the `app/test/` directory.

2.  **Run the tests:**
    From the project root, simply run the command:
    ```bash
    pytest
    ```
