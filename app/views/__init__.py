from importlib import import_module

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
