
from llama_cpp import Llama
import random

inst_list = [
    "日本語で簡潔に回答してください",
    "日本語で丁寧に回答してください ",
    "日本語で回答してください",
    "日本語で注意深くで回答してください",
    "日本語で心のこもった回答をしてください",
    "日本語で､先生として回答してください",
]


class GGUFBot:
    def __init__(self, model_path="model/Mixtral-8x22B-Instruct-v0.1.Q5_K_M-00001-of-00004.gguf",
                 max_new_tokens=4000,
                 n_ctx=4096,
                 n_gpu_layers=300) -> None:
        print("loading model...")

        self.model = Llama(model_path=model_path,
                           n_ctx=n_ctx, n_gpu_layers=n_gpu_layers, )
        self.max_new_tokens = max_new_tokens

    def ask(self, question):
        inst = random.choice(inst_list)
        prompt = f"""<s>[INST]{inst}\n{question}[/INST]"""

        output = self.model(
            prompt,
            max_tokens=self.max_new_tokens,
            # temperature = 0.7,
            # top_p = 0.8,
            # repeat_penalty = 1.1,
            # frequency_penalty = 1.0,
            # presence_penalty = 1.0,
            # stop = ["\n###  Instruction:", "\n### Response:", "\n"],
            # echo = True,
        )
        return output["choices"][0]["text"].strip()
