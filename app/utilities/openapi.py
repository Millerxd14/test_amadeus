# app/utils/openapi.py

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

def create_custom_openapi(app: FastAPI):
    """
    Esta función personaliza el schema de OpenAPI generado por FastAPI.
    Añade un botón de "Authorize" global para poder probar los endpoints
    protegidos con JWT desde la documentación de Swagger.
    """



    if app.openapi_schema:
        return app.openapi_schema

    # Genera el schema base
    openapi_schema = get_openapi(
        title="Reserva de Clases API",
        version="1.0.0",
        description="This is a custom OpenAPI to reserve classes with JWT authentication.",
        routes=app.routes,
    )

    # Añade la definición del esquema de seguridad (JWT Bearer)
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Introduce tu token JWT aquí. Ejemplo: 'Bearer eyJhbGciOiJIUzI1Ni...'"
        }
    }

    # Aplica este esquema de seguridad a todas las rutas de la API
    openapi_schema["security"] = [{"BearerAuth": []}]

    public_paths = [
        "/auth/token",
        "/docs",
        "/openapi.json"
    ]
    
    paths_to_modify = openapi_schema.get("paths", {})
    for path, methods in paths_to_modify.items():
        if path in public_paths:
            for method in methods:
                methods[method]["security"] = []

    app.openapi_schema = openapi_schema
    return app.openapi_schema