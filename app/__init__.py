# pylint: disable=no-member,unused-variable
import os

from flask import Flask, render_template
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "ログイン後に再度実行してください"

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    # sqlite保存場所
    sqlite_fpath = os.path.join(app.instance_path, "pra.sqlite")
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{sqlite_fpath}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        GENERATE_DIR=os.path.join("app", "static", "files"),
        WORDCLOUD_DIR=os.path.join("app", "static", "files", "wordcloud"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    for make_dir_path in [app.instance_path, app.config["GENERATE_DIR"], app.config["WORDCLOUD_DIR"]]:
        try:
            os.makedirs(make_dir_path)
        except OSError:
            pass
        
    # Login処理初期化
    login_manager.init_app(app)

    from. import db
    db.init_db(app)

    @app.before_first_request
    def create_table():
        db.app_db.create_all()
        db.set_seed_emotion()
        
    # Blueprint初期化
    from . import views
    views.init_app(app)

    return app
