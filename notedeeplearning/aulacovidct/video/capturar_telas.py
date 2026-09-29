"""Captura as telas do notebook pipeline_treinamento_covid_ct.ipynb aberto no Jupyter, para o vídeo da aula.

Uso (com o Jupyter rodando):
    python capturar_telas.py "http://localhost:8890/notebooks/pipeline_treinamento_covid_ct.ipynb?token=SEU_TOKEN"

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
    ("01_abertura",               0,  None, 0),
    ("02_pipeline_conceitos",     0,  "O caminho que", 0),
    ("03_bibliotecas_gpu",        3,  None, 0),
    ("04_configuracoes",          5,  None, 0),
    ("05_dados_contagem",         7,  None, 0),
    ("06_dados_exemplos",         9,  None, 0),
    ("07_divisao_explicacao",    11,  None, 0),
    ("08_divisao_codigo",        12,  None, 0),
    ("09_carregamento",          13,  None, 0),
    ("10_carregamento_saida",    14,  "SAIDA", 0),
    ("11_aumento_explicacao",    15,  None, 0),
    ("12_aumento_exemplo",       17,  None, 0),
    ("13_vgg16_explicacao",      19,  None, 0),
    ("14_vgg16_saida",           20,  None, 0),
    ("15_cabeca_explicacao",     21,  None, 0),
    ("16_cabeca_resumo",         22,  "SAIDA", 0),
    ("17_treino1_explicacao",    23,  None, 0),
    ("18_treino1_inicio",        24,  "SAIDA", 0),
    ("19_treino1_fim",           24,  "Fase 1:", 1),
    ("20_ajustefino_explicacao", 25,  None, 0),
    ("21_ajustefino_fim",        26,  "Fase 2:", 1),
    ("22_curvas_explicacao",     27,  None, 0),
    ("23_curvas_grafico",        28,  "SAIDA", 0),
    ("24_relatorio",             29,  None, 0),
    ("25_metricas_explicacao",   31,  None, 0),
    ("26_matriz_confusao",       32,  "SAIDA", 0),
    ("27_metricas_valores",      32,  "VP=", 1),
    ("28_salvar_modelo",         33,  None, 0),
    ("29_previsao_imagem",       35,  None, 0),
    ("30_previsoes_grade",       38,  "SAIDA", 0),
    ("31_resumo_exercicios",     39,  None, 0),
]

# Células que NÃO aparecem no vídeo (seção "0. Como rodar este notebook": fica só no notebook)
OCULTAR = [1, 2]

# Nenhum arquivo extra mostrado no editor
ARQUIVOS = []

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
    pagina.add_style_tag(content=".jp-cell-toolbar{display:none!important}")
    # tira a seleção/destaque azul da célula ativa
    pagina.add_style_tag(content=".jp-Cell.jp-mod-active .jp-Collapser, .jp-Cell.jp-mod-selected{background:transparent!important} .jp-Notebook .jp-Cell.jp-mod-active .jp-Collapser{background:transparent!important} .jp-Notebook .jp-Cell.jp-mod-selected{border-color:transparent!important;box-shadow:none!important}")
    pagina.evaluate("document.querySelectorAll('.jp-mod-active,.jp-mod-selected').forEach(e=>e.classList.remove('jp-mod-active','jp-mod-selected'))")
    # O Jupyter esconde saídas além da 50ª atrás de "Show more outputs": expande tudo
    for i in (24, 26):
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

