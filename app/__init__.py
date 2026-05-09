"""Flask application factory and extensions."""
from __future__ import annotations

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO

from config import Config

# Initialize Flask extensions (bound to app in create_app)
db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO(cors_allowed_origins="*")


def create_app() -> Flask:
    """Create and configure the Flask app instance."""
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(Config)

    # Attach extensions to the app
    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app, cors_allowed_origins="*", manage_session=False)

    # Import models so Flask-Migrate can discover them
    from app import models  # noqa: F401

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.task import task_bp
    from app.routes.analytics import analytics_bp
    from app.routes.websocket import register_socketio_events

    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(analytics_bp)

    # Register WebSocket events
    register_socketio_events(socketio)

    return app
