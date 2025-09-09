from flask_login import UserMixin
from ...extensions import db

class User(UserMixin, db.Model):
    __tablename__ = "Users"
    
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    tasks = db.relationship("Tasks", backref="author", lazy=True)
    
    def __repr__(self):
        return f"f<User: {self.uid}>"
    
    def get_id(self):
        return self.uid