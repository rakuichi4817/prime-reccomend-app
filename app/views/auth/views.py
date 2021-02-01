# pylint: disable=no-member
from datetime import datetime

from flask import (
    Blueprint, flash, render_template, url_for, request, redirect, session
)
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash

from app import login_manager
from app.db import app_db
from app.models import User, UserTable

app = Blueprint("auth", __name__)

# セッションログインユーザの呼び出し


@login_manager.user_loader
def load_user(user_id):
    
    try:
        login_user = UserTable.query.filter_by(id=user_id).first()
        return User(user_id, login_user.name)
    except:
        return


@app.route('/login', methods=("GET", "POST"))
def login():
    """ログイン処理

    Returns:
        getでアクセス時はログイン画面、postのときはトップ画面へ
    """
    # ポストでリクエストされたらログイン処理
    if request.method == "POST":
        # リクエストデータの取得
        user_id = request.form["id"]
        password = request.form["password"]

        error_message = None
        # DBからIDでレコード取得
        check_user = UserTable.query.filter_by(id=user_id).first()
        if not check_user:
            error_message = "登録されていないIDです。"
        elif not check_password_hash(check_user.password, password):
            error_message = "パスワードが一致しません。"

        # 問題なければログイン
        if error_message is None:
            user = User(user_id, check_user.name)
            login_user(user)
            return redirect("/")
        # 問題があった際はメッセージ表示
        flash(error_message)
        
    return render_template("auth/login.html", title="login")

# アカウント作成
@app.route("/register", methods=("GET", "POST"))
def register():
    """新規登録処理

    Returns:
        getでアクセス時は新規登録画面、postのときはログイン画面へ
    """
    # ポストでリクエストされたら新規登録処理
    if request.method == "POST":

        error_message = None
        # リクエストデータの取得
        password = request.form["password"]
        check_password = request.form["checkPassword"]
        user_id = request.form["id"]
        name = request.form["name"]
        sex = request.form["sex"]
        birthday = f"{request.form['birthyear']}-{request.form['birthmonth']}-{request.form['birthday']}"

        # 受け取った値の処理
        if not user_id:
            error_message = "IDは必須です。"
        elif not password:
            error_message = "パスワードは必須です。"
        elif not name:
            error_message = "名前は必須です。"
        elif not sex:
            error_message = "性別は必須です。"
        elif not (request.form['birthyear'] and request.form['birthmonth'] and request.form['birthday']):
            error_message = "誕生日は必須です。"
        elif check_password != password:
            error_message = "パスワードが一致しません。"
        elif UserTable.query.filter_by(id=user_id).first() is not None:
            error_message = f"ID「{user_id}」はすでに利用されています。"

        # 全て問題なければDBにアカウント追加
        if error_message is None:
            # ハッシュ化
            hash_pass = generate_password_hash(password)
            birthday = datetime.strptime(birthday, r"%Y-%m-%d")
            regist_user = UserTable(
                id=user_id, password=hash_pass, name=name, sex=sex, birthday=birthday)
            app_db.session.add(regist_user)
            app_db.session.commit()

            return redirect(url_for("auth.login"))

        flash(error_message)

    return render_template("auth/register.html", title="register")


# ログアウト
@app.route("/logout")
@login_required
def logout():
    """ログアウト処理

    Returns:
        ログイン画面へ
    """
    logout_user()
    return redirect("/")
