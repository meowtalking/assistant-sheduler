from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#SQLALCHEMY_DATABASE_URL = "mysql://root:meowmeow@mysql:3306/assistantsheduler"

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://assistant_user:meowing@mysql:3306/assistantsheduler"


engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"host": "localhost"})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()