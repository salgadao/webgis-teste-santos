#!/usr/bin/env bash
set -euo pipefail

SANDBOX_NAME="vitrine360"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

printf '\n=== NemoClaw 360 — instalador guiado ===\n\n'

ARCH="$(uname -m)"
printf 'Arquitetura detectada: %s\n' "$ARCH"
if [[ "$ARCH" != "arm64" ]]; then
  printf '\nATENÇÃO: este fluxo foi preparado para Mac Apple Silicon (arm64).\n'
  printf 'Consulte a matriz oficial do NemoClaw antes de continuar.\n'
  exit 2
fi

if ! command -v docker >/dev/null 2>&1; then
  printf '\nDocker não foi encontrado.\n'
  printf 'Instale/inicie Docker Desktop OU Colima antes de continuar.\n'
  printf 'Depois confirme no Terminal com: docker info\n'
  exit 3
fi

if ! docker info >/dev/null 2>&1; then
  printf '\nDocker existe, mas não está rodando/acessível.\n'
  printf 'Abra Docker Desktop ou inicie Colima e rode este script novamente.\n'
  exit 4
fi

printf 'Docker: OK\n'

if ! command -v nemoclaw >/dev/null 2>&1; then
  printf '\nInstalando NemoClaw pelo instalador oficial NVIDIA...\n'
  curl -fsSL https://www.nvidia.com/nemoclaw.sh | bash
else
  printf 'NemoClaw já instalado: %s\n' "$(command -v nemoclaw)"
fi

printf '\nModelos/agents disponíveis no NemoClaw:\n'
nemoclaw agents list || true

printf '\nCole sua NVIDIA API key quando solicitado. Ela NÃO aparecerá na tela.\n'
read -r -s -p 'NVIDIA API key (nvapi-...): ' NVIDIA_INFERENCE_API_KEY
printf '\n'
export NVIDIA_INFERENCE_API_KEY

if [[ "$NVIDIA_INFERENCE_API_KEY" != nvapi-* ]]; then
  printf 'A chave não parece começar com nvapi-. Abortando.\n'
  unset NVIDIA_INFERENCE_API_KEY
  exit 5
fi

# O Nemotron 3 Ultra suporta contexto de até 1 milhão de tokens. NemoClaw permite
# gravar esse limite no config gerado durante o onboarding.
export NEMOCLAW_CONTEXT_WINDOW=1000000
export NEMOCLAW_REASONING=true

printf '\nPesquisa web opcional.\n'
printf 'Se você já tiver Tavily API key, cole agora; senão apenas pressione Enter.\n'
read -r -s -p 'Tavily API key (opcional): ' TAVILY_API_KEY
printf '\n'

if [[ -n "$TAVILY_API_KEY" ]]; then
  export TAVILY_API_KEY
  export NEMOCLAW_WEB_SEARCH_PROVIDER=tavily
  printf 'Tavily será configurado durante o onboarding.\n'
else
  export NEMOCLAW_WEB_SEARCH_PROVIDER=none
  printf 'Pesquisa web ficará desativada nesta primeira instalação. Poderá ser adicionada depois.\n'
fi

printf '\nIniciando onboarding do OpenClaw com equipe multiagente...\n'
printf 'Quando o assistente perguntar o provider, escolha NVIDIA Endpoints.\n'
printf 'Quando perguntar o modelo, escolha nvidia/nemotron-3-ultra-550b-a55b.\n\n'

nemoclaw onboard \
  --agent openclaw \
  --agents "$SCRIPT_DIR/agents.yaml" \
  --name "$SANDBOX_NAME"

printf '\nInstalando skill Presença Local 360...\n'
nemoclaw "$SANDBOX_NAME" skill install "$SCRIPT_DIR/skills/presenca-local-360/"

printf '\nVerificando status e agentes...\n'
nemoclaw "$SANDBOX_NAME" status || true
nemoclaw "$SANDBOX_NAME" agents list || true

printf '\n=== PRONTO ===\n'
printf 'Abrir no terminal: nemoclaw launch %s\n' "$SANDBOX_NAME"
printf 'Dashboard: nemoclaw %s dashboard-url --quiet\n' "$SANDBOX_NAME"
printf '\nA chave NVIDIA foi usada apenas como variável do processo. Feche este Terminal ao terminar.\n'

unset NVIDIA_INFERENCE_API_KEY
unset TAVILY_API_KEY 2>/dev/null || true
unset NEMOCLAW_CONTEXT_WINDOW
unset NEMOCLAW_REASONING
