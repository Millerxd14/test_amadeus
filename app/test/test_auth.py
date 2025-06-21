# tests/test_auth.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database.connection import Base, get_db
from app.schemas.teacher import TeacherCreate
from app.crud import teacher as teacher_crud
import os

# --- Configuración de la Base de Datos de Prueba ---
# Usamos una base de datos SQLite en memoria para los tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

# Crear un profesor de prueba directamente en la base de datos ya que el profesor es el admin en este caso
db = TestingSessionLocal()
try:
    teacher_data = TeacherCreate(
        first_name="Test",
        last_name="DirectDB",
        age=35,
        document_number="123456",
        password="123456"
    )
    existing_teacher = teacher_crud.get_teacher_by_document_number(db, document_number=teacher_data.document_number)
    if not existing_teacher:
        teacher_crud.create_teacher(db=db, teacher=teacher_data)
        db.commit()
finally:
    db.close()

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Aplicamos la sobrescritura
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_login():
    response = client.post(
        "/auth/token",
        data={"username": "123456", "password": "123456"}
    )
    assert response.status_code == 200
    json_response = response.json()
    assert "access_token" in json_response
    assert json_response["token_type"] == "bearer"

def test_create_teacher_wihtout_token():
    response = client.post(
        "/teacher/",
        json={"first_name": "Test", "last_name": "User", "age": 30, "document_number": "123456789", "password": "testpassword"}
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Not authenticated"


def test_create_teacher_wiht_token():
    login_response = client.post(
        "/auth/token",
        data={"username": "123456", "password": "123456"}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post(
        "/teacher/",
        headers=headers,
        json={"first_name": "Test", "last_name": "UserToken", "age": 30, "document_number": "987654321", "password": "testpassword"}
    )
    print(response.json())
    assert response.status_code == 201
    assert response.json()["document_number"] == "987654321"


def test_login_wrong_password():
    response = client.post(
        "/auth/token",
        data={"username": "123456789", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect document number or password"}

def test_login_wrong_username():
    response = client.post(
        "/auth/token",
        data={"username": "nonexistentuser", "password": "testpassword"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect document number or password"}

# Eliminar archivo de base de datos
@pytest.fixture(scope="session", autouse=True)
def cleanup_test_db():
    yield
    engine.dispose()
    if os.path.exists("./test.db"):
        os.remove("./test.db")
        