from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255), unique=True)
    password = Column(String(255))
    blog_details = relationship('Blog', back_populates='user_details')

class Blog(Base):
    __tablename__ = 'blog'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    title = Column(String(255))
    no_of_pages = Column(Integer, nullable=True, default=0)
    description = Column(String(255))
    user_id = Column(Integer, ForeignKey('user.id'))
    user_details = relationship('User', back_populates='blog_details')     