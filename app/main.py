from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from pathlib import Path
from app.routers import class_schedule, student, teacher, auth
from app.database.connection import engine, Base
from app.models import student as student_model , teacher as teacher_model, class_schedule as class_schedule_model
from app.middlewares import jwt_validator, rol_validator
from app.utilities import openapi


print("Creando tablas en la base de datos...")
Base.metadata.create_all(bind=engine)
print("Tablas creadas.")

class Server:
    def __init__(self, host: str = "0.0.0.0", port: int = 5660):
        self.app = FastAPI()
        self.host = host
        self.port = port
        self._configure_cors()
        self._create_static_directories()
        self._mount_static_files()
        self._include_routers()
        self._setup_root_route()
        self._create_custom_openapi()
    def _configure_cors(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self.app.add_middleware(jwt_validator.JWTValidatorMiddleware)
        self.app.add_middleware(rol_validator.RoleValidatorMiddleware)

    def _create_static_directories(self):
        self.static_dir = Path("static")
        self.static_dir.mkdir(parents=True, exist_ok=True)
        self.video_storage_dir = self.static_dir / "videos"
        self.video_storage_dir.mkdir(parents=True, exist_ok=True)

    def _create_custom_openapi(self):
        self.app.openapi = lambda: openapi.create_custom_openapi(self.app)
    def _mount_static_files(self):
        self.app.mount("/static", StaticFiles(directory=self.static_dir), name="static")

    def _include_routers(self):
        self.app.include_router(auth.router, prefix="/auth", tags=["Authentication"],)  
        self.app.include_router(student.router, prefix="/students", tags=["Students"],)  
        self.app.include_router(teacher.router, prefix="/teachers", tags=["Teachers"],)  
        self.app.include_router(class_schedule.router, prefix="/class-schedules", tags=["Class Schedules"],) 

    def _setup_root_route(self):
        @self.app.get("/")
        async def root():
            return {"message": "pong"}

    def run(self):
        uvicorn.run(self.app, host=self.host, port=self.port, reload=True)

server_instance = Server()
app = server_instance.app

if __name__ == "__main__":
    print(f"Iniciando servidor directamente desde __main__ en http://{server_instance.host}:{server_instance.port}")
    server_instance.run()