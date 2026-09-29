"""Captura as telas do notebook pipeline_de_agentes.ipynb aberto no Jupyter, para o vídeo da aula.

Uso (com o Jupyter rodando):
    python capturar_telas.py "http://localhost:8890/notebooks/pipeline_de_agentes.ipynb?token=SEU_TOKEN"

Cada cena rola o notebook até uma célula (e, opcionalmente, até um trecho de texto dentro
dela) e salva uma imagem 1920x1080 em video/telas/.
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

URL = sys.argv[1]
BASE = URL.split("/notebooks/")[0]
TOKEN = URL.split("token=")[-1]
PREFIXO = URL.split("/notebooks/")[1].split("?")[0].rpartition("/")[0]   # pasta do notebook dentro do servidor Jupyter
PASTA = Path(__file__).parent / "telas"
PASTA.mkdir(exist_ok=True)

# (arquivo, índice da célula, âncora, número)
# âncora: None = topo da célula | "SAIDA" = topo da saída | "PX" = rolar N pixels a partir do topo
#         | texto = N-ésima ocorrência desse texto dentro da célula
CENAS = [
    ("01_abertura",                 0,  None, 0),
    ("02_arquitetura_conceitos",    0,  "Ao todo são", 0),
    ("03_prerequisitos_chaves",     3,  None, 0),
    ("04_versoes",                  4,  None, 0),
    ("05_importacoes_env",          6,  None, 0),
    ("06_chaves_llm",               8,  None, 0),
    ("07_yaml_explicacao",        10,  None, 0),
    ("08_yaml_carregamento",      11,  None, 0),
    ("10_pydantic_explicacao",   12,  None, 0),
    ("11_pydantic_codigo",       13,  None, 0),
    ("12_ferramentas",           14,  None, 0),
    ("13_crew1_explicacao",      16,  None, 0),
    ("14_crew1_codigo",          17,  None, 0),
    ("15_crew2",                 18,  None, 0),
    ("16_flow_explicacao",       20,  None, 0),
    ("17_flow_codigo",           21,  None, 0),
    ("18_diagrama_explicacao",   22,  None, 0),
    ("19_diagrama_fluxo",        23,  "SAIDA", 0),
    ("20_execucao_inicio",       24,  None, 0),
    ("21_exec_crew_iniciada",    25,  "Crew Execution Started", 0),
    ("22_exec_agente_dados",     25,  "Agent Started", 0),
    ("23_exec_ferramenta_busca", 25,  "Tool Execution Started", 0),
    ("24_exec_resposta_dados",   25,  "Agent Final Answer", 0),
    ("25_exec_agente_afinidade", 25,  "Agent Started", 1),
    ("26_exec_avaliador",        25,  "Agent Started", 2),
    ("27_exec_resposta_nota",    25,  "Agent Final Answer", 2),
    ("28_exec_redator_email",    25,  "Agent Started", 3),
    ("29_exec_email_final",      25,  "Agent Final Answer", 4),
    ("30_exec_fluxo_concluido",  25,  "Flow Completion", 0),
    ("31_custos",                26,  None, 0),
    ("32_tabela_lead",           29,  None, 0),
    ("33_tabela_lead_final",     30,  "SAIDA", 0),
    ("34_email_gerado",          31,  None, 0),
    ("35_router_explicacao",     33,  None, 0),
    ("36_router_codigo",         34,  "PX", 620),
    ("37_diagrama_completo",     36,  "SAIDA", 0),
    ("38_fluxo_completo_email",  38,  "E-MAIL GERADO PELO FLUXO COMPLETO", 1),
    ("39_resumo_exercicios",     39,  None, 0),
]

# Células que NÃO aparecem no vídeo (seção "0. Rodando no Google Colab": fica só no notebook)
OCULTAR = [1, 2]

# Arquivos YAML mostrados no editor do Jupyter
ARQUIVOS = [
    ("09_yaml_agentes", "config/agentes_qualificacao_leads.yaml"),
    ("09b_yaml_tarefas", "config/tarefas_qualificacao_leads.yaml"),
]

JS_ROLAR_TEXTO = """([celula, texto, n, deslocamento]) => {
    // Acha a n-ésima ocorrência do texto dentro da célula e rola até ela
    const w = document.createTreeWalker(celula, NodeFilter.SHOW_TEXT);
    let achados = 0, no;
    while ((no = w.nextNode())) {
        let i = no.textContent.indexOf(texto);
        while (i >= 0) {
            const r = document.createRange(); r.setStart(no, i); r.setEnd(no, i + texto.length);
            const visivel = r.getBoundingClientRect().height > 0;   // ignora o fonte oculto das células Markdown
            if (visivel && achados === n) {
                let p = celula.parentElement;
                while (p && !(p.scrollHeight > p.clientHeight && getComputedStyle(p).overflowY.match(/auto|scroll/))) p = p.parentElement;
                p.scrollTop += r.getBoundingClientRect().top - p.getBoundingClientRect().top - deslocamento;
                return true;
            }
            if (visivel) achados++;
            i = no.textContent.indexOf(texto, i + 1);
        }
    }
    return achados;
}"""

JS_ROLAR = """([el, deslocamento]) => {
    el.scrollIntoView({block: 'start'});
    let p = el.parentElement;
    while (p && !(p.scrollHeight > p.clientHeight && getComputedStyle(p).overflowY.match(/auto|scroll/))) p = p.parentElement;
    if (p) p.scrollTop -= deslocamento;
}"""

with sync_playwright() as p:
    navegador = p.chromium.launch()
    pagina = navegador.new_page(viewport={"width": 1536, "height": 864}, device_scale_factor=1.25)

    pagina.goto(URL)
    pagina.wait_for_selector(".jp-Cell", timeout=60000)
    pagina.wait_for_timeout(5000)
    # Mostra as saídas longas inteiras (sem caixa de rolagem) e limpa a seleção inicial
    pagina.add_style_tag(content=".jp-mod-outputsScrolled .jp-OutputArea { max-height: none !important; overflow: visible !important; }")
    pagina.evaluate("document.querySelectorAll('.jp-mod-outputsScrolled').forEach(e => e.classList.remove('jp-mod-outputsScrolled'))")

    celulas = pagina.locator(".jp-Notebook .jp-Cell")
    for i in OCULTAR:
        celulas.nth(i).scroll_into_view_if_needed()
        celulas.nth(i).evaluate("e => e.style.display = 'none'")
    pagina.wait_for_timeout(800)
    # O Jupyter esconde saídas além da 50ª atrás de "Show more outputs": expande tudo
    for i in (25, 38):
        celulas.nth(i).scroll_into_view_if_needed()
        pagina.wait_for_timeout(500)
        botoes = celulas.nth(i).locator(".jp-TrimmedOutputs")
        while botoes.count():
            botoes.first.click(); pagina.wait_for_timeout(1500)
    pagina.evaluate("document.querySelectorAll('.jp-mod-outputsScrolled').forEach(e => e.classList.remove('jp-mod-outputsScrolled'))")

    # Opcional: capturar só algumas cenas, ex.: python capturar_telas.py URL 02 38
    filtro = sys.argv[2:]
    for nome, indice, ancora, ocorrencia in CENAS:
        if filtro and not any(nome.startswith(f) for f in filtro):
            continue
        celula = celulas.nth(indice)
        celula.scroll_into_view_if_needed()
        pagina.wait_for_timeout(400)
        if ancora is None or ancora == "PX":
            alvo, deslocamento = celula, (12 if ancora is None else -ocorrencia)
        elif ancora == "SAIDA":
            alvo, deslocamento = celula.locator(".jp-OutputArea").first, 12
        else:
            alvo = None
            achou = pagina.evaluate(JS_ROLAR_TEXTO, [celula.element_handle(), ancora, ocorrencia, 60])
            if achou is not True:
                print(f"  aviso: '{ancora}' #{ocorrencia} não encontrado (há {achou})")
        if alvo is not None:
            pagina.evaluate(JS_ROLAR, [alvo.element_handle(), deslocamento])
        pagina.wait_for_timeout(2500 if "diagrama" in nome else 800)
        pagina.screenshot(path=PASTA / f"{nome}.png")
        print("capturada:", nome)

    for nome, caminho in ARQUIVOS:
        pagina.goto(f"{BASE}/edit/{PREFIXO + '/' if PREFIXO else ''}{caminho}?token={TOKEN}")
        pagina.wait_for_selector(".cm-content", timeout=30000)
        pagina.wait_for_timeout(2500)
        pagina.screenshot(path=PASTA / f"{nome}.png")
        print("capturada:", nome)

    navegador.close()

