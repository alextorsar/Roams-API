from database.database import engine, Base
from models.user import User

Base.metadata.create_all(bind=engine)