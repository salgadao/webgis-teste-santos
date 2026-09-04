# NVIDIA Nemotron 3 Ultra — starter

Este diretório deixa pronto o caminho mais simples para usar o **NVIDIA Nemotron 3 Ultra hospedado pela NVIDIA**, sem precisar baixar o modelo nem possuir hardware DGX.

## Modelo

- Model ID: `nvidia/nemotron-3-ultra-550b-a55b`
- Endpoint NVIDIA NIM: `https://integrate.api.nvidia.com/v1`
- Acesso: NVIDIA-hosted endpoint (API compatível com OpenAI)

## 1. Obtenha sua chave NVIDIA

Abra a página oficial do modelo no NVIDIA API Catalog:

`https://build.nvidia.com/nvidia/nemotron-3-ultra-550b-a55b`

Faça login/crie sua conta NVIDIA Developer e clique em **Get API Key / Generate API Key**. A chave normalmente começa com `nvapi-`.

**Nunca coloque a chave dentro do código ou faça commit dela no GitHub.**

## 2. Configuração local ou Codespaces

Copie `.env.example` para `.env` e preencha:

```bash
cp .env.example .env
```

Depois edite `.env`:

```text
NVIDIA_API_KEY=nvapi-SUA_CHAVE_AQUI
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

## 3. Teste a conexão

```bash
python check_api.py
```

Se estiver funcionando, você verá uma resposta produzida pelo Nemotron 3 Ultra.

## 4. Conversar pelo terminal

```bash
python chat.py
```

Digite suas mensagens. Use `/sair` para encerrar.

## 5. Interface web

```bash
python webui.py
```

Abra a porta `7860` no navegador. Em GitHub Codespaces, a aba **Ports** permite abrir a URL pública/privada correspondente.

## GitHub Codespaces

O projeto inclui `.devcontainer/devcontainer.json`. Depois que a chave estiver configurada como Secret/variável no ambiente, você pode executar todo o cliente no navegador sem instalar Python no seu computador.

## Segurança

`.env` está bloqueado no `.gitignore`. Não coloque `NVIDIA_API_KEY` em arquivos versionados, issues, commits ou mensagens públicas.

## E depois: agentes

O Ultra pode ser usado como cérebro de ferramentas agentic. A NVIDIA documenta integrações com OpenCode, OpenClaw, Kilo Code, OpenHands, Hermes e Pi. Primeiro valide o acesso com `check_api.py`; depois conecte um agent harness.
