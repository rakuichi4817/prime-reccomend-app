from flask import Blueprint, render_template
from flask_login import login_required

from app.db import app_db
from app.models import ReviewTable

app = Blueprint("general", __name__)


@app.route('/')
def index():
    """トップページ用

    Returns:
        index.htmlへのrender
    """
    # レビュー一覧の取得
    all_reviews = ReviewTable.query.limit(10)
    return render_template("index.html", title="TOP", all_reviews=all_reviews)
