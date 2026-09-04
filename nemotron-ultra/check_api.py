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

client = OpenAI(api_key=api_key, base_url=base_url)

response = client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": "user",
            "content": "Responda em português: confirme em uma frase qual modelo está atendendo esta chamada."
        }
    ],
    temperature=0.2,
    max_tokens=250,
)

print(response.choices[0].message.content)
