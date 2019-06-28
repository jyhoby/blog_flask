from datetime import datetime
from App.exts import db



class BlogType(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    typename = db.Column(db.String(20))
    blogs = db.relationship("Blog",backref="my_blogtype",lazy=True)


class Blog(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    imgurl = db.Column(db.String(250),default='/static/home/images/1.jpg')
    blog_type = db.Column(db.Integer,db.ForeignKey(BlogType.id))
    create_time = db.Column(db.DateTime,default=datetime.now)

class User(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(20),unique=True)
    password = db.Column(db.String(20))



