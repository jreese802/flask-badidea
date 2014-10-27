# web midterm?
from Flask import Flask, render_template
from Flask.ext.bootstrap import Bootstrap
from Flask.ext.moment import Moment
from werkzeug import secure_filename

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpg','png','bmp','jpeg','gif'])

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
  return render_template('home.html')

@app.route('/upload')
def upload():
  return render_template('upload.html')

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
  app.run(debug=True)
