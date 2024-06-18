# from src.VLLMServer import launch_command,get_client_dict,ask_llm,ask_llm_prompt
from tqdm import tqdm
from datasets import load_dataset
from src.code_utils import extract_code_block
from src.process_openmath_ja import parse_record, eval_answer
import yaml
from vllm import SamplingParams, LLM
import json

# %%
out_path = "processed/data.jsonl"

# %%

# load dataset
ds = load_dataset("kunishou/OpenMathInstruct-1-1.8m-ja",
                  split="train", streaming=False)

# ds=ds.shuffle()

# %%
model_name = "microsoft/Phi-3-medium-128k-instruct"

llm = LLM(model=model_name, trust_remote_code=True,
          max_model_len=20000
          )

# %%
model_name = "microsoft/Phi-3-medium-128k-instruct"
pre_command = """次の問題を解きなさい｡出力事項は以下のとおりである｡
#解説: 問題を解くための基本的な考え方を日本語で出力する｡
#Python: 計算プログラム｡以下の例を参考に､出力形式を守ること｡
```
#a+bの計算を行う
a=1
b=2
print(a+b)
```
#問題
"""

# %%
batch_size = 300
idx = 0


for j in tqdm(range(int(len(ds)/batch_size))):

    prompts = []
    answer_list = []
    question_list = []
    idx_list = []

    for i in range(batch_size):
        record = ds[idx]
        idx += 1
        # 問題文と回答の取得
        question, answer = parse_record(record)
        answer_list.append(answer)
        question_list.append(question)
        idx_list.append(idx)

        # promptの生成
        ja_text = pre_command+question
        prompt = f"""<|user|>
{ja_text}<|end|>
<|assistant|>"""
        prompts.append(prompt)

    # 回答の生成
    outputs = llm.generate(
        prompts,
        sampling_params=SamplingParams(
            temperature=0.1,
            max_tokens=1024,
            repetition_penalty=1.2,
        )
    )

    # 回答のチェック
    for i in range(len(outputs)):
        res = outputs[i].outputs[0].text.strip()
        res = res.replace("\'", "`")

        # 生成されたコードを実際にまわして評価する
        explanation_block = res[:res.find("```")]
        try:
            code_block = extract_code_block(res)
        except:
            continue

        answer = answer_list[i]
        question = question_list[i]
        # 真偽判定
        is_correct_answer = eval_answer(code_block, answer, verbose=False)

        generated_prompt = explanation_block+"\n"+code_block
        if is_correct_answer:
            new_record = {
                "id": idx_list[i],
                "question": question,
                "prediction": generated_prompt,
                "answer": answer,

            }
            with open(out_path, "a") as f:
                f.write(json.dumps(new_record, ensure_ascii=False)+"\n")

# %%
