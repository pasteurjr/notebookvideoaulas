"""Monta NoteLLM/Transformer.ipynb a partir dos notebooks executados dos capítulos 2 a 7.

- Copia todas as células (código e saídas) exatamente como estão nos notebooks originais.
- Troca o texto markdown pela tradução em português (_geracao/traducao/capNN_pt.json).
- Embute as figuras do livro (imagens/*.png) como base64 dentro das células.
- Insere antes de cada célula de código uma nota curta em português.
- Acrescenta uma seção de preparação que grava os módulos auxiliares, para rodar no Colab.
"""
import base64
import json
import re
from pathlib import Path

import nbformat

PROG = Path("/media/pasteurjr/hd4t/progpython")
NOTE = PROG / "NoteLLM"
GER = NOTE / "_geracao"

A = PROG / "LLMs-from-scratch"
B = PROG / "llmfromscratch2/LLMs-from-scratch"
C = PROG / "LLMSFROMSCRATCH3/LLMs-from-scratch"

FONTES = {
    2: A / "ch02/01_main-chapter-code/ch02.ipynb",
    3: A / "ch03/01_main-chapter-code/ch03.ipynb",
    4: A / "ch04/01_main-chapter-code/ch04.ipynb",
    5: A / "ch05/01_main-chapter-code/ch05.ipynb",
    6: B / "ch06/01_main-chapter-code/ch06.ipynb",
    7: C / "ch07/01_main-chapter-code/ch07.ipynb",
}

# Módulos auxiliares: cada capítulo importa a versão de previous_chapters.py que acompanhava aquele capítulo
MODULOS = {
    "previous_chapters_cap04.py": (A / "ch04/01_main-chapter-code/previous_chapters.py",
                                   "Código do capítulo 3 usado no capítulo 4"),
    "previous_chapters_cap05.py": (A / "ch05/01_main-chapter-code/previous_chapters.py",
                                   "Código dos capítulos 2 a 4 usado no capítulo 5"),
    "previous_chapters_cap06.py": (B / "ch06/01_main-chapter-code/previous_chapters.py",
                                   "Código dos capítulos 2 a 5 usado no capítulo 6"),
    "previous_chapters_cap07.py": (C / "ch07/01_main-chapter-code/previous_chapters.py",
                                   "Código dos capítulos 2 a 6 usado no capítulo 7"),
    "gpt_download.py": (C / "ch07/01_main-chapter-code/gpt_download.py",
                        "Download dos pesos oficiais do GPT-2 (OpenAI)"),
}

TITULOS = {
    2: "Capítulo 2 — Trabalhando com dados de texto",
    3: "Capítulo 3 — Implementando mecanismos de atenção",
    4: "Capítulo 4 — Implementando um modelo GPT do zero",
    5: "Capítulo 5 — Pré-treinamento com dados não rotulados",
    6: "Capítulo 6 — Fine-tuning para classificação de texto",
    7: "Capítulo 7 — Fine-tuning para seguir instruções",
}

manifest = json.loads((GER / "imagens_manifest.json").read_text())
largura_por_arquivo = {m["file"]: max(m["width_attr"]) for m in manifest.values()}


def img_html(nome):
    b64 = base64.b64encode((NOTE / "imagens" / nome).read_bytes()).decode()
    return f'<img src="data:image/png;base64,{b64}" width="{largura_por_arquivo[nome]}">'


def md(texto, cid, **meta):
    c = nbformat.v4.new_markdown_cell(texto)
    c.id = cid
    c.metadata.update(meta)
    return c


def code(texto, cid, **meta):
    c = nbformat.v4.new_code_cell(texto)
    c.id = cid
    c.metadata.update(meta)
    return c


# Caracteres digitados por acidente no notebook do cap. 5 depois da execução (as saídas estão corretas).
# Restaura o texto do livro. Mantém c05-141 com gpt.to("cpu"), correção intencional do professor.
CORRECOES = {
    "c05-076": [("        ) ,.\n", "        )\n"), ("idx=encoded,..\n", "idx=encoded,\n")],
    "c05-091": [("print(inverse_vocab[next_token_id]) I", "print(inverse_vocab[next_token_id])")],
    "c05-129": [("contained in this folder '", "contained in this folder")],
}
CELULAS_VAZIAS = {"c02-005", "c02-140"}   # células de código vazias, sem saída


def ajustar_codigo(src, cap, cid):
    for antigo, novo in CORRECOES.get(cid, []):
        assert antigo in src, (cid, antigo)
        src = src.replace(antigo, novo)
    src = re.sub(r"\bfrom previous_chapters import", f"from suporte.previous_chapters_cap{cap:02d} import", src)
    src = re.sub(r"\bfrom gpt_download import", "from suporte.gpt_download import", src)
    return src


def nota(texto, cid):
    return md(f"> 🇧🇷 **O que esta célula faz:** {texto}", cid, nota_pt=True)


celulas = []

# ------------------------------------------------------------------ abertura
celulas.append(md("""# Transformer — construindo um LLM do zero

O objetivo deste notebook é desenvolver, desde o início e passo a passo, um **transformer**: a arquitetura por trás
dos modelos de linguagem do tipo GPT. Partimos de texto puro e chegamos a um modelo que gera texto, classifica
mensagens e segue instruções.

| Capítulo | O que se constrói |
|---|---|
| 2 | Tokenização do texto, embeddings e o carregador de dados |
| 3 | O mecanismo de **atenção**: self-attention, máscara causal e multi-head |
| 4 | A arquitetura **GPT** completa: LayerNorm, GELU, bloco transformer e o modelo |
| 5 | **Pré-treinamento**, avaliação e carregamento dos pesos oficiais do GPT-2 |
| 6 | **Fine-tuning** para classificar mensagens como spam |
| 7 | **Fine-tuning com instruções**, transformando o modelo em um assistente |

Antes de cada célula de código há uma nota em português (🇧🇷) dizendo, em poucas palavras, o que ela faz.""", "abertura"))

# ------------------------------------------------------------------ instruções de execução (Colab + Google Drive)
URL_RAW = "https://raw.githubusercontent.com/rasbt/LLMs-from-scratch/main"
URL_GPT2 = "https://openaipublic.blob.core.windows.net/gpt-2/models"
URL_SPAM = "https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip"

celulas.append(md(f"""## Como executar este notebook no Google Colab, com o Google Drive

O notebook foi preparado para rodar no **Google Colab**, guardando no **Google Drive** o próprio notebook, os dados
baixados e os modelos treinados. Assim nada se perde quando a sessão do Colab termina.

### 1. O que é preciso

- Uma conta Google, com acesso ao [Google Drive](https://drive.google.com) e ao [Google Colab](https://colab.research.google.com).
- Cerca de **8 GB livres no Google Drive** (a conta gratuita tem 15 GB). As tabelas do passo 6 mostram o que ocupa esse espaço.

### 2. Salvar o notebook no Google Drive

1. Abra o [Google Drive](https://drive.google.com).
2. Em **Meu Drive**, crie uma pasta chamada **`Transformer`**: botão **+ Novo → Nova pasta**.
3. Entre na pasta e envie o arquivo **`Transformer.ipynb`**: botão **+ Novo → Upload de arquivo**.

### 3. Abrir o notebook no Colab

1. No Drive, clique com o botão direito em `Transformer.ipynb` → **Abrir com → Google Colaboratory**.
2. Se o Colab não aparecer na lista: **Abrir com → Conectar mais apps**, procure **Colaboratory**, instale e repita o passo anterior.
3. Outra forma: em [colab.research.google.com](https://colab.research.google.com), menu **Arquivo → Abrir notebook → Google Drive**
   e escolha `Meu Drive/Transformer/Transformer.ipynb`.

As alterações feitas no Colab são salvas automaticamente no mesmo arquivo do Drive.

### 4. Ativar a GPU

Menu **Ambiente de execução → Alterar o tipo de ambiente de execução → Acelerador de hardware: GPU T4 → Salvar**.
Sem GPU o notebook funciona, mas os treinos dos capítulos 5, 6 e 7 ficam muito lentos.

### 5. Conectar o Google Drive

Execute a célula **Conectar o Google Drive**, logo abaixo. O Colab pede autorização para acessar o seu Drive: aceite.
A partir daí, a pasta de trabalho passa a ser `Meu Drive/Transformer`, e tudo o que o notebook baixar ou gravar fica nela.
A célula também informa se a GPU está ativa.

### 6. Preparar o ambiente e baixar os arquivos

1. Execute as células da seção **Preparação do ambiente**: elas instalam o `tiktoken` e gravam na pasta `suporte/`
   os módulos com o código que cada capítulo reaproveita dos anteriores.
2. Opcional: execute a célula **Baixar todos os arquivos de uma vez**. Se preferir pular, não há problema: cada capítulo
   baixa sozinho o que precisa, na primeira vez em que é executado.

Arquivos baixados da internet (ficam na pasta `Transformer` do Drive):

| Arquivo ou pasta | Usado no | Origem | Tamanho |
|---|---|---|---|
| `the-verdict.txt` | cap. 2 e 5 | [{URL_RAW}/ch02/01_main-chapter-code/the-verdict.txt]({URL_RAW}/ch02/01_main-chapter-code/the-verdict.txt) | 20 KB |
| `gpt2/124M/` (7 arquivos) | cap. 5 e 6 | [{URL_GPT2}/124M/]({URL_GPT2}/124M/checkpoint) | 477 MB |
| `sms_spam_collection/` | cap. 6 | [{URL_SPAM}]({URL_SPAM}) | 200 KB |
| `instruction-data.json` | cap. 7 | [{URL_RAW}/ch07/01_main-chapter-code/instruction-data.json]({URL_RAW}/ch07/01_main-chapter-code/instruction-data.json) | 200 KB |
| `gpt2/355M/` (7 arquivos) | cap. 7 | [{URL_GPT2}/355M/]({URL_GPT2}/355M/checkpoint) | 1,4 GB |

Os 7 arquivos de cada pasta `gpt2/…` são: `checkpoint`, `encoder.json`, `hparams.json`, `model.ckpt.data-00000-of-00001`,
`model.ckpt.index`, `model.ckpt.meta` e `vocab.bpe`.

Arquivos gravados pelo próprio notebook durante a execução:

| Arquivo | Capítulo | Tamanho aproximado |
|---|---|---|
| `model.pth` e `model_and_optimizer.pth` | 5 | 650 MB e 1,9 GB |
| `train.csv`, `validation.csv`, `test.csv` e `review_classifier.pth` | 6 | 160 KB e 550 MB |
| `gpt2-medium355M-sft.pth` e `instruction-data-with-response.json` | 7 | 1,7 GB e 30 KB |
| gráficos `.pdf` (`loss-plot.pdf`, `accuracy-plot.pdf` etc.) | 5, 6 e 7 | poucos KB |

### 7. Executar

Execute os capítulos **em ordem**, célula por célula (**Shift + Enter**), ou use **Ambiente de execução → Executar tudo**.

### Dicas

- **Se a sessão cair** (o Colab gratuito desconecta depois de um tempo sem uso ou de algumas horas): os arquivos continuam no Drive.
  Reabra o notebook, execute de novo **Conectar o Google Drive** e a **Preparação do ambiente** e recomece do **início do capítulo**
  em que parou. Cada capítulo pode ser executado sem os anteriores, porque importa da pasta `suporte/` o que precisa.
- **Sem Google Drive:** pule a célula do Drive. Os arquivos ficam em `/content`, que é apagado quando a sessão termina.
- **Seção 7.8 (avaliação com o Llama 3):** precisa do [Ollama](https://ollama.com) instalado e rodando no computador local.
  No Colab essas células não funcionam; pule-as.
- **Saídas que já aparecem nas células:** vêm de uma execução completa feita numa GPU NVIDIA RTX 3060. Ao executar de novo,
  os números podem variar um pouco.
- **No computador local (Jupyter):** pule a célula do Drive; os arquivos ficam na pasta do notebook. É preciso ter Python com
  `torch`, `tiktoken`, `tensorflow`, `matplotlib`, `pandas`, `numpy`, `tqdm`, `requests` e `psutil`.""", "instrucoes"))

celulas.append(nota("Conecta o Google Drive e passa a usar a pasta `Meu Drive/Transformer` como pasta de trabalho; "
                    "fora do Colab, usa a pasta atual. Também informa se há GPU disponível.", "drive-pt"))
celulas.append(code("""#@title Conectar o Google Drive
import os
import torch

PASTA_NO_DRIVE = "/content/drive/MyDrive/Transformer"

try:
    from google.colab import drive
    drive.mount("/content/drive")
    os.makedirs(PASTA_NO_DRIVE, exist_ok=True)
    os.chdir(PASTA_NO_DRIVE)
except ImportError:
    print("Fora do Google Colab: os arquivos ficam na pasta atual.")

print("Pasta de trabalho:", os.getcwd())
print("GPU:", torch.cuda.get_device_name(0) if torch.cuda.is_available()
      else "nenhuma (no Colab: Ambiente de execução → Alterar o tipo de ambiente de execução → GPU T4)")""",
                    "drive", cellView="form"))

# ------------------------------------------------------------------ preparação
celulas.append(md("""## Preparação do ambiente

As células abaixo deixam o notebook pronto para rodar em qualquer lugar, inclusive no Google Colab:

- instalam a biblioteca `tiktoken` (o tokenizador usado pelo GPT-2);
- baixam o conto *The Verdict*, o texto usado para treinar o modelo;
- gravam na pasta `suporte/` os módulos auxiliares. Cada capítulo importa dali o código construído nos capítulos anteriores.

No Colab, as células de gravação dos módulos aparecem recolhidas; basta executá-las.""", "prep-md"))

celulas.append(nota("Instala o tokenizador `tiktoken` e confere as versões das bibliotecas principais.", "prep-pip-pt"))
celulas.append(code("""%pip install -q tiktoken

from importlib.metadata import version
for pacote in ["torch", "tiktoken", "tensorflow", "matplotlib", "pandas", "numpy"]:
    try:
        print(f"{pacote}: {version(pacote)}")
    except Exception:
        print(f"{pacote}: NÃO INSTALADO")""", "prep-pip"))

celulas.append(nota("Baixa o conto *The Verdict*, que será o texto de treino, caso ele ainda não esteja na pasta.", "prep-verdict-pt"))
celulas.append(code("""import os
import urllib.request

if not os.path.exists("the-verdict.txt"):
    url = "https://raw.githubusercontent.com/rasbt/LLMs-from-scratch/main/ch02/01_main-chapter-code/the-verdict.txt"
    urllib.request.urlretrieve(url, "the-verdict.txt")
print("the-verdict.txt:", os.path.getsize("the-verdict.txt"), "bytes")""", "prep-verdict"))

for i, (nome, (origem, descricao)) in enumerate(MODULOS.items(), 1):
    fonte = origem.read_text(encoding="utf-8")
    assert "'''" not in fonte
    celulas.append(nota(f"Grava o módulo auxiliar `suporte/{nome}`: {descricao.lower()}.", f"prep-mod{i}-pt"))
    celulas.append(code(
        f"#@title {descricao} → suporte/{nome}\n"
        "import os\n"
        "os.makedirs(\"suporte\", exist_ok=True)\n"
        "open(\"suporte/__init__.py\", \"a\").close()\n\n"
        f"codigo = r'''{fonte}'''\n\n"
        f"with open(\"suporte/{nome}\", \"w\", encoding=\"utf-8\") as f:\n"
        "    f.write(codigo)\n"
        f"print(\"Gravado: suporte/{nome}\")",
        f"prep-mod{i}", cellView="form"))

celulas.append(nota("Opcional: baixa de uma vez todos os dados e os pesos do GPT-2 usados nos capítulos 5 a 7 "
                    "(cerca de 1,9 GB). Arquivos que já existem na pasta são pulados.", "prep-baixar-pt"))
celulas.append(code(f"""#@title Baixar todos os arquivos de uma vez (opcional)
import os
import urllib.request
import zipfile


def baixar(url, destino):
    if os.path.exists(destino) and os.path.getsize(destino) > 0:
        print("já existe:", destino)
        return
    os.makedirs(os.path.dirname(destino) or ".", exist_ok=True)
    print("baixando:", destino)
    urllib.request.urlretrieve(url, destino + ".parcial")   # grava com outro nome até terminar
    os.replace(destino + ".parcial", destino)


# Capítulos 2 e 5: o conto usado no treino
baixar("{URL_RAW}/ch02/01_main-chapter-code/the-verdict.txt", "the-verdict.txt")

# Capítulo 6: mensagens SMS rotuladas como spam / não spam
if not os.path.exists("sms_spam_collection/SMSSpamCollection.tsv"):
    baixar("{URL_SPAM}", "sms_spam_collection.zip")
    with zipfile.ZipFile("sms_spam_collection.zip") as z:
        z.extractall("sms_spam_collection")
    os.replace("sms_spam_collection/SMSSpamCollection", "sms_spam_collection/SMSSpamCollection.tsv")
print("dataset de spam: ok")

# Capítulo 7: exemplos de instruções e respostas
baixar("{URL_RAW}/ch07/01_main-chapter-code/instruction-data.json", "instruction-data.json")

# Capítulos 5, 6 e 7: pesos oficiais do GPT-2 (124M e 355M)
ARQUIVOS_GPT2 = ["checkpoint", "encoder.json", "hparams.json", "model.ckpt.data-00000-of-00001",
                 "model.ckpt.index", "model.ckpt.meta", "vocab.bpe"]
for tamanho in ["124M", "355M"]:
    for nome in ARQUIVOS_GPT2:
        baixar(f"{URL_GPT2}/{{tamanho}}/{{nome}}", f"gpt2/{{tamanho}}/{{nome}}")

print("Pronto: todos os arquivos estão em", os.getcwd())""", "prep-baixar", cellView="form"))

# ------------------------------------------------------------------ capítulos
LIMPEZA = """import gc
import torch

# Libera a memória ocupada pelos modelos dos capítulos anteriores
for nome in ["model", "gpt", "optimizer", "checkpoint", "params", "model_state_dict"]:
    globals().pop(nome, None)
gc.collect()
if torch.cuda.is_available():
    torch.cuda.empty_cache()
    print(f"Memória de GPU em uso: {torch.cuda.memory_allocated() / 1e9:.2f} GB")"""

cenas = []
for cap, caminho in FONTES.items():
    origem = json.loads(caminho.read_text())
    trad = json.loads((GER / "traducao" / f"cap{cap:02d}_pt.json").read_text())

    celulas.append(md(f"# {TITULOS[cap]}\n\n{trad['introducao_capitulo'].strip()}", f"cap{cap:02d}-intro", capitulo=cap))
    if cap in (6, 7):
        celulas.append(nota("Libera a memória dos modelos dos capítulos anteriores antes de carregar um modelo novo.",
                            f"cap{cap:02d}-limpeza-pt"))
        celulas.append(code(LIMPEZA, f"cap{cap:02d}-limpeza"))

    for i, c in enumerate(origem["cells"]):
        cid = f"c{cap:02d}-{i:03d}"
        if c["cell_type"] == "markdown":
            texto = trad["markdown"][cid]
            texto = re.sub(r"\{\{IMG:([\w.\-]+)\}\}", lambda m: img_html(m.group(1)), texto)
            celulas.append(md(texto, cid))
        elif c["cell_type"] == "code":
            if cid in CELULAS_VAZIAS:
                assert not "".join(c["source"]).strip() and not c["outputs"], cid
                continue
            celulas.append(nota(trad["notas"][cid], f"{cid}-pt"))
            nova = nbformat.from_dict(c)
            nova.id = cid
            nova.source = ajustar_codigo("".join(c["source"]), cap, cid)
            nova.metadata = {}
            celulas.append(nova)
        else:
            raise ValueError(c["cell_type"])

    for cena in trad["cenas"]:
        cenas.append({"capitulo": cap, **cena})

celulas.append(md("""# Encerramento

Ao longo deste notebook construímos um LLM completo, passo a passo:

1. transformamos texto em tokens e embeddings;
2. implementamos o mecanismo de atenção;
3. montamos a arquitetura GPT;
4. pré-treinamos o modelo e carregamos os pesos oficiais do GPT-2;
5. ajustamos o modelo para classificar spam;
6. ajustamos o modelo para seguir instruções e o avaliamos com outro LLM.

Esse é o mesmo ciclo usado, em escala muito maior, para criar modelos como o ChatGPT.""", "encerramento"))

# Crédito exigido pela licença Apache 2.0 do código original; fica no fim, fora do roteiro do vídeo
celulas.append(md("""---
<small>Créditos: o código deste notebook é baseado no repositório
[LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch), de Sebastian Raschka, distribuído sob a licença Apache 2.0.</small>""",
                  "creditos"))

# ------------------------------------------------------------------ numeração sequencial das execuções
n = 0
for c in celulas:
    if c.cell_type == "code" and c.get("execution_count"):
        n += 1
        c.execution_count = n
        for o in c.outputs:
            if "execution_count" in o:
                o["execution_count"] = n
    elif c.cell_type == "code":
        c.execution_count = None

nb = nbformat.v4.new_notebook()
nb.cells = celulas
nb.metadata = {
    "kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"},
    "language_info": {"name": "python"},
    "accelerator": "GPU",
    "colab": {"provenance": [], "gpuType": "T4", "toc_visible": True},
}
nbformat.validate(nb)
nbformat.write(nb, NOTE / "Transformer.ipynb")
(GER / "cenas.json").write_text(json.dumps(cenas, ensure_ascii=False, indent=1))

print(f"Transformer.ipynb: {len(celulas)} células, "
      f"{sum(c.cell_type == 'code' for c in celulas)} de código, "
      f"{(NOTE / 'Transformer.ipynb').stat().st_size / 1e6:.1f} MB; {len(cenas)} cenas")
