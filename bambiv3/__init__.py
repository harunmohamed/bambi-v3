import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config['SECRET_KEY'] = '0a383bdacfada9ed7b9603837f78bb71'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
moment = Moment(app)
bootstrap = Bootstrap(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'bambichatter@gmail.com' #os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = '@bambichat' #os.environ.get('EMAIL_PASS')
mail = Mail(app)



from bambiv3 import routes, models
