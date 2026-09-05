# Nemotron 3 Ultra — acesso simples

Clique no botão abaixo para abrir ou criar seu ambiente no GitHub Codespaces:

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/salgadao/webgis-teste-santos?quickstart=1)

Depois que abrir a tela parecida com VS Code no navegador, use o Terminal na parte de baixo.

## Comandos

```bash
cd nemotron-ultra
read -s -p "Cole sua NOVA NVIDIA API Key: " NVIDIA_API_KEY; export NVIDIA_API_KEY; echo
python check_api.py
python webui.py
```

Quando `python webui.py` estiver rodando, abra a porta `7860` pela aba **Ports**.

> Segurança: não use nem reutilize uma chave NVIDIA que já tenha sido publicada em conversa, issue, commit ou outro local visível. Gere uma nova chave antes de usar.
