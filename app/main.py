from app.db.db import engine, Base

import app.models.expediente
import app.models.parte
import app.models.actuacion
import app.models.documento
import app.models.plazo
import app.models.estado
import app.models.regla

Base.metadata.create_all(bind=engine)

print("✅ Base de datos creada")