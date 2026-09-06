# Esteira profissional de prospecção — Google + web + visão + vendas

## Arquitetura

### 1. Descoberta estruturada — Google Places API (New)
Usar Text Search/Nearby Search para localizar empresas por nicho e região.
Campos mínimos recomendados conforme necessidade/custo:
- place id;
- display name;
- endereço;
- tipo/categoria;
- rating e número de avaliações;
- site;
- telefone público;
- Google Maps URI;
- fotos (resource names).

Nunca usar field mask `*` em produção. Solicitar apenas os campos necessários para reduzir custo e exposição de dados.

### 2. Enriquecimento — Tavily ou Brave
Para cada lead aprovado:
- site oficial;
- página de contato;
- redes/menções públicas;
- cardápio/serviços quando públicos;
- diferenciais;
- notícias/reformas/novidades quando relevantes;
- concorrentes próximos;
- contexto de bairro/turismo.

### 3. Fotos — Google Place Photos
Baixar apenas as fotos necessárias para auditoria visual, preservando metadados/atribuições exigidos pelo serviço e respeitando os termos do Google Maps Platform.

### 4. Visão — Nemotron 3 Nano Omni
Entregar ao `vision-operator` até um conjunto pequeno e representativo de imagens por lead.
O agente devolve fatos visuais e oportunidades de produção, não um julgamento genérico de "foto ruim".

### 5. Estratégia — Nemotron 3 Ultra
`main` combina:
- dados do negócio;
- auditoria visual;
- presença web/local;
- contexto de nicho/região;
- preços/pacotes;
- regras comerciais;
para produzir um dossiê de venda personalizado.

### 6. QA
`qa-critic` verifica fontes, datas e cada afirmação antes de liberar a abordagem.

## Saída por lead
Salvar em `leads/<cidade>/<slug>/`:

```text
lead.json
sources.md
visual-audit.md
google-local-audit.md
sales-brief.md
proposal-angle.md
qa.md
photos/   # somente quando permitido/necessário
```

## Regiões iniciais
### Baixada Santista
- Santos
- São Vicente
- Praia Grande
- Guarujá
- Cubatão conforme nicho

### Litoral Norte
- São Sebastião
- Praia da Baleia e entorno
- Camburi/Camburizinho quando fizer sentido
- Juquehy e eixo turístico próximo, conforme logística e ticket

## Nichos de alto potencial visual
- hotéis/pousadas;
- restaurantes e bares;
- clínicas/estética/odontologia;
- academias/estúdios;
- imobiliárias e imóveis premium;
- arquitetura/interiores;
- lojas/showrooms;
- turismo/experiências;
- espaços de eventos;
- marinas/serviços náuticos quando adequados.

## Filtro de ética e qualidade
Não usar dados pessoais não necessários. Trabalhar com dados empresariais públicos e canais de contato publicados para fins comerciais, respeitando LGPD, termos das plataformas e opt-out. Não automatizar disparos massivos. A meta é prospecção personalizada e justificável.
