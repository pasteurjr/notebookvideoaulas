# Roteiro do vídeo: Pipeline de treinamento de deep learning: COVID-19 em tomografias

| Item | Detalhe |
|---|---|
| **Notebook** | `pipeline_de_agentes.ipynb` (executado, com todas as saídas) |
| **Cenas** | 31, cada uma com uma tela capturada do Jupyter (1920×1080, pasta `telas/`) |
| **Narração** | 1285 palavras, em tom de aula |
| **Duração estimada** | **9 min 06 s** (~150 palavras/min + 1 s de pausa por cena) |
| **Fonte para montar o vídeo** | `roteiro.json` (tela, narração, início e duração de cada cena) |
| **Revisão** | Todas as telas foram conferidas contra a narração (números, nomes e trechos citados) |


---

## Roteiro cena a cena

### Cena 01: Abertura

`telas/01_abertura.png` · 0:00 → 0:21 (21 s)

**Na tela:** Título, objetivo e o fluxo do pipeline

> Olá! Nesta aula vamos construir um pipeline completo de treinamento de um modelo de deep learning. O problema é real: olhando uma tomografia computadorizada do pulmão, o modelo deve dizer se o caso é positivo para COVID-19 ou normal. Um aviso importante: é um exemplo didático, não serve para diagnóstico médico.

### Cena 02: O caminho e os conceitos

`telas/02_pipeline_conceitos.png` · 0:21 → 0:46 (25 s)

**Na tela:** Fluxo em 7 etapas e a tabela de conceitos

> O caminho é o de qualquer projeto de visão computacional: dividir as imagens, carregá-las, aproveitar um modelo pré-treinado, treinar, avaliar e fazer previsões. Deep learning são redes neurais com muitas camadas que aprendem padrões direto dos pixels. E transfer learning é reaproveitar uma rede já treinada em milhões de imagens para um problema com poucas imagens, como o nosso.

### Cena 03: Bibliotecas e GPU

`telas/03_bibliotecas_gpu.png` · 0:46 → 1:10 (24 s)

**Na tela:** Importações e a saída 'GPU disponível: RTX 5080'

> Usamos o TensorFlow com o Keras, a biblioteca de deep learning; o scikit-learn, para as métricas; e o matplotlib, para os gráficos. Treinar uma rede envolve milhões de multiplicações, e a GPU, a placa de vídeo, faz essas contas em paralelo. Aqui ela foi encontrada: uma RTX 5080. No Colab, a GPU T4 gratuita também dá conta.

### Cena 04: Configurações

`telas/04_configuracoes.png` · 1:10 → 1:31 (21 s)

**Na tela:** Tabela de parâmetros e a célula de configuração

> Todos os parâmetros ficam juntos numa célula. Três merecem atenção. O lote é quantas imagens a rede vê antes de cada ajuste; aqui, oito. Uma época é uma passada completa por todas as imagens de treino. E a taxa de aprendizado é o tamanho do passo em cada ajuste dos pesos.

### Cena 05: Conhecendo os dados

`telas/05_dados_contagem.png` · 1:31 → 1:47 (16 s)

**Na tela:** Contagem: 349 covid, 397 normal, 746 no total

> Os dados são o COVID-CT, um conjunto público de tomografias. Antes de treinar, sempre olhamos os dados: são 349 imagens de covid e 397 normais, 746 no total. As classes estão equilibradas, o que facilita o treino.

### Cena 06: Exemplos de tomografias

`telas/06_dados_exemplos.png` · 1:47 → 2:00 (13 s)

**Na tela:** Grade com 4 imagens de cada classe

> Aqui estão alguns exemplos. Repare que as imagens têm tamanhos e formatos diferentes: algumas coloridas, outras em tons de cinza. Mais adiante, todas serão padronizadas para 224 por 224 pixels.

### Cena 07: Treino, validação e teste

`telas/07_divisao_explicacao.png` · 2:00 → 2:24 (24 s)

**Na tela:** Tabela dos três conjuntos com a analogia

> Esta é uma das etapas mais importantes. Separamos as imagens em três conjuntos que nunca se misturam: o treino, que é o material de estudo; a validação, que funciona como os simulados; e o teste, que é a prova final. Testar com imagens de treino seria dar a prova com as mesmas questões do material de estudo.

### Cena 08: Dividindo as imagens

`telas/08_divisao_codigo.png` · 2:24 → 2:43 (19 s)

**Na tela:** Função dividir_dataset e a tabela 537 / 59 / 150

> A função embaralha as imagens com uma semente fixa, para ser reproduzível, e copia cada uma para a pasta do seu conjunto e da sua classe. O resultado: 537 imagens de treino, 59 de validação e 150 de teste, sempre com as duas classes.

### Cena 09: Carregando com tf.data

`telas/09_carregamento.png` · 2:43 → 3:01 (18 s)

**Na tela:** Explicação de image_dataset_from_directory

> Em vez de carregar tudo na memória, criamos um dataset que lê as imagens do disco em lotes. Ele descobre o rótulo pelo nome da pasta, redimensiona para 224 por 224 e codifica o rótulo em one-hot: covid vira um-zero, e normal, zero-um.

### Cena 10: Um lote de imagens

`telas/10_carregamento_saida.png` · 3:01 → 3:13 (12 s)

**Na tela:** Formato (8, 224, 224, 3) e rótulos one-hot

> A saída confirma: cada lote tem oito imagens de 224 por 224 pixels, com três canais de cor. E aqui estão os oito rótulos, já no formato one-hot.

### Cena 11: Aumento de dados e normalização

`telas/11_aumento_explicacao.png` · 3:13 → 3:40 (27 s)

**Na tela:** Explicação e o código do aumento de dados

> Com poucas imagens, a rede pode decorar o treino em vez de aprender, o chamado overfitting. O aumento de dados mostra, a cada época, versões levemente giradas, espelhadas ou aproximadas das imagens. E a normalização, com o preprocess input, coloca as imagens no formato em que a VGG16 foi treinada. Esquecer esse passo é um erro comum, e os notebooks originais deste projeto o esqueciam.

### Cena 12: Aumento de dados em ação

`telas/12_aumento_exemplo.png` · 3:40 → 3:50 (10 s)

**Na tela:** A mesma tomografia em 7 variações

> Veja o efeito: a mesma tomografia, transformada sete vezes de forma aleatória. Para a rede, é como se tivéssemos muito mais imagens.

### Cena 13: Transfer learning com a VGG16

`telas/13_vgg16_explicacao.png` · 3:50 → 4:12 (22 s)

**Na tela:** Explicação da VGG16 e dos parâmetros

> Treinar uma rede do zero exigiria dezenas de milhares de imagens. Então usamos a VGG16, uma rede de 16 camadas já treinada no ImageNet, com mais de um milhão de fotos. Descartamos a parte final dela, que classificava mil categorias, e congelamos o resto, para que seus pesos não mudem na primeira fase.

### Cena 14: A VGG16 carregada

`telas/14_vgg16_saida.png` · 4:12 → 4:26 (14 s)

**Na tela:** Saída: 19 camadas, 14.714.688 parâmetros

> A VGG16 carregada tem 19 camadas e cerca de 14,7 milhões de parâmetros, que são os pesos aprendidos no ImageNet. As últimas camadas formam o bloco cinco, que vamos usar mais adiante.

### Cena 15: A nova cabeça

`telas/15_cabeca_explicacao.png` · 4:26 → 4:46 (20 s)

**Na tela:** Tabela das camadas da cabeça

> Sobre a VGG16 colocamos uma cabeça nova. O pooling resume as características extraídas; a camada densa as combina; o dropout desliga metade dos neurônios durante o treino, para a rede não depender de poucos detalhes; e a saída softmax devolve duas probabilidades que somam um: covid e normal.

### Cena 16: Resumo do modelo

`telas/16_cabeca_resumo.png` · 4:46 → 5:02 (16 s)

**Na tela:** Parâmetros treináveis (131.842) e não treináveis

> No resumo do modelo, compare os números: só cerca de 132 mil parâmetros são treináveis, os da cabeça nova. Os 14,7 milhões da VGG16 estão congelados. É por isso que o transfer learning funciona com poucas imagens.

### Cena 17: Compilando e treinando

`telas/17_treino1_explicacao.png` · 5:02 → 5:24 (22 s)

**Na tela:** compile: Adam, categorical_crossentropy, accuracy e EarlyStopping

> Antes de treinar, compilamos o modelo. O otimizador Adam ajusta os pesos; a função de perda mede o erro das previsões; e a acurácia é a porcentagem de acertos. O early stopping vigia a validação: se ela parar de melhorar por oito épocas, o treino para e os melhores pesos são restaurados.

### Cena 18: Primeiras épocas

`telas/18_treino1_inicio.png` · 5:24 → 5:37 (13 s)

**Na tela:** Linhas das épocas com loss e val_accuracy

> Cada linha é uma época. A perda, o loss, vai caindo, e a acurácia na validação sobe rápido: de 68% na primeira época para cerca de 90% em poucas épocas.

### Cena 19: Fim da fase 1

`telas/19_treino1_fim.png` · 5:37 → 5:45 (8 s)

**Na tela:** 'Fase 1: 44 épocas em 130 segundos'

> O early stopping encerrou a primeira fase na época 44, em pouco mais de dois minutos na GPU.

### Cena 20: Ajuste fino

`telas/20_ajustefino_explicacao.png` · 5:45 → 6:04 (19 s)

**Na tela:** Descongelando o bloco 5 com taxa 1e-5

> Na segunda fase, o ajuste fino, descongelamos o último bloco da VGG16 para que ele também se adapte às tomografias. Usamos uma taxa de aprendizado dez vezes menor, porque os pesos pré-treinados são valiosos e passos grandes os estragariam. E compilamos de novo o modelo.

### Cena 21: Fim do ajuste fino

`telas/21_ajustefino_fim.png` · 6:04 → 6:13 (9 s)

**Na tela:** 'Fase 2: 13 épocas em 41 segundos'

> O ajuste fino levou 13 épocas, em cerca de 40 segundos. A acurácia na validação chegou perto de 95%.

### Cena 22: Curvas de aprendizado

`telas/22_curvas_explicacao.png` · 6:13 → 6:24 (11 s)

**Na tela:** Como ler as curvas e o código do gráfico

> As curvas de aprendizado mostram a evolução ao longo das épocas. Se o treino continua melhorando enquanto a validação piora, é sinal de overfitting.

### Cena 23: Os gráficos

`telas/23_curvas_grafico.png` · 6:24 → 6:40 (16 s)

**Na tela:** Perda e acurácia, com a linha do início do ajuste fino

> À esquerda, a perda cai e se estabiliza; à direita, a acurácia sobe. A linha tracejada marca o início do ajuste fino, que ainda trouxe um ganho. Treino e validação andam juntos, sem sinal forte de overfitting.

### Cena 24: Avaliação no teste

`telas/24_relatorio.png` · 6:40 → 6:57 (17 s)

**Na tela:** Relatório de classificação: acurácia 0,820

> Agora, a prova final: as 150 imagens de teste, que o modelo nunca viu. O relatório mostra, para cada classe, a precisão, o recall e o f1. A acurácia geral foi de 82%, acima dos 73 a 77% dos notebooks originais.

### Cena 25: Recall, precisão e especificidade

`telas/25_metricas_explicacao.png` · 6:57 → 7:22 (25 s)

**Na tela:** Tabela de métricas com as fórmulas

> Considerando covid como o caso positivo, temos verdadeiros positivos, falsos negativos, verdadeiros negativos e falsos positivos. O recall, ou sensibilidade, mede quantos casos de covid o modelo detectou. A especificidade, quantos normais ele reconheceu. E a precisão, quantas vezes acertou ao dizer covid. Em medicina, o recall é crucial: um falso negativo é um paciente doente mandado para casa.

### Cena 26: Matriz de confusão

`telas/26_matriz_confusao.png` · 7:22 → 7:37 (15 s)

**Na tela:** Matriz 51 / 18 / 9 / 72

> Na matriz de confusão, a diagonal são os acertos: 51 casos de covid detectados e 72 normais reconhecidos. Os erros: 18 casos de covid que passaram como normais e 9 normais acusados de covid.

### Cena 27: Os números

`telas/27_metricas_valores.png` · 7:37 → 7:52 (15 s)

**Na tela:** Recall 73,9%, especificidade 88,9%, precisão 85%, acurácia 82%

> Em números: recall de 73,9%, especificidade de 88,9%, precisão de 85% e acurácia de 82%. O modelo é mais seguro para descartar do que para detectar a doença, e melhorar o recall seria o próximo objetivo.

### Cena 28: Salvando o modelo

`telas/28_salvar_modelo.png` · 7:52 → 8:07 (15 s)

**Na tela:** Modelo salvo (117 MB) e carregado com as mesmas previsões

> O modelo treinado é salvo num único arquivo ponto keras, com a arquitetura e os pesos, e pode ser usado depois sem treinar de novo. Carregamos o arquivo e conferimos: as previsões são as mesmas.

### Cena 29: Prevendo uma tomografia

`telas/29_previsao_imagem.png` · 8:07 → 8:27 (20 s)

**Na tela:** Função prever_imagem e os resultados 94,1% e 100%

> Por fim, o uso prático: uma função que recebe uma tomografia e devolve o diagnóstico com o grau de certeza. A imagem passa pelas mesmas transformações do treino. Nos exemplos, uma tomografia de covid foi classificada como positiva, com 94% de certeza, e uma normal, como negativa.

### Cena 30: Previsões em imagens de teste

`telas/30_previsoes_grade.png` · 8:27 → 8:46 (19 s)

**Na tela:** Grade de 8 previsões: verde acerto, vermelho erro

> Nesta grade, verde é acerto e vermelho é erro. O modelo acertou sete de oito. O erro foi um caso de covid classificado como normal, justamente o tipo de erro mais perigoso. Repare também num acerto com só 52% de certeza: o modelo estava em dúvida.

### Cena 31: Resumo e exercícios

`telas/31_resumo_exercicios.png` · 8:46 → 9:06 (20 s)

**Na tela:** Lista do que fizemos e os 5 exercícios

> Recapitulando: exploramos os dados, dividimos em treino, validação e teste, aplicamos aumento de dados e normalização, usamos transfer learning com a VGG16, treinamos em duas fases e avaliamos com recall e especificidade. Como exercício, troquem a VGG16 pela ResNet50, rodem sem a normalização e comparem. Até a próxima!
