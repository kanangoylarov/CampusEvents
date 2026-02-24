from flask import Flask
from flask_login import LoginManager
from db import db, User
from user import user_bp
from event import event_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app) # Connect the database object to this app
app.register_blueprint(user_bp)
app.register_blueprint(event_bp)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    # This tells Flask-Login how to load a user from the ID stored in their session
    return User.query.get(int(user_id))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)