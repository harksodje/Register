from datetime import datetime
from Register import app, db
#db = SQLAlchemy(app)

class user_data (db.Model):
    __table_name = 'User table'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    admin = db.Column(db.Boolean, nullable = False, default  = False)
    password = db.Column(db.String(60), nullable = False)
    #posts = db.relationship('Post', backref ='author', lazy = True)
   
    def __repr__(self):
        return f"user_data('{self.username}','{self.email}', )"