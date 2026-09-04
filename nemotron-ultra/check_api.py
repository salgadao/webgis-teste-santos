import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("NVIDIA_API_KEY")
base_url = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")
model = os.getenv("NEMOTRON_MODEL", "nvidia/nemotron-3-ultra-550b-a55b")

if not api_key or api_key.startswith("nvapi-SUA_CHAVE"):
    raise SystemExit(
        "NVIDIA_API_KEY não configurada. Copie .env.example para .env e coloque sua chave NVIDIA."
    )

client = OpenAI(base_url=base_url, api_key=api_key)

completion = client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": "user",
            "content": "Responda em português do Brasil. Confirme que a chamada ao Nemotron 3 Ultra está funcionando e explique em uma frase o que você é capaz de fazer."
        }
    ],
    temperature=1,
    top_p=0.95,
    max_tokens=16384,
    extra_body={"chat_template_kwargs": {"enable_thinking": True}},
    stream=True,
)

print(f"Modelo: {model}\n")
print("--- raciocínio ---")
in_answer = False
for chunk in completion:
    if not chunk.choices:
        continue

    delta = chunk.choices[0].delta
    reasoning = getattr(delta, "reasoning_content", None)
    if reasoning:
        print(reasoning, end="", flush=True)

    if delta.content is not None:
        if not in_answer:
            print("\n\n--- resposta ---")
            in_answer = True
        print(delta.content, end="", flush=True)

print("\n")
