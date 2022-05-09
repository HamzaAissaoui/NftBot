from datetime import datetime
from bot import db
from sqlalchemy.orm import relationship
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String

class Sneaker():

    __tablename__ = 'sneaker'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    fullname = Column(String)

    def __repr__(self):
       return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Post():

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"