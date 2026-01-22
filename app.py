from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
import os
import logging

# Define base for models
class Base(DeclarativeBase):
    pass

# Initialize extensions
db = SQLAlchemy(model_class=Base)
migrate = Migrate()

# Create app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "fallback-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure database
db_url = os.getenv("DATABASE_URL")

# Fix postgres:// vs postgresql:// for SQLAlchemy
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

# Force SSL for Render PostgreSQL
if db_url and "sslmode" not in db_url:
    if "?" in db_url:
        db_url = db_url + "&sslmode=require"
    else:
        db_url = db_url + "?sslmode=require"

app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
logging.basicConfig(level=logging.DEBUG)

# Attach app to extensions
db.init_app(app)
migrate.init_app(app, db)

# Login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

# ✅ Import models
import models  # now SQLAlchemy knows about your tables
import routes

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
