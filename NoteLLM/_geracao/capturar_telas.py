"""Gera as capturas de tela das cenas do roteiro a partir de Transformer.ipynb.

1. Converte o notebook em HTML com o visual do JupyterLab (nbconvert, template "lab").
2. Abre o HTML no Chromium com o Playwright.
3. Para cada cena, recorta a região que vai da primeira à última célula da cena
   (incluindo as notas em português das células de código) e salva em roteiro/telas/.
"""
import json
import sys
from pathlib import Path

import nbformat
from nbconvert import HTMLExporter
from playwright.sync_api import sync_playwright

NOTE = Path("/mnt/data1/progpython/notebooksvideoaulas/NoteLLM")
GER = NOTE / "_geracao"
TELAS = NOTE / "roteiro_v2" / "telas"
LARGURA = 1100        # largura da janela, em pixels CSS
ALTURA_MAX = 1250     # altura máxima de uma captura, em pixels CSS
ESCALA = 2            # capturas em alta resolução

CSS_EXTRA = """
body { background: #ffffff !important; }
.jp-Notebook { padding: 12px 24px !important; }
/* notas em português com destaque */
.jp-MarkdownCell blockquote { border-left: 5px solid #1a7f37; background: #eef8f0;
  margin: 4px 0; padding: 8px 14px; color: #1f2328; font-size: 15px; }
.jp-MarkdownCell blockquote p { margin: 0; }
"""


def gerar_html():
    nb = nbformat.read(NOTE / "Transformer.ipynb", as_version=4)
    html, _ = HTMLExporter(template_name="lab").from_notebook_node(nb)
    html = html.replace("</head>", f"<style>{CSS_EXTRA}</style></head>")
    destino = GER / "Transformer_render.html"
    destino.write_text(html, encoding="utf-8")
    return destino, [c.id for c in nb.cells], {c.id: c for c in nb.cells}


def expandir(ids_cena, ordem, por_id):
    """Inclui a nota em português que precede cada célula de código."""
    todos = []
    for cid in ids_cena:
        nota = f"{cid}-pt"
        if nota in por_id and nota not in todos:
            todos.append(nota)
        if cid not in todos:
            todos.append(cid)
    todos.sort(key=ordem.index)
    return todos


def main(somente=None):
    html, ordem, por_id = gerar_html()
    cenas = json.loads((GER / "roteiro_cenas.json").read_text())
    TELAS.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        nav = p.chromium.launch()
        pagina = nav.new_page(viewport={"width": LARGURA, "height": 900}, device_scale_factor=ESCALA)
        pagina.goto(html.as_uri())
        pagina.wait_for_load_state("networkidle")
        pagina.evaluate("document.fonts.ready")

        for cena in cenas:
            if somente and cena["arquivo"] not in somente:
                continue
            ids = expandir(cena["celulas"], ordem, por_id)
            # posição de cada célula em coordenadas da página (independe da rolagem)
            caixas = pagina.evaluate(
                """ids => ids.map(id => {
                    const el = document.getElementById('cell-id=' + id);
                    if (!el) return null;
                    const r = el.getBoundingClientRect();
                    return {top: r.top + window.scrollY, bottom: r.bottom + window.scrollY};
                })""", ids)
            if None in caixas:
                raise RuntimeError(f"célula não encontrada no HTML: {ids[caixas.index(None)]}")

            # Cena que cabe numa tela: captura o trecho inteiro, da primeira à última célula.
            # Cena alta demais: captura só as células da cena, em telas separadas;
            # uma tela nova começa quando há células no meio ou quando a altura passaria do limite.
            grupos = []
            topo, base = min(b["top"] for b in caixas), max(b["bottom"] for b in caixas)
            separar = cena.get("separar", False)   # cena que deve mostrar só as células listadas
            if base - topo <= ALTURA_MAX and not separar:
                grupos = [{"ids": ids, "top": topo, "bottom": base}]
            for cid, caixa in ([] if grupos else zip(ids, caixas)):
                g = grupos[-1] if grupos else None
                vizinha = g and ordem.index(cid) == ordem.index(g["ids"][-1]) + 1
                if g and vizinha and caixa["bottom"] - g["top"] <= ALTURA_MAX:
                    g["ids"].append(cid)
                    g["bottom"] = caixa["bottom"]
                else:
                    grupos.append({"ids": [cid], "top": caixa["top"], "bottom": caixa["bottom"]})
            # uma nota em português sozinha numa tela vai junto com a célula de código seguinte
            for i in range(len(grupos) - 1, 0, -1):
                if all(x.endswith("-pt") for x in grupos[i - 1]["ids"]):
                    grupos[i]["ids"] = grupos[i - 1]["ids"] + grupos[i]["ids"]
                    grupos[i]["top"] = grupos[i - 1]["top"]
                    del grupos[i - 1]
            # tela muito baixa (ex.: só um título) é unida à vizinha, se o trecho resultante couber
            i = 0
            while i < len(grupos) - 1:
                a, b = grupos[i], grupos[i + 1]
                pequena = min(a["bottom"] - a["top"], b["bottom"] - b["top"]) < 160
                vizinhas = ordem.index(b["ids"][0]) == ordem.index(a["ids"][-1]) + 1
                if pequena and b["bottom"] - a["top"] <= ALTURA_MAX and (vizinhas or not separar):
                    grupos[i] = {"ids": a["ids"] + b["ids"], "top": a["top"], "bottom": b["bottom"]}
                    del grupos[i + 1]
                else:
                    i += 1

            arquivos = []
            base_nome = cena["arquivo"][:-4]
            for i, g in enumerate(grupos):
                nome = f"{base_nome}{'' if i == 0 else chr(ord('a') + i)}.png"
                altura_real = g["bottom"] - g["top"]
                altura = int(min(altura_real, ALTURA_MAX)) + 12
                pagina.set_viewport_size({"width": LARGURA, "height": altura})
                pagina.evaluate(f"window.scrollTo(0, {g['top'] - 6})")
                pagina.wait_for_timeout(150)
                desvio = pagina.evaluate(f"window.scrollY - ({g['top'] - 6})")
                if abs(desvio) > 1:
                    raise RuntimeError(f"{nome}: não foi possível rolar até a cena (desvio {desvio}px)")
                pagina.screenshot(path=str(TELAS / nome))
                arquivos.append(nome)
                cortada = " (CORTADA: célula única maior que o limite)" if altura_real > ALTURA_MAX else ""
                print(f"{nome}: {len(g['ids'])} células, {int(altura_real)}px{cortada}")
            cena["imagens"] = arquivos
        nav.close()
    (GER / "roteiro_cenas.json").write_text(json.dumps(cenas, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main(set(sys.argv[1:]) or None)
