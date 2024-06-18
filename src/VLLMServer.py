from openai import OpenAI
# "A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions. USER: {user_input} ASSISTANT:"


def ask_llm(client_dict, model_name, question,

            ):
    client = client_dict[model_name]["client"]
    model = client_dict[model_name]["name"]
    completion = client.chat.completions.create(
        model=model,
        messages=[
            # {"role": "system", "content": "以下は、タスクを説明する指示と、文脈のある入力の組み合わせです。要求を適切に満たす応答を書きなさい。"},
            {"role": "user", "content": question}
        ]
    )

    return completion.choices[0].message.content.strip()


def ask_llm_prompt(client_dict, model_name, question,):
    client = client_dict[model_name]["client"]

    template1 = client_dict[model_name]["config"]["template1"]
    template2 = client_dict[model_name]["config"]["template2"]
    prompt = template1+question+template2
    completion = client.completions.create(model=model_name,
                                           prompt=prompt,
                                           max_tokens=int(client_dict[model_name]["config"]["max_tokens"]))
    return completion.choices[0].text.strip()  # .message.content.strip()


def get_client_dict(conf):
    server_dict = {}

    for model_conf in conf:
        port = model_conf["PORT"]
        openai_api_key = "EMPTY"
        openai_api_base = f"http://localhost:{port}/v1"
        client = OpenAI(
            api_key=openai_api_key,
            base_url=openai_api_base,
        )
        name = model_conf["name"]
        server_dict[name] = {
            # "model": model_conf["model"],
            "client": client,
            "config": model_conf,
        }

    return server_dict


def launch_command(conf):
    cmd = ""
    for model_conf in conf:
        cmd += _launch_command(model_conf)+"\n\n"

    return cmd


def _launch_command(model_conf):
    cmd = ""
    model_name = model_conf["name"]
    port = model_conf["PORT"]
    gpu_id = model_conf["GPU_ID"]
    max_model_len = model_conf["max-model-len"]
    cmd += f"export CUDA_VISIBLE_DEVICES={gpu_id}\n"
    cmd += f"""python -m vllm.entrypoints.openai.api_server \
--model {model_name} --max-model-len {max_model_len} --port {port} \
"""
    if "tensor-parallel-size" in model_conf:
        tensor_parallel_size = model_conf["tensor-parallel-size"]
        cmd+=f"--tensor-parallel-size {tensor_parallel_size} "
    if "gpu-memory-utilization" in model_conf:
        gpu_util = model_conf["gpu-memory-utilization"]
        cmd+=f"--gpu-memory-utilization {gpu_util} "
    if "template" in model_conf:
        template = model_conf["template"]
        cmd += f"--chat-template {template} "
    return cmd
