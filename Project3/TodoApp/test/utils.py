from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine,text
from sqlalchemy.orm import sessionmaker
from ..database import Base
from ..main import app
from fastapi import status
from ..routers.todos import get_db, get_current_user
import pytest
from ..models import Todos, Users
from ..routers.auth import bcrypt_context

SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {'username': 'rohanbanda', 'id':1, 'user_role': 'admin'}

client = TestClient(app)

@pytest.fixture
def test_todo():
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos"))
        connection.commit()

    todo = Todos(
        title = "Learn to code!",
        description="Need to learn everyday!",
        priority=5,
        complete = False, 
        owner_id = 1,
        # id = 1,
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    db.close()
    # with engine.connect() as connection:
    #     connection.execute(text("DELETE FROM todos"))
    #     connection.commit()

@pytest.fixture
def test_user():
    user = Users(
        username = "rohanbanda",
        email = "mymail@gmail.com",
        first_name = "Rohan",
        last_name = "Banda",
        hashed_password = bcrypt_context.hash("testpassword"),
        role = "admin",
        phone_number = "1234567890",
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()
