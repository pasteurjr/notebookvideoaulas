"""Gera roteiro_video.md e roteiro_video.html a partir de roteiro.json.

Uso:  python gerar_roteiro.py
Depois, para o PDF:  python html_para_pdf.py   (precisa do Playwright)
"""
import base64
import html
import io
import json
from pathlib import Path

import mistune
from PIL import Image

PASTA = Path(__file__).parent
PALAVRAS_POR_SEGUNDO = 150 / 60   # ritmo de narração (~150 palavras/min)
PAUSA_POR_CENA = 1                # segundos

roteiro = json.loads((PASTA / "roteiro.json").read_text(encoding="utf-8"))

# --- tempos de cada cena ---
inicio = 0
for cena in roteiro["cenas"]:
    cena["duracao_s"] = round(len(cena["narracao"].split()) / PALAVRAS_POR_SEGUNDO + PAUSA_POR_CENA)
    cena["inicio_s"] = inicio
    inicio += cena["duracao_s"]
roteiro["duracao_total_s"] = inicio
(PASTA / "roteiro.json").write_text(json.dumps(roteiro, ensure_ascii=False, indent=2), encoding="utf-8")

mmss = lambda s: f"{s // 60}:{s % 60:02d}"
palavras = sum(len(c["narracao"].split()) for c in roteiro["cenas"])
total = roteiro["duracao_total_s"]

cabecalho = f"""# Roteiro do vídeo: {roteiro['titulo']}

| Item | Detalhe |
|---|---|
| **Notebook** | `pipeline_de_agentes.ipynb` (executado, com todas as saídas) |
| **Cenas** | {len(roteiro['cenas'])}, cada uma com uma tela capturada do Jupyter (1920×1080, pasta `telas/`) |
| **Narração** | {palavras} palavras, em tom de aula |
| **Duração estimada** | **{total // 60} min {total % 60:02d} s** (~150 palavras/min + {PAUSA_POR_CENA} s de pausa por cena) |
| **Fonte para montar o vídeo** | `roteiro.json` (tela, narração, início e duração de cada cena) |
| **Revisão** | Todas as telas foram conferidas contra a narração (números, nomes e trechos citados) |

"""

cenas_md = []
for i, c in enumerate(roteiro["cenas"], 1):
    cenas_md.append(
        f"### Cena {i:02d}: {c['titulo']}\n\n"
        f"`{c['tela']}` · {mmss(c['inicio_s'])} → {mmss(c['inicio_s'] + c['duracao_s'])} ({c['duracao_s']} s)\n\n"
        f"**Na tela:** {c['destaque']}\n\n"
        f"> {c['narracao']}\n"
    )

markdown = cabecalho + "\n---\n\n## Roteiro cena a cena\n\n" + "\n".join(cenas_md)
(PASTA / "roteiro_video.md").write_text(markdown, encoding="utf-8")

# --- versão HTML (base do PDF), com as telas embutidas ---
def imagem_base64(caminho):
    img = Image.open(PASTA / caminho).convert("RGB")
    img.thumbnail((1400, 1400))
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=82)
    return base64.b64encode(buf.getvalue()).decode()

cenas_html = []
for i, c in enumerate(roteiro["cenas"], 1):
    cenas_html.append(f"""
<section class="cena">
  <div class="cena-topo"><span class="num">Cena {i:02d}</span> <span class="tit">{html.escape(c['titulo'])}</span>
    <span class="tempo">{mmss(c['inicio_s'])} → {mmss(c['inicio_s'] + c['duracao_s'])} · {c['duracao_s']} s</span></div>
  <img src="data:image/jpeg;base64,{imagem_base64(c['tela'])}" alt="{html.escape(c['tela'])}">
  <p class="destaque"><b>Na tela:</b> {html.escape(c['destaque'])} <code>{html.escape(c['tela'])}</code></p>
  <p class="narracao">{html.escape(c['narracao'])}</p>
</section>""")

render = mistune.create_markdown(plugins=["table"])
pagina = f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><title>Roteiro do vídeo: Pipeline de Agentes</title>
<style>
  @page {{ size: A4; margin: 16mm 14mm; }}
  body {{ font-family: "DejaVu Sans", Arial, sans-serif; font-size: 10.5pt; color: #1d1d1f; line-height: 1.45; }}
  h1 {{ font-size: 19pt; margin: 0 0 10px; }}
  h2 {{ font-size: 14.5pt; margin: 22px 0 8px; border-bottom: 2px solid #e4e4e7; padding-bottom: 4px; }}
  h3 {{ font-size: 12pt; margin: 16px 0 6px; }}
  table {{ border-collapse: collapse; width: 100%; margin: 8px 0; font-size: 9.5pt; }}
  th, td {{ border: 1px solid #d4d4d8; padding: 5px 7px; text-align: left; vertical-align: top; }}
  th {{ background: #f4f4f5; }}
  pre {{ background: #f4f4f5; padding: 8px 10px; border-radius: 6px; font-size: 8.8pt; white-space: pre-wrap; page-break-inside: avoid; }}
  code {{ font-family: "DejaVu Sans Mono", monospace; font-size: 8.8pt; background: #f4f4f5; padding: 0 3px; border-radius: 3px; }}
  pre code {{ background: none; padding: 0; }}
  blockquote {{ margin: 8px 0; padding: 6px 12px; border-left: 4px solid #a1a1aa; background: #fafafa; }}
  .quebra {{ page-break-before: always; }}
  .cena {{ page-break-inside: avoid; margin: 0 0 12px; padding-bottom: 10px; border-bottom: 1px solid #e4e4e7; }}
  .cena-topo {{ display: flex; gap: 10px; align-items: baseline; margin-bottom: 6px; }}
  .num {{ background: #1d4ed8; color: #fff; font-weight: bold; padding: 1px 8px; border-radius: 4px; font-size: 9.5pt; }}
  .tit {{ font-weight: bold; font-size: 11.5pt; flex: 1; }}
  .tempo {{ color: #52525b; font-size: 9.5pt; }}
  .cena img {{ display: block; width: 84%; margin: 0 auto; border: 1px solid #d4d4d8; border-radius: 4px; }}
  .destaque {{ color: #3f3f46; font-size: 9.5pt; margin: 6px 0 4px; }}
  .narracao {{ font-size: 11pt; margin: 4px 0 0; padding: 8px 12px; background: #eff6ff; border-radius: 6px; }}
</style></head><body>
{render(cabecalho)}
<h2>Roteiro cena a cena</h2>
{''.join(cenas_html)}
</body></html>"""
(PASTA / "roteiro_video.html").write_text(pagina, encoding="utf-8")
print(f"{len(roteiro['cenas'])} cenas | {palavras} palavras | {total // 60} min {total % 60:02d} s")
