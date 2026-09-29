# Notebooks das videoaulas

Notebooks em português, explicados célula a célula, usados nas videoaulas do curso.

| Aula | Notebook | Abrir no Colab |
|---|---|---|
| **Pipeline de agentes** (CrewAI): 5 agentes de IA pesquisam um lead na internet, dão uma nota e escrevem um e-mail de vendas | [`noteagentes/noteaulaagentes/pipeline_de_agentes.ipynb`](noteagentes/noteaulaagentes/pipeline_de_agentes.ipynb) | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/pasteurjr/notebookvideoaulas/blob/main/noteagentes/noteaulaagentes/pipeline_de_agentes.ipynb) |
| **Pipeline de treinamento de deep learning**: detecção de COVID-19 em tomografias com transfer learning (VGG16) | [`notedeeplearning/aulacovidct/pipeline_treinamento_covid_ct.ipynb`](notedeeplearning/aulacovidct/pipeline_treinamento_covid_ct.ipynb) | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/pasteurjr/notebookvideoaulas/blob/main/notedeeplearning/aulacovidct/pipeline_treinamento_covid_ct.ipynb) |

**Cada notebook traz, logo no início, a seção "0. Como rodar este notebook"** com o passo a passo para o Google Colab e para o computador local.

## Dados

Os dados (imagens) **não ficam no GitHub**: estão na pasta compartilhada do Google Drive
**[notebooksvideos](https://drive.google.com/drive/folders/1mMRjinjohj_jyMsJzO7rxgYKm6unVKze?usp=sharing)**, com a mesma estrutura de pastas deste repositório.

## Rodando no computador

```bash
git clone https://github.com/pasteurjr/notebookvideoaulas.git
cd notebookvideoaulas
conda create -n notecursos python=3.12 -y
conda activate notecursos
pip install -r requirements.txt
jupyter notebook
```

> **GPU NVIDIA recente (ex.: série RTX 50) e o TensorFlow não encontra a GPU?** Aponte o `LD_LIBRARY_PATH` para as bibliotecas CUDA instaladas pelo pip:
> ```bash
> export LD_LIBRARY_PATH=$(ls -d $CONDA_PREFIX/lib/python3.12/site-packages/nvidia/*/lib | tr '\n' ':')$LD_LIBRARY_PATH
> ```

## Chaves de API

A aula de agentes usa serviços pagos (DeepSeek e Serper). **Cada aluno usa as próprias chaves**, guardadas nos *Secrets* do Colab ou num arquivo `.env` local (modelo em `.env.exemplo`). **Nunca** coloque chaves nos notebooks nem envie o `.env` para o GitHub.

> ⚠️ O modelo de detecção de COVID-19 é **apenas didático** e não serve para diagnóstico médico.
