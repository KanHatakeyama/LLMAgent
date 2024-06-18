

from vllm import LLM
from vllm import SamplingParams


class GeneralBot:
    def __init__(self,
                 model_name,
                 max_model_len=5000,
                 gpu_memory_utilization=0.2,
                 template1="""<|user|>
""",
                 template2="""<|end|>
<|assistant|>"""
                 ):
        self.model_name = model_name
        self.template1 = template1
        self.template2 = template2

        print("initialing model...")
        self.llm = LLM(model=model_name, trust_remote_code=True,
                       max_model_len=max_model_len,
                       # tensor_parallel_size=2,
                       gpu_memory_utilization=gpu_memory_utilization,
                       )

    def ask(self, question):
        prompts = [self.template1+question+self.template2]
        outputs = self.llm.generate(
            prompts,
            sampling_params=SamplingParams(
                temperature=0.5,
                max_tokens=1000,
            )
        )
        output = outputs[0]
        return output.outputs[0].text.strip()
