import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

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
  image_filename = db.Column(db.String, index=True)
  image_date = db.Column(db.String, index=True)
  comments = db.relationship('Comment', backref='comments')

  def __init__(self, filename, date, comments=None):
    self.image_filename = filename
    self.image_date = date
    self.image_comments = comments

  def __repr__(self):
    return '<Image {}>'.format(self.image_id)

class Comment(db.Model):
  __tablename__ = 'Comment'
  comment_id = db.Column(db.Integer, primary_key=True)
  comment_content = db.Column(db.UnicodeText)
  comment_date = db.Column(db.String, index=True)
  image_id = db.Column(db.Integer, db.ForeignKey('Image.image_id'))  

  def __init__(self, content, date, image_id):
    self.comment_content = content
    self.comment_date = date
    self.image_id = image_id

  def __repr__(self):
    return '<Comment {}>'.format(self.comment_id)

# db.drop_all()
# db.create_all()

# image = Image('1234.jpg','1234')
# image2 = Image('2345.png','2345')
# image3 = Image('9765.jpg','9876')
# db.session.add_all([image,image2,image3])

# comment = Comment('This sucks.', '1235', 1)
# comment2 = Comment('Totally.', '1236',1)
# comment3 = Comment('Me IRL.', '1333', 3)
# db.session.add_all([comment, comment2, comment3])

# db.session.commit()