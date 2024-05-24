import uuid
from .database import Base
from sqlalchemy import UUID, Boolean, Column, ForeignKey, Integer, String


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True, index=True)
    # id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
    phone_number = Column(String) 



class Todos(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key = True, index = True)
    # id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean,default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))


