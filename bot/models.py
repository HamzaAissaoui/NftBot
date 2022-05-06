from datetime import datetime
from bot import db


class User():

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post():

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"