
from vllm import SamplingParams


class VLLMBot:
    def __init__(self, llm
                 ):
        self.llm = llm

    def ask(self, prompt, max_tokens=2048):
        # 回答の生成
        outputs = self.llm.generate(
            [prompt],
            sampling_params=SamplingParams(
                temperature=0.1,
                max_tokens=max_tokens,
                repetition_penalty=1.2,
            )
        )

        return outputs[0].outputs[0].text.strip()
