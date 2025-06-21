from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from pathlib import Path

# Importar el router de video
from app.routers import class_schedule
from app.database.connection import engine, Base

# Crear la base de datos y las tablas
Base.metadata.create_all(bind=engine)

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

    def _configure_cors(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def _create_static_directories(self):
        self.static_dir = Path("static")
        self.static_dir.mkdir(parents=True, exist_ok=True)
        self.video_storage_dir = self.static_dir / "videos"
        self.video_storage_dir.mkdir(parents=True, exist_ok=True)


    def _mount_static_files(self):
        self.app.mount("/static", StaticFiles(directory=self.static_dir), name="static")

    def _include_routers(self):
        self.app.include_router(class_schedule.router, prefix="/classes", tags=["Classes"],) 


    def _setup_root_route(self):
        @self.app.get("/")
        async def root():
            return {"message": "Servidor FastAPI funcionando."}

    def run(self):
        uvicorn.run(self.app, host=self.host, port=self.port, reload=True)

server_instance = Server()
app = server_instance.app

if __name__ == "__main__":
    print(f"Iniciando servidor directamente desde __main__ en http://{server_instance.host}:{server_instance.port}")
    server_instance.run()