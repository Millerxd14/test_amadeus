# Sistema de Agendamiento de Clases (Prueba)

Este proyecto es un backend de API desarrollado con FastAPI como un sistema de prueba para el agendamiento de clases.

## Descripción

El sistema gestiona el agendamiento de clases y se basa en tres modelos principales:

*   **Profesor (`Teacher`)**: Gestiona la información de los profesores.
*   **Estudiante (`Student`)**: Gestiona la información de los estudiantes.
*   **Clase Agendada (`ClassSchedule`)**: Representa una clase programada entre un profesor y un estudiante.

Cada modelo cuenta con sus propias operaciones CRUD (Crear, Leer, Actualizar, Eliminar).

---

## Autenticación

Para realizar cualquier operación en la API (excepto el login), es **obligatorio estar autenticado**. El sistema utiliza autenticación basada en JWT.

### Usuarios de Prueba

Para facilitar las pruebas, se han creado los siguientes usuarios. El nombre de usuario corresponde al número de documento.

*   **Usuario Profesor**:
    *   **Username**: `19988022`
    *   **Password**: `123456`
*   **Usuario Estudiante**:
    *   **Username**: `1007708719`
    *   **Password**: `123456`

---

## Acceso a la Aplicación

*   **Documentación de la API (Swagger UI)**: La documentación interactiva se encuentra en la ruta `/docs`.
    *   URL: [http://localhost:5660/docs](http://localhost:5660/docs)
*   **Frontend (Login)**: La interfaz de usuario para iniciar sesión se encuentra en la ruta `/static/videos/index.html`.
    *   URL: [http://localhost:5660/static/videos/index.html](http://localhost:5660/static/videos/index.html)

---

## Cómo Ejecutar el Proyecto

### Opción 1: Usando Docker (Recomendado)

1.  **Construir la imagen de Docker:**
    ```bash
    docker build -t amadeus-fastapi-app .
    ```

2.  **Ejecutar el contenedor:**
    ```bash
    docker run -p 5660:5660 amadeus-fastapi-app
    ```

3.  **(Opcional) Ejecutar con Hot-Reload:**
    Si deseas que los cambios en el código se reflejen automáticamente sin tener que reconstruir la imagen, monta un volumen:
    ```bash
    docker run -p 5660:5660 -v .:/app amadeus-fastapi-app
    ```

### Opción 2: Entorno Local

1.  **Crear y activar un entorno virtual** (si no lo has hecho).
    ```bash
    # Crear entorno
    python -m venv venv
    # Activar en macOS/Linux
    source venv/bin/activate
    # Activar en Windows
    # venv\Scripts\activate
    ```

2.  **Instalar las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Ejecutar el servidor Uvicorn:**
    Desde la raíz del proyecto, ejecuta el siguiente comando:
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 5660 --reload --log-level info
    ```

---

## Pruebas (Testing)

El proyecto incluye una suite de pruebas desarrollada con `pytest`.

1.  **Ubicación de las pruebas:**
    Las pruebas se encuentran en el directorio `app/test/`.

2.  **Ejecutar las pruebas:**
    Desde la raíz del proyecto, simplemente ejecuta el comando:
    ```bash
    pytest
    ```
