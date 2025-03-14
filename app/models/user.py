from app import db



class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)  
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default="user", nullable=False)

    def __init__(self, username, password, role="user"):
        self.username = username
        self.password = password
        self.role = role

    def __repr__(self):
        return f'<User [self.username]>'
    

    
    
    
