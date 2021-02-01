import re

re_url = re.compile(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+')

def pick_url(string):
    """テキストからURLを抽出する

    Args:
        string (str): URL抽出の対象文書

    Returns:
        str or None: テキスト中のURLか、存在しない場合はNoneを返す
    """
    result = re_url.search(string)
    if result:
        return result.group()
    return result
