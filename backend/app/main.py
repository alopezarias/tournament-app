# backend/app/main.py
from fastapi import FastAPI
from app.controllers.auth_controller import router as auth_router
# Puedes incluir otros routers, por ejemplo de teams, tournament, etc.

app = FastAPI(title="Torneo Futbolín API", version="1.0")

app.include_router(auth_router, prefix="/auth", tags=["auth"])

@app.get("/")
def root():
    return {"message": "Bienvenido a la API del Torneo Futbolín"}
