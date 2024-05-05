from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    # Initialize database
    db.init_app(app)

    from app import models

    # Create database tables
    with app.app_context():
        db.create_all()

    # Register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app
