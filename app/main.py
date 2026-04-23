from app.db.db import engine, Base
import models

# crea todas las tablas
Base.metadata.create_all(bind=engine)