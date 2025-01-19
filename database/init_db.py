from database.database import engine, Base
from models.user import User
from models.conversation import Conversation
from models.message import Message

Base.metadata.create_all(bind=engine)