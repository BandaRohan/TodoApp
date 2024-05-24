from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'

# SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:rhnrxn@127.0.0.1:3306/todoapplicationdatabase'

# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:rhnrxn@localhost/TodoApplicationDatabase'

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread':False})

# engine = create_engine(SQLALCHEMY_DATABASE_URL)
                       
SessionLocal = sessionmaker(autocommit = False, autoflush=False,bind = engine)

Base = declarative_base()

