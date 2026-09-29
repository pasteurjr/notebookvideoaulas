# Roteiro do vídeo: Pipeline de Agentes com CrewAI: qualificação de leads e e-mail de vendas

| Item | Detalhe |
|---|---|
| **Notebook** | `pipeline_de_agentes.ipynb` (executado, com todas as saídas) |
| **Cenas** | 37, cada uma com uma tela capturada do Jupyter (1920×1080, pasta `telas/`) |
| **Narração** | 1285 palavras, em tom de aula |
| **Duração estimada** | **9 min 10 s** (~150 palavras/min + 1 s de pausa por cena) |
| **Fonte para montar o vídeo** | `roteiro.json` (tela, narração, início e duração de cada cena) |
| **Revisão** | Todas as telas foram conferidas contra a narração (números, nomes e trechos citados) |


---

## Roteiro cena a cena

### Cena 01: Abertura

`telas/01_abertura.png` · 0:00 → 0:25 (25 s)

**Na tela:** Título e a lista de 5 passos do pipeline

> Olá! Nesta aula vamos ver um pipeline comercial feito só com agentes de IA, usando o CrewAI, uma biblioteca Python para criar equipes de agentes. A partir de um lead, uma pessoa interessada no nosso produto, os agentes pesquisam a pessoa e a empresa na internet, dão uma nota e, se ela for boa, escrevem um e-mail de vendas personalizado.

### Cena 02: Arquitetura e conceitos

`telas/02_arquitetura_conceitos.png` · 0:25 → 0:51 (26 s)

**Na tela:** Diagrama das duas crews e a tabela de conceitos

> São cinco agentes em duas equipes. Guarde cinco conceitos: agente é um assistente de IA com um papel definido; tarefa é o trabalho dado a ele; ferramenta é algo que ele usa além do próprio conhecimento, como uma busca no Google; crew é uma equipe de agentes; e flow é o roteiro que diz o que roda primeiro e o que vem depois.

### Cena 03: Pré-requisitos e chaves de API

`telas/03_prerequisitos_chaves.png` · 0:51 → 1:16 (25 s)

**Na tela:** Tabela DeepSeek / Serper e os passos do arquivo .env

> Os agentes usam dois serviços: o DeepSeek, que fornece o LLM, o modelo de linguagem que lê e escreve texto, e o Serper, que busca no Google. Cada um exige uma chave de API, uma senha que identifica a sua conta e desconta os créditos dela. Cada aluno cria as suas, e elas ficam no arquivo ponto env, nunca no notebook.

### Cena 04: Versões instaladas

`telas/04_versoes.png` · 1:16 → 1:27 (11 s)

**Na tela:** Saída: CrewAI 1.15.22 e Pydantic 2.12.5

> A primeira célula confere as versões: CrewAI um ponto quinze e Pydantic dois. Isso ajuda quando algo dá errado, porque o CrewAI muda bastante entre versões.

### Cena 05: Importações e .env

`telas/05_importacoes_env.png` · 1:27 → 1:42 (15 s)

**Na tela:** load_dotenv(".env") e o import de Agent, Task, Crew, LLM

> O destaque das importações é o load dotenv: ele lê o ponto env e cria variáveis de ambiente, configurações que o programa enxerga sem que apareçam no código. É ali que o CrewAI busca as chaves.

### Cena 06: Verificando chaves e criando o LLM

`telas/06_chaves_llm.png` · 1:42 → 1:53 (11 s)

**Na tela:** Saída das chaves carregadas, modelo deepseek-v4-flash e temperature=0.3

> Aqui conferimos se as chaves foram carregadas, sem exibi-las, e criamos o LLM, o deepseek v4 flash. O temperature baixo deixa as respostas mais previsíveis.

### Cena 07: Configuração em YAML

`telas/07_yaml_explicacao.png` · 1:53 → 2:18 (25 s)

**Na tela:** Tabela com os 4 arquivos e a tabela de campos (role, goal, backstory, description, expected_output)

> Os textos dos agentes e das tarefas ficam em arquivos YAML, um formato de texto simples com pares nome e valor. Cada agente tem role, o papel; goal, o objetivo; e backstory, a história que lhe dá experiência e personalidade. Cada tarefa tem description, o que fazer, e expected output, como entregar. Tudo isso vira instrução para o modelo.

### Cena 08: Carregando os YAML

`telas/08_yaml_carregamento.png` · 2:18 → 2:29 (11 s)

**Na tela:** Saída com os nomes dos 5 agentes

> O código abre os quatro arquivos e guarda cada um num dicionário. A saída confirma os cinco agentes: três de qualificação e dois de e-mail.

### Cena 09: Por dentro de um YAML

`telas/09_yaml_agentes.png` · 2:29 → 2:48 (19 s)

**Na tela:** role, goal e backstory do Especialista em Dados de Leads

> Por dentro, o especialista em dados tem papel, objetivo e uma história que o descreve como detalhista: é a descrição do cargo, que orienta como ele pensa. O verbose mostra o raciocínio na tela, e o allow delegation falso impede que ele repasse o trabalho.

### Cena 10: Por dentro do YAML de tarefas

`telas/09b_yaml_tarefas.png` · 2:48 → 3:06 (18 s)

**Na tela:** description, expected_output e a variável {dados_lead}

> No arquivo de tarefas, a description é a ordem de serviço, com o que pesquisar, e o expected output descreve o relatório a entregar. O dados lead entre chaves é uma variável: na execução, o CrewAI troca esse trecho pelos dados do lead.

### Cena 11: Saída estruturada com Pydantic

`telas/10_pydantic_explicacao.png` · 3:06 → 3:23 (17 s)

**Na tela:** Explicação de output_pydantic e os três blocos

> LLMs respondem em texto livre, que é difícil de usar num programa. Por isso usamos o Pydantic, uma biblioteca Python para descrever e validar estruturas de dados: dizemos quais campos a resposta deve ter, de que tipo e com que limites.

### Cena 12: Os modelos Pydantic

`telas/11_pydantic_codigo.png` · 3:23 → 3:44 (21 s)

**Na tela:** Classes do Pydantic, Field e os limites ge/le

> Cada classe é um molde: dados pessoais, dados da empresa e pontuação, e uma quarta classe junta tudo. O Field descreve cada campo, e os limites ge e le, maior ou igual e menor ou igual, garantem, por exemplo, nota entre zero e cem. Assim a resposta vira um objeto Python.

### Cena 13: Ferramentas

`telas/12_ferramentas.png` · 3:44 → 3:59 (15 s)

**Na tela:** SerperDevTool e ScrapeWebsiteTool

> As ferramentas são as mãos dos agentes: o SerperDevTool busca no Google, e o ScrapeWebsiteTool lê o texto de uma página, o chamado scraping. É o próprio agente que decide quando usar cada uma.

### Cena 14: Crew 1: qualificação

`telas/13_crew1_explicacao.png` · 3:59 → 4:20 (21 s)

**Na tela:** Tabela dos 3 agentes e o parâmetro context

> A primeira equipe tem o especialista em dados, o analista de afinidade cultural, que avalia se a empresa combina com a nossa, e o avaliador, que dá a nota. O context faz o avaliador receber o resultado dos colegas: é assim que um agente usa o trabalho do outro.

### Cena 15: Código da Crew 1

`telas/14_crew1_codigo.png` · 4:20 → 4:38 (18 s)

**Na tela:** context=[...] e output_pydantic na terceira tarefa

> Cada agente recebe a configuração do YAML, as ferramentas e o LLM, e cada tarefa é ligada ao seu agente. Na última estão o context e o output pydantic, que obriga a resposta a seguir o nosso molde. A Crew reúne tudo.

### Cena 16: Crew 2: e-mail

`telas/15_crew2.png` · 4:38 → 4:53 (15 s)

**Na tela:** Redator e Especialista em Engajamento, sem ferramentas

> A segunda equipe escreve o e-mail: o redator faz o rascunho, e o especialista em engajamento acrescenta CTAs, as chamadas para ação, como um convite para reunião. Eles não usam ferramentas: os dados já chegam prontos.

### Cena 17: O Flow

`telas/16_flow_explicacao.png` · 4:53 → 5:12 (19 s)

**Na tela:** @start, @listen e a tabela de etapas

> O Flow junta as equipes. Cada método é uma etapa, e a ordem vem dos decoradores, as marcações com arroba sobre a função: start marca o início, e listen faz uma etapa começar quando outra termina. O lead é uma pessoa fictícia, numa empresa real.

### Cena 18: Código do Flow

`telas/17_flow_codigo.png` · 5:12 → 5:30 (18 s)

**Na tela:** buscar_leads → pontuar_leads → filtrar_leads (> 70) → escrever_email

> O caminho: buscar os leads; pontuar cada um com a primeira equipe, usando o kickoff for each, e guardar o resultado no state, a memória compartilhada do fluxo; filtrar quem tem nota acima de setenta; e escrever o e-mail com a segunda equipe.

### Cena 19: Diagrama do fluxo

`telas/19_diagrama_fluxo.png` · 5:30 → 5:38 (8 s)

**Na tela:** Caixas e setas: quem escuta quem

> O CrewAI desenha o fluxo: cada caixa é uma etapa, e cada seta mostra quem escuta quem.

### Cena 20: Executando o pipeline

`telas/20_execucao_inicio.png` · 5:38 → 5:52 (14 s)

**Na tela:** await fluxo.kickoff_async() e o início do fluxo

> Hora de rodar. Usamos await com kickoff async porque o Jupyter é assíncrono: espera uma operação demorada sem travar. Leva alguns minutos, e o verbose mostra tudo o que os agentes fazem.

### Cena 21: A crew começa

`telas/21_exec_crew_iniciada.png` · 5:52 → 6:00 (8 s)

**Na tela:** Painéis 'Crew Execution Started' e 'Task Started'

> A equipe recebe a primeira tarefa, e a variável dados lead já foi trocada pelos dados do lead.

### Cena 22: O especialista em dados entra em ação

`telas/22_exec_agente_dados.png` · 6:00 → 6:07 (7 s)

**Na tela:** 'Agent Started' e o primeiro 'Tool Execution Started'

> O especialista em dados decide sozinho usar a busca: pesquisa setor, funcionários e faturamento do Nubank.

### Cena 23: Buscando no Google

`telas/23_exec_ferramenta_busca.png` · 6:07 → 6:14 (7 s)

**Na tela:** Resultado da busca: links e trechos reais

> Aqui estão as buscas e um resultado: títulos, links e trechos reais, vindos do Google.

### Cena 24: Resposta do especialista

`telas/24_exec_resposta_dados.png` · 6:14 → 6:27 (13 s)

**Na tela:** 'Agent Final Answer': relatório de análise do lead

> A resposta final é um relatório em português. O agente percebeu que a pessoa é fictícia e não inventou dados: só confirmou o que é público sobre a empresa.

### Cena 25: Analista de afinidade cultural

`telas/25_exec_agente_afinidade.png` · 6:27 → 6:36 (9 s)

**Na tela:** Busca por cultura e valores da empresa

> O analista de afinidade pesquisa cultura e valores. Cada agente busca de acordo com o papel descrito no YAML.

### Cena 26: O avaliador

`telas/26_exec_avaliador.png` · 6:36 → 6:43 (7 s)

**Na tela:** Avaliador e Validador de Leads recebe o contexto

> O avaliador recebe, pelo context, o trabalho dos dois colegas e consolida tudo numa nota.

### Cena 27: A nota do lead

`telas/27_exec_resposta_nota.png` · 6:43 → 6:56 (13 s)

**Na tela:** JSON estruturado com 'pontuacao': 94

> A resposta vem em JSON, um formato de dados estruturado, seguindo o molde do Pydantic. Nota: noventa e quatro, com o peso de cada critério. Passou no filtro com folga.

### Cena 28: A crew de e-mail assume

`telas/28_exec_redator_email.png` · 6:56 → 7:04 (8 s)

**Na tela:** Redator de E-mails recebendo os dados qualificados

> Com nota acima de setenta, o fluxo aciona a segunda equipe, e o redator começa a escrever.

### Cena 29: E-mail otimizado

`telas/29_exec_email_final.png` · 7:04 → 7:13 (9 s)

**Na tela:** 'Agent Final Answer' do Especialista em Engajamento

> O especialista em engajamento entrega a versão final: direta, personalizada e com uma chamada clara para agendar uma reunião.

### Cena 30: Tokens e custo

`telas/31_custos.png` · 7:13 → 7:34 (21 s)

**Na tela:** Tokens de cada crew (164.667 e 119.638) e o custo estimado com preço de exemplo

> Os modelos cobram por token, um pedaço de palavra, contando o texto enviado e o gerado. Foram cerca de cento e sessenta e cinco mil tokens na qualificação e cento e vinte mil no e-mail. Com o preço de exemplo da célula, isso dá uns quatro centavos de dólar.

### Cena 31: Tabela do lead

`telas/33_tabela_lead_final.png` · 7:34 → 7:51 (17 s)

**Na tela:** Porte, setor, presença de mercado 10, nota 94

> Com o Pydantic, montar esta tabela é só ler os campos: setor, cerca de dez mil funcionários, faturamento, presença de mercado e a nota noventa e quatro. Dados prontos para um CRM, o sistema que gerencia os clientes da empresa.

### Cena 32: O e-mail final

`telas/34_email_gerado.png` · 7:51 → 8:03 (12 s)

**Na tela:** Texto completo do e-mail em português

> E o produto final: o e-mail pronto para envio, com o nome da pessoa, os dados levantados, os casos de uso do formulário e uma chamada para ação.

### Cena 33: Indo além: router, and_ e or_

`telas/35_router_explicacao.png` · 8:03 → 8:17 (14 s)

**Na tela:** Tabela alto / medio / baixo e o aviso sobre self.state

> Para ir além: o and faz uma etapa esperar duas outras. O router é um desvio: devolve um rótulo, como alto, médio ou baixo, e só roda o caminho com aquele rótulo.

### Cena 34: Código do router

`telas/36_router_codigo.png` · 8:17 → 8:30 (13 s)

**Na tela:** -> Literal['alto', 'medio', 'baixo'] e self.state["leads_aprovados"]

> A anotação Literal lista os rótulos possíveis, para o diagrama desenhar os caminhos. E quem escuta um rótulo recebe só o rótulo; por isso os leads aprovados ficam no state.

### Cena 35: Diagrama do fluxo completo

`telas/37_diagrama_completo.png` · 8:30 → 8:38 (8 s)

**Na tela:** Router contar_leads com três saídas tracejadas

> No novo diagrama, as linhas vermelhas são o and, e as tracejadas são os três caminhos do router.

### Cena 36: Resultado do fluxo completo

`telas/38_fluxo_completo_email.png` · 8:38 → 8:49 (11 s)

**Na tela:** E-mail gerado pelo caminho 'baixo'

> Com um lead só, o router escolheu o caminho baixo e gerou um novo e-mail. O texto muda a cada execução, mas a estrutura se mantém.

### Cena 37: Resumo e exercícios

`telas/39_resumo_exercicios.png` · 8:49 → 9:10 (21 s)

**Na tela:** Lista do que vimos e os 5 exercícios

> Recapitulando: agentes com papel, objetivo e história; ferramentas para pesquisar na web; tarefas encadeadas com context; respostas estruturadas com Pydantic; e equipes orquestradas por um Flow. Agora é com vocês: troquem a empresa e o produto, adicionem leads e, como desafio, criem um agente que descubra leads sozinho. Até a próxima!
