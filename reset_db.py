from app.db.db import Base, engine
from app.models.documento import Documento
from app.models.expediente import Expediente

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)