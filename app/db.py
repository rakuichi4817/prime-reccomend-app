# pylint: disable=no-member
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemyのインスタンス化
app_db = SQLAlchemy()


def init_db(app):
    """DBの初期化

    Args:
        app (Flaskクラス): Flaskインスタンス
    """
    app_db.init_app(app)


def set_seed_emotion():
    from app.models import EmotionTable
    seed_emotions = [
        {"id": 0, "emotion": "感動", "file_name": "cry.png"},
        {"id": 1, "emotion": "楽しい", "file_name": "laugh.png"},
        {"id": 2, "emotion": "尊い・好き", "file_name": "love.png"},
        {"id": 3, "emotion": "謎", "file_name": "question.png"},
        {"id": 4, "emotion": "怖い", "file_name": "shock.png"},
        {"id": 5, "emotion": "眠い", "file_name": "sleep.png"},
        {"id": 6, "emotion": "ハラハラ", "file_name": "surprise.png"},
        {"id": 7, "emotion": "考える", "file_name": "think.png"},

        ]
    for seed_emotion in seed_emotions:
        check_emotion = EmotionTable.query.filter_by(
            id=seed_emotion["id"]).first()
        if not check_emotion:
            emotion = EmotionTable(
                id=seed_emotion["id"],
                emotion=seed_emotion["emotion"],
                file_name=seed_emotion["file_name"]
            )
            app_db.session.add(emotion)
            app_db.session.commit()
