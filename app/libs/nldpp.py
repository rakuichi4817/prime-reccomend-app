import re

from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import *
from janome.tokenfilter import *
from wordcloud import WordCloud

re_url = re.compile(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+')

# janome config
char_filters = [UnicodeNormalizeCharFilter()]
tokenizer = Tokenizer()
stop_poss_lst = ['記号', '助詞', "助動詞", "名詞,接尾",
                 "名詞,非自立", "動詞,非自立", "接頭詞", "副詞", "動詞,接尾", "副詞"]
token_filters = [POSStopFilter(stop_poss_lst)]
janalayzer = Analyzer(char_filters=char_filters, token_filters=token_filters)

# wordcloud config
wordcloud_setting = {
    "background_color": "white",
    "font_path": r"C:\Windows\Fonts\YUGOTHL.ttc",
    "width": 900,
    "height": 500,
    "prefer_horizontal": 1,
    "contour_width": 1,
    "contour_color": "black"
}


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


def get_feature_wkt(text, sep=" "):
    """必要な単語のみを残して分かちがき

    Args:
        text (str): 対象文書

    Returns:
        str: 特徴的な語を残してスペースで分かち書きされている文字列
    """
    return f"{sep}".join([token.base_form for token in janalayzer.analyze(text)])


def get_wordcloud_wkt(wkt_text, img_path):
    """ワードクラウドを分かち書きテキストより作成

    Args:
        wkt_text (str): ワードクラウド化する分かち書きされたテキスト
        img_path (str): 画像を保存するパス

    Returns:
        boolean: 作成が成功したかどうか
    """

    try:
        wd = WordCloud(**wordcloud_setting).generate(wkt_text)
        wd.to_file(img_path)
        return True
    except:
        return False

def get_wordcloud(text, img_path):
    
    try:
        wkt_text = get_feature_wkt(text)
        wd = WordCloud(**wordcloud_setting).generate(wkt_text)
        wd.to_file(img_path)
        return True
    except:
        return False 
