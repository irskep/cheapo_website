from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import Engine
from sqlalchemy import event
from sqlalchemy.orm import deferred
from werkzeug.security import generate_password_hash, check_password_hash


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.close()


db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String, unique=True, nullable=False)

    # If you don't need these, feel free to delete and run the migration workflow, or
    # ignore them indefinitely.
    # Just remember: https://www.kalzumeus.com/2010/06/17/falsehoods-programmers-believe-about-names/
    name = deferred(db.Column(db.String, nullable=False, default=""))
    pronouns = deferred(db.Column(db.String, nullable=False, default=""))

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
