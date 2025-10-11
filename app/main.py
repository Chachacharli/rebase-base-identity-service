from contextlib import asynccontextmanager

# Import information of pyproject.toml
import toml
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

from app.api import api_router
from app.core.db import init_db

pyproject_data = toml.load("pyproject.toml")
__version__ = pyproject_data["tool"]["poetry"]["version"]
__name__ = pyproject_data["tool"]["poetry"]["name"]
__description__ = pyproject_data["tool"]["poetry"]["description"]


# -----------------------------
# Lifespan handler
# -----------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Se ejecuta al iniciar la app
    init_db()
    yield
    # Aquí podrías poner lógica de cierre (shutdown)
    print("Closing app...")


app = FastAPI(
    lifespan=lifespan, title=__name__, version=__version__, description=__description__
)

templates = Jinja2Templates(directory="app/templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
