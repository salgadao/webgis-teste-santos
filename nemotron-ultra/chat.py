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
        "content": "Você é um assistente técnico. Responda em português do Brasil, de forma clara e precisa."
    }
]

print(f"Nemotron 3 Ultra — modelo: {model}")
print("Digite /sair para encerrar.\n")

while True:
    user_text = input("Você: ").strip()
    if not user_text:
        continue
    if user_text.lower() in {"/sair", "sair", "exit", "quit"}:
        break

    messages.append({"role": "user", "content": user_text})

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.4,
        max_tokens=2000,
    )

    answer = response.choices[0].message.content or ""
    print(f"\nNemotron: {answer}\n")
    messages.append({"role": "assistant", "content": answer})
