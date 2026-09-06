# NemoClaw 360 — implantação

Este diretório contém a configuração de uma equipe multiagente para operar o negócio Presença Local 360 / Vitrine Local 360.

## Onde rodar
Preferência: MacBook Air Apple Silicon com Docker Desktop ou Colima. Não usar GitHub Codespaces como ambiente principal de NemoClaw.

## Pré-requisitos
1. Docker Desktop ou Colima funcionando.
2. Terminal do macOS.
3. NVIDIA API key válida para NVIDIA Endpoints.
4. Opcional, mas recomendado para pesquisa web: Tavily API key ou Brave Search API key.

## Instalar NemoClaw
No Terminal do Mac:

```bash
curl -fsSL https://www.nvidia.com/nemoclaw.sh | bash
```

Aceite o aviso de software de terceiros quando solicitado.

## Onboarding recomendado
Use OpenClaw como agente principal.
Use NVIDIA Endpoints como provider.
Escolha `nvidia/nemotron-3-ultra-550b-a55b` como modelo principal.
Nome sugerido do sandbox: `vitrine360`.

Para iniciar com a equipe declarativa:

```bash
nemoclaw onboard --agents ./agents.yaml --name vitrine360
```

No assistente interativo:
- Agent: OpenClaw
- Provider: NVIDIA Endpoints
- Model: nvidia/nemotron-3-ultra-550b-a55b
- Web Search: Tavily ou Brave, se a chave já estiver disponível
- Network policy: Balanced para começar

## Instalar o skill do negócio
Depois que o sandbox estiver pronto:

```bash
nemoclaw vitrine360 skill install ./skills/presenca-local-360/
```

## Verificar equipe

```bash
nemoclaw vitrine360 agents list
nemoclaw vitrine360 status
```

## Abrir o agente
Interface no terminal:

```bash
nemoclaw launch vitrine360
```

Ou dashboard:

```bash
nemoclaw vitrine360 dashboard-url --quiet
```

## Prompt inicial recomendado

```text
Você é o coordenador geral do negócio Presença Local 360. Leia o skill presenca-local-360 e use os subagentes. Primeiro construa um plano operacional de 30 dias para transformar o negócio em vendas reais na Baixada Santista, usando o que já existe no workspace. Delegue pesquisa de mercado, nichos, oferta, preços, prospecção, vendas, SEO/copy, jurídico/operação, marca/site e revisão crítica. Não aceite respostas genéricas: cada subagente deve produzir artefatos concretos no workspace e o qa-critic deve revisar antes da síntese final.
```

## Pesquisa web
OpenClaw/NemoClaw suporta Brave Search e Tavily Search. Para prospecção real, habilite uma dessas integrações durante o onboarding. Tavily é útil para pesquisa + extração de páginas; Brave é útil para busca geral.

## Google Maps / Perfil da Empresa
Pesquisa web não substitui Google Places/Maps. Para uma esteira profissional de leads com dados de negócios e fotos públicas, a fase seguinte é integrar Google Maps Platform/Places API com uma chave separada e políticas de acesso mínimas. Não colocar essa chave em arquivos do GitHub.

## Visão / análise de fotos
Nemotron 3 Ultra é o coordenador de texto/raciocínio. Para análise de fotos, usar o subagente multimodal oficial baseado em Nemotron 3 Nano Omni. A configuração é feita após o sandbox principal estar estável; ver `VISION-OMNI.md`.

## Segurança
- nunca versionar chaves;
- credenciais devem ficar no OpenShell/NemoClaw ou em entrada segura do host;
- não automatizar envio de mensagens comerciais sem revisão humana;
- não prometer ranking, vendas ou resultados garantidos;
- manter fontes e data de coleta em cada dossiê de lead.
