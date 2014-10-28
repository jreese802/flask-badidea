import os
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask

basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload/'
app.config['ALLOWED_EXTENSIONS'] = set(['jpg','png','bmp','jpeg','gif'])

app.config['SQLALCHEMY_DATABASE_URI'] =\
'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)

class Image(db.Model):
  __tablename__ = 'Image'
  image_id = db.Column(db.Integer, primary_key=True)
  image_date = db.Column(db.Integer, index=True)
  comments = db.relationship('Image', backref='Comment')

  def __repr__(self):
    return '<Image {}>'.format(self.image_id)

class Comment(db.Model):
  __tablename__ = 'Comment'
  comment_id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.UnicodeText)
  comment_date = db.Column(db.Integer, index=True)
  image_id = db.Column(db.Integer, db.ForeignKey('Image.image_id'))  

  def __repr(self):
    return '<Comment {}>'.format(self.comment_id)