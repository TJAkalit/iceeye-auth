from sqlalchemy.ext.asyncio import (
    AsyncSession, create_async_engine,
)
from sqlalchemy.orm import sessionmaker
from config import db

url = "postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}".format(
    HOST=db.HOST,
    PORT=db.PORT,
    NAME=db.DBNAME,
    USER=db.USER,
    PASSWORD=db.PASSWORD,
)
engine = create_async_engine(url)
Session = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)
