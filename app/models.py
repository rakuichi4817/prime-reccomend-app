# pylint: disable=no-member
from flask_login import UserMixin
from app.db import app_db


# User情報管理クラス
class User(UserMixin):
    """ログイン管理用のUserクラス

    Args:
        UserMixin (flask_login.UserMixin): 継承元クラス
    """

    def __init__(self, user_id):
        self.id = user_id


class UserTable(app_db.Model):
    """SQLiteとの接続用クラス

    Args:
        app_db (SQLAlchemy()): SQLAlchemyインスタンス

    """
    __tablename__ = 'users'
    id = app_db.Column(app_db.String, primary_key=True)
    password = app_db.Column(app_db.String)

    def __init__(self, id=None, password=None):
        self.id = id
        self.password = password

    def __repr__(self):
        return '<UserTable %r>' % (self.id)
