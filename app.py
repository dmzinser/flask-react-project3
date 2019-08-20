from flask import flask, g
from flask_cors import CORS
from flask_login import LoginManager
import models

# IMPORT BLUEPRINTS HERE

DEBUG = True
Port = 8000

login_manager = LoginManager()

app = Flask(__name__, static_url_path="", static_folder="static")

app.secret_key = 'REYKJAVIKING STRING'

login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
  try:
    return models.User.get(models.User.id == userid)
  except models.DoesNotExist:
    return None

# SET UP CORS FOR EACH API HERE

# SET UP THE BLUEPRINT FOR EACH API HERE

@app.before_request
def before_request():
  g.db = models.DATABASE
  g.db.connect()

@app.after_request
def after_request(response):
  g.db.close()
  return response

@app.route('/')
def index():
  return 'Hola!'
if __name__ == '__main__':
  models.initialize()
  app.run(debug=DEBUG, port=PORT)