"""Gera o dataset de perguntas e respostas para o fine-tuning, a partir dos textos
da base de conhecimento (noterag/aularag/dados/documentos), usando o DeepSeek.

Uso (de dentro de notefinetuning/aulafinetuning):
    python _geracao/gerar_dataset.py
Saída: dados/iras_perguntas_respostas.jsonl  ({"instruction", "response", "fonte"})
"""
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

AQUI = Path(__file__).resolve().parents[1]
DOCS = AQUI.parents[1] / "07_rag" / "notebook" / "dados" / "documentos"
SAIDA = AQUI / "dados" / "iras_perguntas_respostas.jsonl"
POR_DOCUMENTO = 45
FOCOS = [  # três rodadas por documento, cada uma com um foco, para cobrir cada fato de vários jeitos
    "Cubra TODOS os fatos do texto, um por um: definições, listas, números e critérios.",
    "Foque em casos práticos do dia a dia do hospital e em cálculos com números, aplicando as regras do texto.",
    "Reformule com outras palavras as perguntas mais importantes: listas completas (todos os itens), critérios e diferenças entre conceitos.",
]

load_dotenv(AQUI / ".env")
cliente = OpenAI(api_key=os.environ["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")

PROMPT = """Você vai criar dados de treinamento para um assistente de controle de infecção hospitalar.
Com base SOMENTE no texto abaixo, escreva {n} pares de pergunta e resposta em português do Brasil.\n{foco}

Regras:
- Perguntas variadas: definições, "o que é", "como calcular", "quando usar", "quais são", casos práticos curtos com números.
- Varie a forma de perguntar (formal, direta, como um profissional de saúde perguntaria no plantão).
- Respostas corretas, objetivas, com 2 a 4 frases, no tom de um infectologista explicando a um colega.
- Não invente dados que não estejam no texto. Não cite "o texto".
- Responda em JSON: {{"pares": [{{"pergunta": "...", "resposta": "..."}}, ...]}}

TEXTO:
{texto}"""

pares = []
vistas = set()
for doc in sorted(DOCS.glob("*.md")):
    texto = doc.read_text(encoding="utf-8")
    for foco in FOCOS:
        r = cliente.chat.completions.create(
            model="deepseek-v4-flash",
            messages=[{"role": "user", "content": PROMPT.format(n=POR_DOCUMENTO, foco=foco, texto=texto)}],
            response_format={"type": "json_object"},
            temperature=0.8,
        )
        itens = json.loads(r.choices[0].message.content)["pares"]
        for p in itens:
            if p["pergunta"].strip().lower() not in vistas:   # sem perguntas repetidas
                vistas.add(p["pergunta"].strip().lower())
                pares.append({"instruction": p["pergunta"].strip(), "response": p["resposta"].strip(), "fonte": doc.name})
        print(f"{doc.name}: {len(itens)} pares")

SAIDA.parent.mkdir(exist_ok=True)
with open(SAIDA, "w", encoding="utf-8") as f:
    for p in pares:
        f.write(json.dumps(p, ensure_ascii=False) + "\n")
print(f"Total: {len(pares)} pares -> {SAIDA}")
