# web midterm?
import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, g
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import secure_filename
import datetime


basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'upload/'
app.config['ALLOWED_EXTENSIONS'] = set(['jpg','png','bmp','jpeg','gif'])

app.config['SQLALCHEMY_DATABASE_URI'] =\
'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

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

db.create_all()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
  return render_template('home.html')




@app.route('/upload')
def upload_page():
  return render_template('upload.html')

@app.route('/upload/')
def upload_slash():
  return redirect(url_for('upload_page'))

@app.route('/images', methods=['POST'])
def process_image():
  file = request.files['file']
  if file and allowed_file(file.filename):
    filename = secure_filename(file.filename)
    #make jpegs into jpgs
    if file.filename[-4:] == 'jpeg':
      file.filename = filename[:-4] + '.jpg'
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    image = Image(filename=filename,
                  date=date,)
    db.session.add(image)
    db.session.commit()
    return redirect(url_for('uploaded_file', filename=filename))
  else:
    render_template('error.html')

@app.route('/images/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/browse')
def browse():
  image_list = db.session.query(Image).all()
  return render_template('browse.html', image_list=image_list)

@app.route('/browse/<page_number>')
def browse_at_page(page_number):
  image_list = db.session.query(Image).all()
  return render_template('browse.html', image_list=image_list)

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404
  
@app.errorhandler(500)
def internal_server_error(e):
  return render_template('500.html'), 500


if __name__ == "__main__":
  app.run(port=int('80'),
          debug=True)

