from flask import Flask
from flask_login import LoginManager
from db import db, User
from user import user_bp
from event import event_bp
from room import room_bp
from organization import organization_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

# burda registerler edilecek
app.register_blueprint(user_bp)
app.register_blueprint(event_bp)
app.register_blueprint(room_bp)
app.register_blueprint(organization_bp)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)