# pylint: disable=no-member
import uuid

from flask import Blueprint, render_template, url_for, request, redirect, session, flash
from flask_login import login_required, current_user

from app.db import app_db
from app.common_function import set_token, check_token
from app.models import ReviewTable, EmotionTable
from app.libs import nldpp

app = Blueprint("review", __name__, url_prefix="/review")

# 投稿に関してトークンで2重送信を防止
token_name = "post_token"


# 新規投稿機能
@app.route("/new-post", methods=("GET", "POST"))
@login_required
def post_review():
    """レビュー投稿に関するリクエスト処理を制御する

    Note:
        投稿→確認、確認→投稿、確認→確定の3つの流れを制御
    """
    # 感情リストの取得
    emotions = EmotionTable.query.all()
    if request.method == "POST":
        submit_type = request.form.get("submit")
        if submit_type == "fix":
            # 確認画面→投稿画面
            post_data = _get_post_review(request, page="confirm")
            return render_template("review/post-review.html", title="Post Review",
                                   emotions=emotions, post_data=post_data)
        elif submit_type == "ok":
            # 確定して投稿
            post_data = _get_post_review(request, page="confirm")

            # トークンチェック
            if check_token(token_name, post_data):
                print("aaa")
                post_data["user_id"] = current_user.id
                add_review = ReviewTable(**post_data)
                app_db.session.add(add_review)
                app_db.session.commit()
                return redirect("/")
            else:
                # 失敗時はメッセージとともに新規投稿画面へ
                post_token = set_token(token_name)
                flash("問題が発生したので初めから登録して下さい。")
                return render_template("review/post-review.html", title="Post Review",
                                       emotions=emotions, post_token=post_token)
        else:
            # 確認画面へ
            post_data = _get_post_review(request, page="post")
            return render_template("review/confirm-review.html", title="Confirm Post Review",
                                   post_data=post_data, emotions=emotions)

    post_token = set_token(token_name)
    return render_template("review/post-review.html", title="Post Review",
                           emotions=emotions, post_token=post_token)


def _get_3emotion_ids(req_emotion_ids):
    """感情に関するリクエストデータを整理して、指定の数の感情IDを辞書型で返す

    Args:
        req_emotion_ids (list): セレクトボックスで複数選択されたIDリスト

    Returns:
        dict: 辞書型でemotion_id1のような形でkeyを持つ
    """
    num = 3
    base_col_name = "emotion_id"
    emotion_ids = {f"{base_col_name}{i}": None for i in range(1, num+1)}
    for i, req_emotion in enumerate(req_emotion_ids, 1):
        if i > num:
            break
        emotion_ids[f"{base_col_name}{i}"] = int(req_emotion)
    return emotion_ids


def _get_post_review(request, page="post"):
    """レビュー投稿に関するリクエストデータを受け取って辞書型にして返す

    Args:
        request (flask.request): HTMLリクエストのリクエストデータ
        page (str, optional): 投稿ページか確認画面か、どちらからのリクエストか判断. Defaults to "post".

    Returns:
        Dict {key:value}: 項目名をkeyリクエスト内容がValueとなっている辞書型
    """

    # リクエストデータの取得
    post_data = {}

    post_data["review_title"] = request.form.get("review_title")
    post_data["video_title"] = request.form.get("video_title")
    post_data["url"] = nldpp.pick_url(request.form.get("url"))
    post_data["star"] = int(request.form.get("star"))
    post_data["target_person"] = request.form.get("target_person")
    post_data["review_comment"] = request.form.get("review_comment")
    post_data[token_name] = request.form.get(token_name)

    if page == "post":
        # 投稿画面→確認画面
        req_emotion_ids = request.form.getlist("emotion")
        emotion_ids = _get_3emotion_ids(req_emotion_ids)
        post_data["emotion_id1"] = emotion_ids["emotion_id1"]
        post_data["emotion_id2"] = emotion_ids["emotion_id2"]
        post_data["emotion_id3"] = emotion_ids["emotion_id3"]
    elif page == "confirm":
        # 確認画面→投稿画面
        post_data["emotion_id1"] = request.form.get("emotion_id1")
        post_data["emotion_id2"] = request.form.get("emotion_id2")
        post_data["emotion_id3"] = request.form.get("emotion_id3")

    return post_data
