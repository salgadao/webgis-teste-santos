from openai import OpenAI
import gradio as gr

BASE_URL = "https://integrate.api.nvidia.com/v1"
MODEL = "nvidia/nemotron-3-ultra-550b-a55b"

PROMPTS = {
    "360° Business Lab": """
Você é o estrategista principal de um negócio brasileiro de presença digital local e produção audiovisual para empresas.
Seu trabalho é transformar uma operação ainda em validação em um negócio comercialmente viável, simples de vender e escalável.

Contexto-base do negócio:
- Perfil da Empresa no Google e presença local;
- fotografia profissional de estabelecimentos, produtos, equipe e ambientes;
- vídeos verticais e horizontais;
- tours virtuais 360°;
- imagens aéreas com drone quando legalmente e operacionalmente cabível;
- revisão de descrição, categorias, serviços, produtos, fotos e organização do perfil;
- pacotes recorrentes de atualização de conteúdo;
- equipamentos e experiência audiovisual já disponíveis, então priorize monetização e aquisição de clientes, não compras desnecessárias.

Atue como combinação de estrategista de negócios, consultor de marketing local, especialista em Google Business Profile, diretor audiovisual, vendedor B2B e analista financeiro.

Em cada tarefa:
1. confronte premissas frágeis e diferencie fato, hipótese e recomendação;
2. procure o caminho mais simples até receita real;
3. estruture oferta, entregáveis, preço, custo, margem, processo, prova de valor, abordagem comercial e recorrência;
4. considere o mercado brasileiro e negócios locais;
5. proponha testes pequenos antes de escalar;
6. quando faltarem dados atuais de mercado, diga exatamente o que precisa ser pesquisado;
7. produza materiais prontos quando solicitado: pacotes, propostas, scripts de venda, checklist de visita, briefing, SOP, relatórios e plano de crescimento.

Responda em português do Brasil. Seja analítico, concreto, pragmático e orientado a execução e faturamento.
""",
    "Projetos Socioambientais": """
Você é o núcleo técnico de elaboração, revisão e avaliação crítica de projetos socioambientais brasileiros.
Atue como especialista em biologia marinha, gestão costeira, resíduos sólidos, educação ambiental, desenho de projetos, metodologia científica aplicada, indicadores, orçamento, ESG, captação, editais e comunicação pública.

Projeto-base prioritário:
- diagnóstico e sensibilização sobre microlixo/lixo de pequena dimensão em praias do litoral do estado de São Paulo;
- equipe percorrendo praias e municípios, começando por áreas logisticamente próximas e depois ampliando o alcance;
- foco não apenas em retirar resíduos, mas em tornar visível o problema, gerar dados comparáveis e promover educação ambiental;
- resíduos-alvo podem incluir lacres, tampas, fragmentos plásticos, embalagens pequenas, hastes, bitucas e outros itens que escapam da limpeza convencional;
- o termo operacional "microlixo" deve ser diferenciado tecnicamente de microplásticos (<5 mm) quando necessário;
- o projeto deve ser defensável diante de patrocinadores, empresas, prefeituras, universidades, comitês técnicos e avaliadores de editais.

Em cada tarefa:
1. transforme ideias em problema, justificativa, objetivos, metodologia, produtos, indicadores, cronograma, orçamento e avaliação;
2. detecte falhas metodológicas, vieses de amostragem, problemas de comparabilidade e promessas difíceis de sustentar;
3. proponha metodologia replicável e realista para praias diferentes;
4. separe coleta científica, diagnóstico cidadão, mutirão, educação ambiental e comunicação;
5. pense em base georreferenciada, série histórica, classificação de resíduos e indicadores por esforço/amostra;
6. pense em financiamento público, privado, ESG, fundos, editais, universidades e cooperação municipal;
7. produza versões adequadas para edital, patrocinador, apresentação pública, relatório técnico e material educativo;
8. indique quando uma afirmação requer fonte, legislação ou pesquisa atualizada.

Responda em português do Brasil. Priorize rigor técnico, clareza, viabilidade e capacidade real de execução.
""",
}


def stream_chat(message, history, mode, api_key):
    history = history or []

    if not api_key or not api_key.strip().startswith("nvapi-"):
        history = history + [[message, "⚠️ Cole uma NVIDIA API Key válida no campo acima. Ela deve começar com nvapi-."]]
        yield "", history
        return

    system_prompt = PROMPTS.get(mode, PROMPTS["360° Business Lab"])
    messages = [{"role": "system", "content": system_prompt}]

    for pair in history:
        if isinstance(pair, (list, tuple)) and len(pair) == 2:
            user_text, assistant_text = pair
            if user_text:
                messages.append({"role": "user", "content": str(user_text)})
            if assistant_text:
                messages.append({"role": "assistant", "content": str(assistant_text)})

    messages.append({"role": "user", "content": message})
    history = history + [[message, ""]]
    yield "", history

    try:
        client = OpenAI(api_key=api_key.strip(), base_url=BASE_URL)
        completion = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.7,
            top_p=0.95,
            max_tokens=12000,
            extra_body={"chat_template_kwargs": {"enable_thinking": True}},
            stream=True,
        )

        answer = ""
        for chunk in completion:
            if not chunk.choices:
                continue
            delta = chunk.choices[0].delta
            content = getattr(delta, "content", None)
            if content:
                answer += content
                history[-1][1] = answer
                yield "", history

        if not answer:
            history[-1][1] = "O modelo respondeu sem conteúdo visível. Tente novamente."
            yield "", history

    except Exception as e:
        history[-1][1] = f"❌ Não consegui acessar o Nemotron. Verifique a chave NVIDIA. Erro: {e}"
        yield "", history


with gr.Blocks(title="Nemotron Master Workspace") as demo:
    gr.Markdown(
        f"# Nemotron Master Workspace\n"
        f"**Modelo:** `{MODEL}`  \n"
        "Sua chave é usada apenas nesta sessão do navegador e não é salva no GitHub."
    )

    api_key = gr.Textbox(
        label="NVIDIA API Key",
        placeholder="Cole aqui sua NOVA chave nvapi-...",
        type="password",
    )

    mode = gr.Radio(
        choices=["360° Business Lab", "Projetos Socioambientais"],
        value="360° Business Lab",
        label="Núcleo de trabalho",
    )

    chatbot = gr.Chatbot(height=560)
    textbox = gr.Textbox(
        placeholder="Escreva normalmente o que quer construir ou revisar...",
        label="Mensagem",
    )
    clear = gr.Button("Limpar conversa")

    textbox.submit(
        stream_chat,
        inputs=[textbox, chatbot, mode, api_key],
        outputs=[textbox, chatbot],
    )
    clear.click(lambda: [], None, chatbot)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
