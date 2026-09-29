"""Converte roteiro_video.html em roteiro_video.pdf usando o Chromium do Playwright."""
from pathlib import Path
from playwright.sync_api import sync_playwright

PASTA = Path(__file__).parent.resolve()

with sync_playwright() as p:
    navegador = p.chromium.launch()
    pagina = navegador.new_page()
    pagina.goto((PASTA / "roteiro_video.html").as_uri())
    pagina.wait_for_load_state("networkidle")
    pagina.pdf(
        path=str(PASTA / "roteiro_video.pdf"),
        format="A4",
        print_background=True,
        display_header_footer=True,
        header_template="<span></span>",
        footer_template='<div style="font-size:8px;width:100%;text-align:center;color:#71717a">'
                        'Roteiro: Pipeline de Agentes · página <span class="pageNumber"></span>/<span class="totalPages"></span></div>',
        margin={"top": "14mm", "bottom": "16mm", "left": "14mm", "right": "14mm"},
    )
    navegador.close()
print("PDF gerado:", PASTA / "roteiro_video.pdf")
