

def gen_prompt(ja_text):
    return f"""<|user|>
{ja_text}<|end|>
<|assistant|>"""


def gen_prompt_for_keywords(q):
    ja_text = f"""次の質問に回答するために検索用の主要なキーワードをカンマ区切りのリストで出力しなさい｡
-単語以外は出力しないこと

#例
#質問
日本の高齢化社会について考える上で大切な論点は?
#キーワード
日本,高齢化,社会

#質問
{q}
#キーワード
"""

    return gen_prompt(ja_text)


def gen_prompt_for_page_choice(q, wiki_hit_titles):
    keywords = ",".join(wiki_hit_titles)
    ja_text = f"""次の質問に回答するために最も適した単語を､#キーワードから一つだけ選びなさい｡
-もし可能なら､質問文から単語を選ぶこと
-質問文と関係性の高い単語を選ぶこと

#例
#質問
日本の総理大臣は?
#キーワード
日本,総理大臣,趣味,遊び
#出力
総理大臣

#質問
{q}
#キーワード
{keywords}
#出力
"""
    return gen_prompt(ja_text)


def gen_prompt_for_rag(q, rag_content, max_content_length=4096):
    content = rag_content[:max_content_length]
    ja_text = f"""#情報をもとに､質問に回答しなさい｡ただし､#情報は間違っているケースも多いので､その場合は#情報は参考にせず回答しなさい｡
#情報
{content}

#質問
{q}
"""
    return gen_prompt(ja_text)
