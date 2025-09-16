from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router
from app.core.db import init_db


# -----------------------------
# Lifespan handler
# -----------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Se ejecuta al iniciar la app
    init_db()
    print("Tablas creadas o actualizadas según los modelos")
    yield
    # Aquí podrías poner lógica de cierre (shutdown)
    print("Aplicación cerrando...")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000", "https://rework-rate.scisa.com.mx"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
