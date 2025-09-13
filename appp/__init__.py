from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from datetime import timedelta, datetime
from dotenv import load_dotenv
from pathlib import Path
import os

db = SQLAlchemy()

def create_app():
    env_path = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(dotenv_path=env_path)

    app = Flask(__name__)

    project_root = Path(__file__).resolve().parent.parent
    db_file_path= project_root / "data" / "avalanche.db"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_file_path.as_posix()}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SESSION_TYPE"] = "sqlalchemy"
    app.config["SESSION_SQLALCHEMY"] = db
    app.config["SESSION_SQLALCHEMY_TABLE"] = "sessions"
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=1)

    db.init_app(app)

    with app.app_context():
        db.create_all()
        try:
            deleted = db.session.execute(
                db.text("DELETE FROM sessions WHERE expiry < :now"),
                {"now": datetime.now()}
            )
            db.session.commit()
            print(f"Deleted {deleted.rowcount} expired sessions on startup")
        except Exception as e:
            db.session.rollback()
            print(f"Session cleanup failed: {e}")

    Session(app)  # Initialize sessions after tables are created

    from .routes import routes
    app.register_blueprint(routes)
    return app