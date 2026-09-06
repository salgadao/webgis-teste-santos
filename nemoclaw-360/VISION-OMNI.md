# Fase 2 — agente visual com Nemotron 3 Nano Omni

Objetivo: permitir que o coordenador Nemotron 3 Ultra delegue análise de fotos, screenshots, vídeos curtos e documentos visuais a um subagente multimodal.

## Modelo visual
`nvidia/nemotron-3-nano-omni-30b-a3b-reasoning`

## Papel
O `vision-operator` deve:
- analisar fotos públicas do negócio ou imagens fornecidas pelo usuário;
- identificar cobertura visual ausente ou fraca;
- avaliar fachada, ambiente, produto, equipe, iluminação, enquadramento, consistência e atualidade aparente;
- produzir observações factuais, não julgamentos gratuitos;
- sugerir shot list de fotografia profissional;
- indicar quando tour 360° agrega compreensão espacial;
- indicar quando drone agrega contexto de localização/entorno;
- devolver relatório estruturado ao `main`.

## Regra importante
O Ultra continua sendo o coordenador. O Omni é especialista em visão. Não usar o Omni para substituir o planejamento comercial geral.

## Estrutura de saída
Cada auditoria visual deve produzir:

```markdown
# Auditoria visual — <empresa>
## Arquivos analisados
## Fatos observados
## O que já está bom
## Lacunas visuais
## Shot list recomendado
## Oportunidade de 360°
## Oportunidade de drone
## Riscos de inferência / coisas que não dá para concluir
## Evidências para argumento comercial
```

## Implantação
A NVIDIA documenta o padrão `main` + `vision-operator` usando um provider auxiliar do Omni e `sessions_spawn`. Fazer esta etapa somente depois que `vitrine360` estiver estável, porque exige configuração adicional de provider/model e validação de egress/credencial.

A configuração final deve ser validada contra a documentação corrente do NemoClaw antes de aplicar; não copiar credenciais para `openclaw.json` ou para este repositório.
