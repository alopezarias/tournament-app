# backend/app/core/config.py
import os
from dotenv import load_dotenv

load_dotenv()  # Carga variables desde un archivo .env si existe

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:secret@localhost:5432/tournament")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "tu_secreto_super_seguro")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 días

settings = Settings()
