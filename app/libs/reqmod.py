import uuid

from flask import session

def set_token(token_name):
    """セッションに指定したkey（token_name）でトークン発行

    Args:
        token_name (str): セッションに保存する際のkey

    Returns:
        str: 発行したトークン
    """
    submit_token = str(uuid.uuid4())
    session[token_name] = submit_token
    
    return submit_token

def check_token(token_name, request_data):
    """セッションに保存されているトークンとリクエストにあるトークンを比較

    Args:
        token_name (str): 比較したいトークン名
        request_data (dict): 比較したいトークンを含む辞書型のデータ

    Returns:
        boolean: トークンが存在かつ一致の場合のみTrueとなり、それ以外はFalse
    """
    session_token = session.pop(token_name, None)
    request_token = request_data.get(token_name)
    
    print(session_token)
    print(request_token)
    
    if not request_token:
        return False
    if not session_token:
        return False
    return session_token == request_token
