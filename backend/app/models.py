from app import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80),nullable=False)
    email = db.Column(db.String(120),unique=True,nullable = False)
    password = db.Column(db.String(255),nullable=True)
    role = db.Column(db.String(20),default="user")
    provider = db.Column(db.String(20),default="local")
    dob = db.Column(db.Date,nullable=True)
    gender = db.Column(db.String(20),nullable=True)
    def __repr__(self):
        return f"User {self.username}"


