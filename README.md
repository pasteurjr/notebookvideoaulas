# Curso Engenharia de IA com SDD

Cada pasta é uma aula, na ordem do curso, com o **notebook** (na versão mostrada no vídeo da aula) e os arquivos que ele usa.
Os **vídeos**, os **roteiros** e os **dados** grandes ficam no Google Drive do curso: [pasta notebooksvideos](https://drive.google.com/drive/folders/1mMRjinjohj_jyMsJzO7rxgYKm6unVKze?usp=sharing),
com a mesma estrutura de pastas. As aulas 09 a 11 são demonstrações de aplicações: só vídeo e roteiro, no Drive.

| # | Aula | Notebook | Dados |
|---|---|---|---|
| 01 | Pipeline de machine learning (câncer de mama, Wisconsin) | [`01_pipeline_machine_learning/notebook/exalgint3.ipynb`](01_pipeline_machine_learning/notebook/exalgint3.ipynb) [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/pasteurjr/notebookvideoaulas/blob/main/01_pipeline_machine_learning/notebook/exalgint3.ipynb) | upload do `bcw.csv` |
| 02 | IA na medicina: infectologia | [`02_ia_na_medicina/notebook/ia_na_medicina_infectologia.ipynb`](02_ia_na_medicina/notebook/ia_na_medicina_infectologia.ipynb) [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/pasteurjr/notebookvideoaulas/blob/main/02_ia_na_medicina/notebook/ia_na_medicina_infectologia.ipynb) | Google Drive |
| 03 | Deep learning com transfer learning: COVID-19 em tomografia (VGG16) | [`03_deep_learning_covid_ct/notebook/pipeline_treinamento_covid_ct.ipynb`](03_deep_learning_covid_ct/notebook/pipeline_treinamento_covid_ct.ipynb) [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/pasteurjr/notebookvideoaulas/blob/main/03_deep_learning_covid_ct/notebook/pipeline_treinamento_covid_ct.ipynb) | Google Drive |
| 04 | Transformer: construindo um LLM do zero | [`04_transformer_llm_do_zero/notebook/Transformer.ipynb`](04_transformer_llm_do_zero/notebook/Transformer.ipynb) [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/pasteurjr/notebookvideoaulas/blob/main/04_transformer_llm_do_zero/notebook/Transformer.ipynb) | Google Drive |
| 05 | Agentes com CrewAI: pipeline de agentes | [`05_agentes_crewai/notebook/pipeline_de_agentes.ipynb`](05_agentes_crewai/notebook/pipeline_de_agentes.ipynb) [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/pasteurjr/notebookvideoaulas/blob/main/05_agentes_crewai/notebook/pipeline_de_agentes.ipynb) | no repositório |
| 06 | Agentes com AutoGen: residente e infectologista revisam pareceres da CCIH | [`06_agentes_autogen/notebook/agentes_autogen_v2_parecer_ccih.ipynb`](06_agentes_autogen/notebook/agentes_autogen_v2_parecer_ccih.ipynb) [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/pasteurjr/notebookvideoaulas/blob/main/06_agentes_autogen/notebook/agentes_autogen_v2_parecer_ccih.ipynb) | no repositório |
| 07 | RAG: assistente de controle de infecção hospitalar | [`07_rag/notebook/rag_infeccao_hospitalar.ipynb`](07_rag/notebook/rag_infeccao_hospitalar.ipynb) [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/pasteurjr/notebookvideoaulas/blob/main/07_rag/notebook/rag_infeccao_hospitalar.ipynb) | no repositório |
| 08 | Fine-tuning com LoRA e QLoRA (Llama-2-7b, infecção hospitalar) | [`08_fine_tuning_lora/notebook/finetuning_lora_infeccao_hospitalar_v3.ipynb`](08_fine_tuning_lora/notebook/finetuning_lora_infeccao_hospitalar_v3.ipynb) [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/pasteurjr/notebookvideoaulas/blob/main/08_fine_tuning_lora/notebook/finetuning_lora_infeccao_hospitalar_v3.ipynb) | no repositório |

## Como rodar os notebooks

Todo notebook começa com a seção **0. Como rodar este notebook**, que explica como abrir no **Google Colab** (recomendado) ou rodar
no computador. A primeira célula de código prepara o Colab sozinha: clona este repositório, copia os dados do Google Drive quando a
aula precisa deles, instala as bibliotecas que faltarem e lê as chaves de API dos *Secrets* do Colab.

- **Código:** este repositório, https://github.com/pasteurjr/notebookvideoaulas.
- **Dados:** as aulas marcadas com "Google Drive" usam a pasta [notebooksvideos](https://drive.google.com/drive/folders/1mMRjinjohj_jyMsJzO7rxgYKm6unVKze?usp=sharing), com a mesma estrutura de pastas
  deste repositório. Adicione um atalho dela ao seu *Meu Drive* (instruções no topo de cada notebook).
- **Chaves de API** (DeepSeek, Serper): nunca ficam nos notebooks. No Colab, use os *Secrets* (ícone 🔑); no computador, copie
  `.env.exemplo` para `.env` na pasta do notebook e coloque as suas chaves. O `.env` não vai para o GitHub.

