"""Gera o cabeçalho padrão "0. Como rodar este notebook" (markdown + célula de preparação)
usado em todos os notebooks do curso, e o aplica a um notebook.

Uso:
    python ferramentas/cabecalho_colab.py
"""
import json
from pathlib import Path

import nbformat

REPO_URL = "https://github.com/pasteurjr/notebookvideoaulas"
DRIVE_URL = "https://drive.google.com/drive/folders/1mMRjinjohj_jyMsJzO7rxgYKm6unVKze?usp=sharing"
RAIZ = Path(__file__).resolve().parents[1]


def markdown(aula, notebook, usa_dados, usa_gpu, pacotes_pip, secrets):
    colab = f"https://colab.research.google.com/github/pasteurjr/notebookvideoaulas/blob/main/{aula}/{notebook}"
    precisa = []
    precisa.append("imagens/dados da pasta **notebooksvideos** do Google Drive" if usa_dados else "nenhum dado externo (só o código do GitHub)")
    precisa.append("**GPU** (no Colab, a T4 gratuita é suficiente)" if usa_gpu else "não precisa de GPU")
    precisa.append("chaves de API: " + ", ".join(f"`{s}`" for s in secrets) if secrets else "nenhuma chave de API")

    passos = [
        f"**Adicione a pasta de dados do curso ao seu Google Drive** (uma vez só, vale para todas as aulas): abra o link **[notebooksvideos]({DRIVE_URL})**, clique com o botão direito no nome da pasta e escolha **Organizar → Adicionar atalho** (ou **Adicionar atalho ao Drive**) → **Meu Drive**. A pasta passa a aparecer como `MyDrive/notebooksvideos`, sem ocupar o seu espaço.",
        "**Abra este notebook no Colab** pelo botão **Abrir no Colab** acima (ele abre direto do GitHub).",
    ]
    if usa_gpu:
        passos.append("**Ative a GPU gratuita:** **Ambiente de execução → Alterar o tipo de ambiente de execução → GPU T4**.")
    if secrets:
        passos.append("**Guarde as chaves de API nos *Secrets* do Colab:** clique no ícone de **chave (🔑)** na barra lateral esquerda, crie "
                      + " e ".join(f"`{s}`" for s in secrets)
                      + " com as **suas** chaves (com crédito) e ative **Acesso ao notebook** em cada uma. As chaves ficam na sua conta Google, nunca no notebook.")
    passos.append("**Rode a célula de preparação logo abaixo.** Ela clona o repositório do GitHub para o Colab, "
                  + ("monta o seu Google Drive (autorize o acesso) e copia os dados da pasta `notebooksvideos` para a pasta da aula, " if usa_dados else "")
                  + "verifica quais bibliotecas a sessão do Colab já tem e **instala só as que faltarem**"
                  + (", e carrega as chaves dos *Secrets*." if secrets else "."))
    passos.append("Depois: **Ambiente de execução → Executar tudo**. Rodar a célula de preparação de novo não causa problema.")
    passos_md = "\n".join(f"{i}. {p}" for i, p in enumerate(passos, 1))
    pip = " ".join(pacotes_pip)

    return f"""## 0. Como rodar este notebook

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)]({colab})

O curso tem duas partes, usadas por **todos** os notebooks:

| O quê | Onde |
|---|---|
| **Código** (notebooks, arquivos de configuração) | GitHub: **{REPO_URL}** |
| **Dados** (imagens e arquivos grandes) | Google Drive: **[pasta notebooksvideos]({DRIVE_URL})**, com a mesma estrutura de pastas do GitHub |

**Esta aula usa:** {"; ".join(precisa)}.

### Opção A: Google Colab (recomendado, nada para instalar no computador)

{passos_md}

**Se aparecer erro de biblioteca** (`ModuleNotFoundError`, `ImportError` ou erro de versão): crie uma célula nova, rode o comando abaixo, depois vá em **Ambiente de execução → Reiniciar sessão** e rode a célula de preparação de novo.

```
!pip install {pip}
```

### Opção B: no seu computador

Pré-requisito: [Miniconda](https://docs.conda.io/en/latest/miniconda.html) (ou Anaconda) e Git instalados. No terminal:

```bash
git clone {REPO_URL}.git
cd notebookvideoaulas
conda create -n notecursos python=3.12 -y
conda activate notecursos
pip install -r requirements.txt
cd {aula}
jupyter notebook {notebook}
```
""" + (f"""
**Dados:** abra a **[pasta notebooksvideos]({DRIVE_URL})**, entre em `{aula}`, clique com o botão direito na pasta **`dados`** → **Fazer download** e descompacte dentro de `notebookvideoaulas/{aula}/`, para ficar `{aula}/dados/...`.
""" if usa_dados else "") + (f"""
**Chaves:** copie `.env.exemplo` para `.env` e coloque nele as **suas** chaves ({", ".join(f"`{s}`" for s in secrets)}). O `.env` nunca vai para o GitHub.
""" if secrets else "") + """
No computador local, a célula de preparação detecta que não está no Colab e não faz nada."""


def celula(aula, usa_dados, pacotes, secrets, extras_env=None):
    extras = "".join(f'\n    os.environ.setdefault("{k}", "{v}")' for k, v in (extras_env or {}).items())
    return f'''# PREPARAÇÃO DO AMBIENTE NO GOOGLE COLAB (igual em todos os notebooks do curso; no computador local não faz nada)
AULA = "{aula}"                           # pasta desta aula no repositório
USA_DADOS_DO_DRIVE = {usa_dados}                                     # copia os dados da pasta "notebooksvideos" do Drive
PACOTES = {json.dumps(pacotes, ensure_ascii=False)}   # módulo: pacote pip
SECRETS = {json.dumps(secrets)}                                   # chaves lidas dos Secrets do Colab (ícone 🔑)

import os, sys, shutil, subprocess, importlib.util

if "google.colab" in sys.modules:
    # 1) Código: clona o repositório do GitHub para o Colab
    if not os.path.exists("/content/notebookvideoaulas"):
        subprocess.run(["git", "clone", "-q", "https://github.com/pasteurjr/notebookvideoaulas.git",
                        "/content/notebookvideoaulas"], check=True)
    os.chdir(f"/content/notebookvideoaulas/{{AULA}}")

    # 2) Dados: copia da pasta "notebooksvideos" (atalho no Meu Drive) para a pasta da aula
    if USA_DADOS_DO_DRIVE and not os.path.exists("dados"):
        from google.colab import drive
        drive.mount("/content/drive")
        shutil.copytree(f"/content/drive/MyDrive/notebooksvideos/{{AULA}}/dados", "dados")

    # 3) Bibliotecas: instala só as que a sessão do Colab ainda não tem
    faltando = [pip for modulo, pip in PACOTES.items() if importlib.util.find_spec(modulo) is None]
    if faltando:
        print("Instalando:", ", ".join(faltando))
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", *faltando], check=True)
        print("Pronto. Se o Colab pedir 'Reiniciar sessão', reinicie e rode esta célula de novo.")
    else:
        print("Todas as bibliotecas já estão instaladas no Colab.")

    # 4) Chaves de API: vêm dos Secrets do Colab (nunca escreva a chave no notebook)
    if SECRETS:
        from google.colab import userdata
        for chave in SECRETS:
            os.environ[chave] = userdata.get(chave){extras}

    print("Pasta da aula:", os.getcwd())
    print("Conteúdo:", sorted(os.listdir(".")))
else:
    print("Ambiente local detectado: usando a pasta atual.")'''


AULAS = [
    dict(aula="noteagentes/noteaulaagentes", notebook="pipeline_de_agentes.ipynb", usa_dados=False, usa_gpu=False,
         pacotes={"crewai": "crewai==1.15.22", "crewai_tools": "crewai-tools==1.15.22", "dotenv": "python-dotenv", "yaml": "pyyaml"},
         secrets=["DEEPSEEK_API_KEY", "SERPER_API_KEY"], extras_env={"MODELO_LLM": "deepseek/deepseek-v4-flash"}),
    dict(aula="notedeeplearning/aulacovidct", notebook="pipeline_treinamento_covid_ct.ipynb", usa_dados=True, usa_gpu=True,
         pacotes={"tensorflow": "tensorflow", "keras": "keras", "sklearn": "scikit-learn", "matplotlib": "matplotlib", "PIL": "pillow"},
         secrets=[]),
]

if __name__ == "__main__":
    for a in AULAS:
        p = RAIZ / a["aula"] / a["notebook"]
        nb = nbformat.read(p, as_version=4)
        # remove o cabeçalho antigo (células da seção 0 até a seção 1)
        inicio = next(i for i, c in enumerate(nb.cells) if c.cell_type == "markdown" and c.source.startswith("## 0."))
        fim = next(i for i, c in enumerate(nb.cells) if c.cell_type == "markdown" and c.source.startswith("## 1."))
        md = nbformat.v4.new_markdown_cell(markdown(a["aula"], a["notebook"], a["usa_dados"], a["usa_gpu"], list(a["pacotes"].values()), a["secrets"]))
        cod = nbformat.v4.new_code_cell(celula(a["aula"], a["usa_dados"], a["pacotes"], a["secrets"], a.get("extras_env")))
        nb.cells[inicio:fim] = [md, cod]
        nbformat.validate(nb)
        nbformat.write(nb, p)
        print(f"{p.relative_to(RAIZ)}: cabeçalho aplicado (células {inicio}-{fim - 1} → 2 células)")
