# pylint: disable=no-member
from datetime import datetime

from flask_login import UserMixin

from app.db import app_db


# User情報管理クラス
class User(UserMixin):
    """ログイン管理用のUserクラス

    Args:
        UserMixin (flask_login.UserMixin): 継承元クラス
    """

    def __init__(self, user_id, name):
        self.id = user_id
        self.name = name


class UserTable(app_db.Model):
    """userテーブルとの接続用クラス

    Args:
        id (string, optional): ユーザID. Defaults to None.
        password (string, optional): パスワード. Defaults to None.
        name (string, optional): ユーザ名. Defaults to None.
        sex (string, optional): 性別. Defaults to None.
        birthday (string, optional): 誕生日（ex:1995-09-08）. Defaults to None.

    """
    __tablename__ = "users"
    id = app_db.Column(app_db.String, primary_key=True)
    password = app_db.Column(app_db.String, nullable=False)
    name = app_db.Column(app_db.String, nullable=False)
    sex = app_db.Column(app_db.String, nullable=False)
    birthday = app_db.Column(app_db.Date, nullable=False)

    def __init__(self, id=None, password=None, name=None, sex=None, birthday=None):

        self.id = id
        self.password = password
        self.name = name
        self.sex = sex
        self.birthday = birthday

    def __repr__(self):
        return f"<UserTable {self.name}>"


class ReviewTable(app_db.Model):
    """reviewsテーブルと接続するためのクラス

    Args:
        割愛
    """

    __tablename__ = "reviews"
    review_id = app_db.Column(app_db.Integer, primary_key=True)
    user_id = app_db.Column(app_db.String, nullable=False)
    review_title = app_db.Column(app_db.String, nullable=False)
    video_title = app_db.Column(app_db.String, nullable=False)
    emotion_id1 = app_db.Column(app_db.Integer)
    emotion_id2 = app_db.Column(app_db.Integer)
    emotion_id3 = app_db.Column(app_db.Integer)
    url = app_db.Column(app_db.String, nullable=False)
    star = app_db.Column(app_db.Integer, nullable=False)
    target_person = app_db.Column(app_db.String)
    review_comment = app_db.Column(app_db.String)
    created_at = app_db.Column(
        app_db.DateTime, nullable=False, default=datetime.now)

    def __init__(self, **kwargs):
        self.user_id = kwargs.get("user_id")
        self.review_title = kwargs.get("review_title")
        self.video_title = kwargs.get("video_title")
        self.emotion_id1 = kwargs.get("emotion_id1")
        self.emotion_id2 = kwargs.get("emotion_id2")
        self.emotion_id3 = kwargs.get("emotion_id3")
        self.url = kwargs.get("url")
        self.star = kwargs.get("star")
        self.target_person = kwargs.get("target_person")
        self.review_comment = kwargs.get("review_comment")

    def __repr__(self):
        return f"<ReviewTable {self.review_id}>"


class EmotionTable(app_db.Model):
    """emotionsテーブルと接続するためのクラス

    Args:
        割愛
    """

    __tablename__ = "emotions"

    id = app_db.Column(app_db.Integer, primary_key=True)
    emotion = app_db.Column(app_db.String, nullable=False)
    file_name = app_db.Column(app_db.String, nullable=False)

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.emotion = kwargs.get("emotion")
        self.file_name = kwargs.get("file_name")

    def __repr__(self):
        return f"<EmotionTable {self.emotion}>"
