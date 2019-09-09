from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

# protect against modyfing cookies, cross-site requests and other attacks
app.config['SECRET_KEY'] = '68e668617fc603ba3612a286618e5453'
# specify location for the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
# specify file extensions supported by the back-end
app.config['ALLOWED_EXTENSIONS'] = ('.spold')
# set up development mode
app.config['ENV'] = 'development'

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
login_manager.init_app(app)

from web.models.user import User
@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))


# blueprint for non-auth parts of app
from web.controllers.main import main
app.register_blueprint(main)

# blueprint for auth routes in our app
from web.controllers.auth import auth
app.register_blueprint(auth)
