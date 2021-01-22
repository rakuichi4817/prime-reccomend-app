from flask_sqlalchemy import SQLAlchemy

# SQLAlchemyのインスタンス化
app_db = SQLAlchemy()


def init_db(app):
    """DBの初期化

    Args:
        app (Flaskクラス): Flaskインスタンス
    """
    app_db.init_app(app)
