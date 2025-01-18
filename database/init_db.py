from database.database import engine, Base
from models.user import User
from models.conversation import Conversation

Base.metadata.create_all(bind=engine)