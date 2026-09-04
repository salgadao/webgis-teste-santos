import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

load_dotenv()

api_key = os.getenv("NVIDIA_API_KEY")
base_url = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")
model = os.getenv("NEMOTRON_MODEL", "nvidia/nemotron-3-ultra-550b-a55b")

if not api_key or api_key.startswith("nvapi-SUA_CHAVE"):
    raise SystemExit("Configure NVIDIA_API_KEY no arquivo .env antes de iniciar a interface.")

client = OpenAI(api_key=api_key, base_url=base_url)

SYSTEM = "Você é um assistente técnico. Responda em português do Brasil, de forma clara e precisa."


def respond(message, history):
    messages = [{"role": "system", "content": SYSTEM}]
    for item in history:
        role = item.get("role")
        content = item.get("content")
        if role in {"user", "assistant"} and isinstance(content, str):
            messages.append({"role": role, "content": content})
    messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.4,
        max_tokens=2000,
    )
    return response.choices[0].message.content or ""


demo = gr.ChatInterface(
    fn=respond,
    type="messages",
    title="NVIDIA Nemotron 3 Ultra",
    description=f"Modelo: {model}",
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
