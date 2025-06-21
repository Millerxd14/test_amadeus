# app/middlewares/rol_validator.py

import json
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt, JWTError
from app.config import settings
ACL = {
    "student": {
        "/class-schedules": ["GET", "POST"], 
        "/teacher": ["GET"]# Listar y crear clases
    },
    "teacher": {
        "/student": ["ALL"],             # Todo el CRUD de estudiantes
        "/teacher": ["POST"],            # Solo crear profesores
        "/class-schedules": ["ALL"],     # Todo el CRUD de clases
    }
}

class RoleValidatorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        public_paths = ["/auth/token", "/docs", "/openapi.json", "/"]
        if request.url.path in public_paths or request.url.path.startswith("/static"):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return JSONResponse(status_code=403, content={"detail": "Not authenticated"})

        try:
            scheme, token = auth_header.split()
            if scheme.lower() != "bearer":
                raise ValueError("Invalid scheme")
            
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_data_str = payload.get("sub")
            if not user_data_str:
                raise ValueError("Missing subject")
            
            user_data = json.loads(user_data_str)
            user_role = user_data.get("kind")

            if not user_role:
                return JSONResponse(status_code=403, content={"detail": "Role not found in token"})

        except (ValueError, JWTError, json.JSONDecodeError) as e:
            return JSONResponse(status_code=403, content={"detail": f"Invalid token for authorization: {e}"})

        # --- Lógica de Validación de Rol ---
        is_authorized = False
        if user_role in ACL:
            user_permissions = ACL[user_role]
            for path_prefix, allowed_methods in user_permissions.items():
                if request.url.path.startswith(path_prefix):
                    if "ALL" in allowed_methods or request.method in allowed_methods:
                        is_authorized = True
                        break
        
        if not is_authorized:
            return JSONResponse(
                status_code=403,
                content={"detail": f"Role '{user_role}' is not authorized to perform {request.method} on {request.url.path}"}
            )

        return await call_next(request)