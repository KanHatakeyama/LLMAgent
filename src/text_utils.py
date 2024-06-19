import re


def split_keywords(text):
    # 全角および半角のカンマや読点でテキストを分割する
    parts = re.split(r'[、,]', text)
    # 空の文字列を取り除く
    parts = [part.strip() for part in parts if part.strip()]
    return parts
