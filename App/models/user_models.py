from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class GoogleUser(Base):
    __tablename__ = 'google_users'

    user_id = Column(Integer, primary_key=True)
    google_user_id = Column(String(1024), nullable=False, unique=True)
    name = Column(String(1024), nullable=False)
    email = Column(String(1024), nullable=False)
    picture = Column(String(1024), nullable=True)


class FacebookUser(Base):
    __tablename__ = 'facebook_users'

    user_id = Column(Integer, primary_key=True)
    fb_user_id = Column(String(1024), nullable=False, unique=True)
    name = Column(String(1024), nullable=False)
    email = Column(String(1024), nullable=True)
    gender = Column(String(1024), nullable=True)
    birth_day = Column(String(1024), nullable=True)
