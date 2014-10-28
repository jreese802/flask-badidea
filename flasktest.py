# web midterm?
import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, g
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import secure_filename


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
  image_name = db.Column(db.String, index=True, unique=True)
  image_date = db.Column(db.Integer, index=True)
  comments = db.relationship('Image', backref='comment', lazy='dynamic')

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


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def index():
  return render_template('home.html')

@app.route('/uploads/')
def upload_slash():
  return redirect(url_for('upload_page'))

@app.route('/upload', methods=['POST'])
def upload():
  file = request.files['file']
  if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      return redirect(url_for('uploaded_file', filename=filename))

@app.route('/uploads')
def upload_page():
  return render_template('upload.html')

@app.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/bootstrap/<name>')
def bootstraptest(name):
  return render_template('bootstraptest.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404
  
@app.errorhandler(500)
def internal_server_error(e):
  return render_template('500.html'), 500


if __name__ == "__main__":
  app.run(port=int('80'),
          debug=True)

