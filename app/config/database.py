from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from services.secret import get_secret

SQLALCHEMY_DATABASE_URL = "mysql://{user}:{password}@{host}:{port}/{db_name}".format(
    user=get_secret("DB_DEV_USER"),
    password=get_secret("DB_DEV_USER_PASSWORD"),
    host=get_secret("DB_HOST"),
    port=get_secret("DB_PORT"),
    db_name=get_secret("DB_NAME")
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, pool_pre_ping=True)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
