from ...extensions import db

class Tasks(db.Model):
    __tablename__ = "Tasks"
    
    tid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String, nullable=True)
    date_n_time = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey("Users.uid") ,nullable=False)
        
    def __repr__(self):
        return f"<Tasks : {self.tid} , {self.title}>"
    
    def get_id(self):
        return self.tid