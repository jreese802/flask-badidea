"""
A simple website that allows the uploading and browsing of images.
Most of what needs to be written for a comments system has been 
written but has not yet been implemented due to a lack of time.

I relied heavily on the O'Reilly book *Flask Web Development*
during the creation of this website. I also utilized the 
"Flask Mega-Tutorial" by Miguel Grinburg for some clarification
about SQLAlchemy. Google and Stack Exchange were indispensible
tools as well. I would not have been able to solve my million 
little problems if it wasn't for other people making the same 
mistakes I made.

I definitely don't think that I'm done with this website. I
have a lot of work that could be done and a lot more I want
to explore. To start, I want to implement a basic comment 
system, fix the 
"""

import os
import datetime
from flask import Flask, render_template, request, redirect, url_for, \
                  send_from_directory, g
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import secure_filename
from flask.ext.wtf import Form
from wtforms import TextAreaField, SubmitField
from wtforms.validators import Required

# Sets the working path to be where the program is launched.
basedir = os.path.abspath(os.path.dirname(__file__))

# Creates an instance of the flask app
app = Flask(__name__)

# Sets where the uploads go and what file extensions may be uploaded
app.config['UPLOAD_FOLDER'] = 'static/upload/'
app.config['ALLOWED_EXTENSIONS'] = set(['jpg','png','bmp','jpeg','gif'])

# Points to the sql database
app.config['SQLALCHEMY_DATABASE_URI'] =\
'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# WTForms secret key for validation agains XSS attacks
app.config['SECRET_KEY'] = "The Night's Plutonian Shore"

# Create more instanses of things
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

# The database creation code
class CommentForm(Form):
  comment = TextAreaField('Comment', validators=[Required()])
  submit = SubmitField('Submit')

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

# Creates the database if it's gone
db.create_all()

# Used to verify that uploaded files have okay extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
  return render_template('home.html')

@app.route('/upload')
def upload_page():
  return render_template('upload.html')

# Redirects for extra slash
@app.route('/upload/')
def upload_slash():
  return redirect(url_for('upload_page'))

# This is the function that gets called after an image is uploaded
# It gives it a safe name, saves it, adds it to the database, then
# returns the page for the image.
@app.route('/images')
def process_image():
  file = request.files['file']
  if file and allowed_file(file.filename):
    filename = secure_filename(file.filename)
    # make jpegs into jpgs
    if file.filename[-4:] == 'jpeg':
      file.filename = filename[:-4] + '.jpg'
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    image = Image(filename=filename, date=date,)
    db.session.add(image)
    db.session.commit()
    return redirect(url_for('uploaded_file', filename=filename))
  else:
    render_template('error.html')

@app.route('/images/<filename>', methods=['GET', 'POST'])
def uploaded_file(filename):
  # This bit runs if the page receives a post
  # It stores the comment in the database
  if request.method == 'POST':
    text = request.form['comment']
    if text == '':
      return render_template('500.html')
    else:
      date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      image = (db.session.query(Image)
                .filter(Image.image_filename == filename).first())
      comment = Comment(content=text, date=date, image_id=image.image_id)
      db.session.add(comment)
      db.session.commit()
  # This bit renders the page. If the page gets a post, this runs after.
  comment_form = CommentForm()
  image = (db.session.query(Image)
            .filter(Image.image_filename == filename).first())
  this_url = '/images/{}'.format(image.image_filename)
  comments =  (db.session.query(Image.comments)
                .filter(Image.image_filename == filename).all())
  # This is here to cause an error and launch the debugger.
  # 1/0
  return  render_template('filepage.html', image=image, comments=comments,
                            comment_form=comment_form, this_url=this_url)

@app.route('/browse')
def browse():
  image_list = db.session.query(Image).all()
  return render_template('browse.html', image_list=image_list)

@app.route('/browse/<page_number>')
def browse_at_page(page_number):
  return render_template('browse.html')

@app.route('/comments/<filename>')
def comments(filename):
  comment_list = db.session.query(Comment).all()
  return render_template('comments.html', comment_list=comment_list)

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404
  
@app.errorhandler(500)
def internal_server_error(e):
  return render_template('500.html'), 500

# The flask server runs on port 80
if __name__ == "__main__":
  app.run(port=int('80'),
          debug=True)

