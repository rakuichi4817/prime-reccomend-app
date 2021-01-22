from flask import Blueprint, render_template
from flask_login import login_required

app = Blueprint("general", __name__)


@app.route('/')
def index():
    """トップページ用

    Returns:
        index.htmlへのrender
    """
    return render_template("index.html", title="TOP", name="vissel")
