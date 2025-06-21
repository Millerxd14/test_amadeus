from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt, JWTError
from app.config import settings

class JWTValidatorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Define las rutas públicas que no necesitan token
        public_paths = [
            "/auth/token",
            "/docs",
            "/openapi.json",
            "/ping",
        ]

        # Si la ruta es pública o es una ruta estática, la dejamos pasar sin validar
        if request.url.path in public_paths or request.url.path.startswith('/static'):
            response = await call_next(request)
            return response

        # Para el resto de rutas, buscamos el token
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return JSONResponse(
                status_code=403,
                content={"detail": "Not authenticated"}
            )

        # Extraemos el token del header "Bearer <token>"
        try:
            scheme, token = auth_header.split()
            if scheme.lower() != "bearer":
                raise ValueError("Invalid authentication scheme")
        except ValueError:
            return JSONResponse(
                status_code=403,
                content={"detail": "Invalid authentication header"}
            )

        try:
            # Verificamos la firma y la expiración del token
            print(f"Validating token: {token}")
            jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
        except JWTError as e:
            # Si el token es inválido, devolvemos un error
            return JSONResponse(
                status_code=403,
                content={"detail": f"Invalid token: {e}"}
            )

        # Si el token es válido, la petición continúa su curso
        response = await call_next(request)
        return response