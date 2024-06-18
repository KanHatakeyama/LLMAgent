import re

# 出力からコード部分を抜き出し


def extract_code_block(text):
    # This regular expression will match text within triple backticks
    pattern = re.compile(r'```(.*?)```', re.DOTALL)
    code_block = pattern.findall(text)[0]
    name_list = ["python", "パイソン"]
    for n in name_list:
        if code_block.startswith(n):
            code_block = code_block[len(n):]
    return code_block.strip()
