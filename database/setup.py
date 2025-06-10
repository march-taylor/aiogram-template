from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True)
	user_id = Column(BigInteger, unique=True)
	language = Column(String(2), default="en")
	added_at = Column(Integer, server_default=func.strftime('%s', 'now'))