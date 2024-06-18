import re

# 出力からコード部分を抜き出し


def extract_code_block(text):
    # This regular expression will match text within triple backticks
    pattern = re.compile(r'```(.*?)```', re.DOTALL)
    code_block = pattern.findall(text)[0]
    if code_block.startswith("python"):
        code_block = code_block[len("python"):]
    return code_block.strip()
