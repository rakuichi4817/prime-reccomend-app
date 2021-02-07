from importlib import import_module
from flask import Markup, Blueprint


# Brueprintで登録するモジュール
modules = ["auth", "general", "review"]


def init_app(app):
    """Blurprintの登録

    Args:
        app (Flask()): Flaskクラスのインスタンス
    Return:
        app (Flask()): Brueprintの設定済みFlaskクラスのインスタンス
    """
    for module in modules:
        bp_views = import_module(f"app.views.{module}.views")
        app.register_blueprint(bp_views.app)
        

    @app.template_filter("cr")
    def cr(arg):
        return Markup(arg.replace("\r\n", "<br>"))
