import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("NVIDIA_API_KEY")
base_url = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")
model = os.getenv("NEMOTRON_MODEL", "nvidia/nemotron-3-ultra-550b-a55b")

if not api_key or api_key.startswith("nvapi-SUA_CHAVE"):
    raise SystemExit("Configure NVIDIA_API_KEY no arquivo .env antes de iniciar o chat.")

client = OpenAI(api_key=api_key, base_url=base_url)
messages = [
    {
        "role": "system",
        "content": "Você é um assistente técnico. Responda em português do Brasil, de forma clara, precisa e útil."
    }
]

print(f"Nemotron 3 Ultra — modelo: {model}")
print("Raciocínio: ativado | Streaming: ativado")
print("Digite /sair para encerrar.\n")

while True:
    user_text = input("Você: ").strip()
    if not user_text:
        continue
    if user_text.lower() in {"/sair", "sair", "exit", "quit"}:
        break

    messages.append({"role": "user", "content": user_text})

    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=1,
        top_p=0.95,
        max_tokens=16384,
        extra_body={"chat_template_kwargs": {"enable_thinking": True}},
        stream=True,
    )

    reasoning_parts = []
    answer_parts = []
    answer_started = False

    print("\n[Raciocínio]\n", end="")
    for chunk in completion:
        if not chunk.choices:
            continue

        delta = chunk.choices[0].delta
        reasoning = getattr(delta, "reasoning_content", None)
        if reasoning:
            reasoning_parts.append(reasoning)
            print(reasoning, end="", flush=True)

        if delta.content is not None:
            if not answer_started:
                print("\n\n[Nemotron]\n", end="")
                answer_started = True
            answer_parts.append(delta.content)
            print(delta.content, end="", flush=True)

    answer = "".join(answer_parts)
    print("\n")
    messages.append({"role": "assistant", "content": answer})
