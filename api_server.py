# %%
from src.Client import Client
from src.TanukiBot import TanukiBot
from src.GeneralBot import GeneralBot
import datetime
import time
import random
from src.VLLMServer import launch_command, get_client_dict, ask_llm_prompt

# %%
import yaml

# %%
conf_path = "config.yaml"

with open(conf_path, "r") as f:
    conf = yaml.safe_load(f.read())

print("run the following llm servers!!")
print(launch_command(conf))
print("---------------")

# %%
client_dict = get_client_dict(conf)
# %%

# %%

with open("env/url.txt") as f:
    url = f.read().strip()

# apiクライアントとchatbotを起動
client = Client(url)


# %%
model_list = list(client_dict.keys())


# %%
while True:
    try:
        row_id, question, inst = client.get_unanswered_question()
    except Exception as e:
        print(e)
        time.sleep(5)
        continue
    if question == "":
        print("no question to answer")
        time.sleep(5)
        continue

    print(question)
    try:
        model_name_A, model_name_B = random.sample(model_list, 2)
        responseA = ask_llm_prompt(client_dict, model_name_A, question)
        responseB = ask_llm_prompt(client_dict, model_name_B, question)
        meta1 = model_name_A
        meta2 = model_name_B
        meta3 = datetime.datetime.now().isoformat()

        client.answer(row_id, responseA, responseB, metainfo1=meta1,
                      metainfo2=meta2, metainfo3=meta3)
    except Exception as e:
        print(e)
        time.sleep(5)


# %%
