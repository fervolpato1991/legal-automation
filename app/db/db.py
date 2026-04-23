from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# conexión a la base
DATABASE_URL = "sqlite:///legal_system.db"

engine = create_engine(DATABASE_URL, echo=True)

# sesión (para interactuar con la DB)
SessionLocal = sessionmaker(bind=engine)

# clase base para modelos
Base = declarative_base()