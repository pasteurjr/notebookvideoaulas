"""Roteiro do vídeo: prepara a lista de cenas e gera roteiro.md e roteiro.pdf.

Uso:
  python gerar_roteiro.py cenas    -> grava _geracao/roteiro_cenas.json (entrada de capturar_telas.py)
  python gerar_roteiro.py roteiro  -> grava roteiro_v2/roteiro_v2.md, roteiro_v2.pdf e cenas_video.json
"""
import json
import sys
from pathlib import Path

import markdown
from PIL import Image
from playwright.sync_api import sync_playwright

NOTE = Path("/mnt/data1/progpython/notebooksvideoaulas/NoteLLM")
GER = NOTE / "_geracao"
ROT = NOTE / "roteiro_v2"
PALAVRAS_POR_SEGUNDO = 2.5   # ritmo de narração calmo (~150 palavras por minuto)

CAPITULOS = {
    2: "Trabalhando com dados de texto",
    3: "Mecanismos de atenção",
    4: "Montando o modelo GPT",
    5: "Pré-treinamento",
    6: "Fine-tuning para classificação",
    7: "Fine-tuning com instruções",
}

ABERTURA = {
    "capitulo": 0, "titulo": "Abertura", "celulas": ["abertura"],
    "narracao": "Nesta aula vamos construir, passo a passo, um modelo de linguagem do tipo GPT, o mesmo tipo de "
                "tecnologia por trás do ChatGPT. Vamos percorrer um único notebook: do texto bruto até um modelo "
                "que segue instruções, passando pela atenção, pela arquitetura transformer, pelo pré-treino e pelo fine-tuning.",
}
ENCERRAMENTO = {
    "capitulo": 99, "titulo": "Encerramento", "celulas": ["encerramento"],
    "narracao": "E assim fechamos o ciclo completo: tokenização, atenção, arquitetura, pré-treino e dois tipos de "
                "fine-tuning. É o mesmo caminho usado pelos grandes modelos de linguagem, só que em escala muito maior. "
                "O notebook está pronto para você executar no Google Colab e explorar cada etapa.",
}


def preparar_cenas():
    cenas = [ABERTURA] + json.loads((GER / "cenas.json").read_text()) + [ENCERRAMENTO]
    # Narrações revisadas contra as telas (chave = número original da cena); algumas cenas saem do vídeo
    revisoes = json.loads((GER / "narracoes_revisadas.json").read_text())
    finais = []
    for n_original, c in enumerate(cenas, 1):
        r = revisoes.get(str(n_original), {})
        if r.get("remover"):
            continue
        c.update({k: r[k] for k in ("titulo", "na_tela", "narracao", "narracao_por_tela") if k in r})
        finais.append(c)
    cenas = finais
    for n, c in enumerate(cenas, 1):
        c["numero"] = n
        c["arquivo"] = f"cena_{n:02d}.png"
    (GER / "roteiro_cenas.json").write_text(json.dumps(cenas, ensure_ascii=False, indent=1))
    total = sum(len(c["narracao"].split()) for c in cenas)
    print(f"{len(cenas)} cenas, {total} palavras, ~{total / PALAVRAS_POR_SEGUNDO / 60:.1f} min de narração")


def mmss(seg):
    return f"{int(seg // 60):02d}:{int(seg % 60):02d}"


def gerar_roteiro():
    cenas = json.loads((GER / "roteiro_cenas.json").read_text())
    duracoes = [max(8, round(len(c["narracao"].split()) / PALAVRAS_POR_SEGUNDO)) for c in cenas]
    total = sum(duracoes)

    linhas = [
        "# Roteiro do vídeo (versão 2) — Construindo um Transformer (LLM) do zero",
        "",
        f"**Notebook:** `Transformer.ipynb` · **Cenas:** {len(cenas)} · **Duração estimada:** {mmss(total)} "
        f"(narração a ~150 palavras por minuto)",
        "",
        "Cada cena traz a captura de tela do notebook (texto explicativo, nota em português, código e saída) "
        "e o texto que o narrador deve ler. O tempo de cada cena é uma estimativa a partir do tamanho da narração.",
        "",
        "## Sumário",
        "",
        "| # | Início | Capítulo | Cena | Duração |",
        "|---|---|---|---|---|",
    ]
    t = 0
    for c, d in zip(cenas, duracoes):
        cap = CAPITULOS.get(c["capitulo"], "—")
        linhas.append(f"| {c['numero']} | {mmss(t)} | {cap} | {c['titulo']} | {d}s |")
        t += d
    linhas.append("")

    t = 0
    cap_atual = None
    manifesto = []
    for c, d in zip(cenas, duracoes):
        if c["capitulo"] in CAPITULOS and c["capitulo"] != cap_atual:
            cap_atual = c["capitulo"]
            linhas += [f"## Capítulo {cap_atual} — {CAPITULOS[cap_atual]}", ""]
        elif c["capitulo"] not in CAPITULOS:
            linhas += [f"## {c['titulo']}", ""]
        imagens = c.get("imagens") or [c["arquivo"]]
        partes = c.get("narracao_por_tela") or [c["narracao"]]
        if len(imagens) > 1 and len(partes) != len(imagens):
            raise ValueError(f"cena {c['numero']}: {len(imagens)} telas, mas {len(partes)} trechos de narração")
        linhas += [
            f"### Cena {c['numero']} — {c['titulo']}",
            "",
            f"*{mmss(t)} → {mmss(t + d)} · {d} segundos"
            + (f" · {len(imagens)} telas em sequência*" if len(imagens) > 1 else "*"),
            "",
        ]
        if c.get("na_tela"):
            linhas += [f"**📺 Na tela:** {c['na_tela']}", ""]
        telas_video = []
        inicio_tela = t
        for k, img in enumerate(imagens):
            letra = chr(ord("A") + k)
            largura, altura = Image.open(ROT / "telas" / img).size
            rolagem = altura / largura > 9 / 16
            trecho = partes[k] if len(imagens) > 1 else c["narracao"]
            seg = round(d * len(trecho.split()) / len(c["narracao"].split())) if len(imagens) > 1 else d
            if len(imagens) > 1:
                linhas += [f"**Tela {letra}** · {mmss(inicio_tela)} → {mmss(inicio_tela + seg)}", ""]
            linhas += [f"![Cena {c['numero']}{' — tela ' + letra if len(imagens) > 1 else ''}](telas/{img})", ""]
            if rolagem:
                linhas += ["*Tela mais alta que o quadro 16:9: rolar de cima para baixo durante a narração.*", ""]
            if len(imagens) > 1:
                linhas += [f"**🎙️ Narração (tela {letra}):** {trecho}", ""]
            telas_video.append({"arquivo": f"telas/{img}", "largura": largura, "altura": altura,
                                "rolagem_vertical": rolagem, "narracao": trecho,
                                "inicio_s": inicio_tela, "duracao_s": seg})
            inicio_tela += seg
        if len(imagens) == 1:
            linhas += [f"**🎙️ Narração:** {c['narracao']}", ""]
        manifesto.append({"cena": c["numero"], "titulo": c["titulo"],
                          "capitulo": c["capitulo"] if c["capitulo"] in CAPITULOS else None,
                          "inicio_s": t, "duracao_s": d, "na_tela": c.get("na_tela", ""),
                          "narracao": c["narracao"], "telas": telas_video})
        t += d

    md_texto = "\n".join(linhas)
    (ROT / "roteiro_v2.md").write_text(md_texto, encoding="utf-8")
    # Arquivo para a geração do vídeo: uma entrada por cena, com as telas, os trechos de narração e os tempos
    (ROT / "cenas_video.json").write_text(json.dumps(
        {"duracao_total_s": total, "palavras_por_minuto": round(PALAVRAS_POR_SEGUNDO * 60),
         "formato_sugerido": "1920x1080 (16:9)", "cenas": manifesto}, ensure_ascii=False, indent=1))

    corpo = markdown.markdown(md_texto, extensions=["tables"])
    html = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<style>
  @page {{ size: A4; margin: 16mm 14mm; }}
  body {{ font-family: "DejaVu Sans", Arial, sans-serif; font-size: 11pt; color: #1f2328; line-height: 1.45; }}
  h1 {{ font-size: 20pt; border-bottom: 3px solid #1a7f37; padding-bottom: 6px; }}
  h2 {{ font-size: 15pt; color: #1a7f37; margin-top: 18px; break-after: avoid; }}
  h3 {{ font-size: 12.5pt; margin: 14px 0 2px; break-after: avoid; }}
  table {{ border-collapse: collapse; width: 100%; font-size: 9.5pt; }}
  th, td {{ border: 1px solid #d0d7de; padding: 3px 6px; text-align: left; }}
  th {{ background: #f6f8fa; }}
  img {{ max-width: 100%; max-height: 175mm; display: block; margin: 6px auto;
        border: 1px solid #d0d7de; break-inside: avoid; }}
  p:has(img) {{ break-inside: avoid; }}
  p:has(> strong:only-child), p:has(> em:only-child) {{ break-after: avoid; page-break-after: avoid; }}
  p strong:first-child {{ color: #1a7f37; }}
</style></head><body>{corpo}</body></html>"""
    html_path = ROT / "roteiro_pdf.html"
    html_path.write_text(html, encoding="utf-8")
    with sync_playwright() as p:
        nav = p.chromium.launch()
        pag = nav.new_page()
        pag.goto(html_path.as_uri())
        pag.wait_for_load_state("networkidle")
        pag.pdf(path=str(ROT / "roteiro_v2.pdf"), format="A4", print_background=True,
                margin={"top": "16mm", "bottom": "16mm", "left": "14mm", "right": "14mm"})
        nav.close()
    html_path.unlink()
    print(f"roteiro_v2.md e roteiro_v2.pdf gravados; {len(cenas)} cenas, duração estimada {mmss(total)}")


if __name__ == "__main__":
    {"cenas": preparar_cenas, "roteiro": gerar_roteiro}[sys.argv[1]]()
