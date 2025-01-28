from sqlalchemy import Column, Integer, String
from database import Base

class Blog(Base):
    __tablename__ = 'blog'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    title = Column(String(255))
    no_of_pages = Column(Integer, nullable=True, default=0)
    description = Column(String(255))