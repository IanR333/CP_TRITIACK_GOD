# Avaliação Preditiva de Energias Renováveis e Radiação Solar

**Autor:** Ian Rodrigues Martins (RM 570540) , Gabriel del pizzo pintor ( RM570436)
**Instituição:** FIAP — Ciência da Computação

Este projeto aplica Machine Learning a dois problemas do domínio de energia, usando dados de duas APIs públicas (sem token). A avaliação principal foi feita em **Python (scikit-learn)**, e a atividade complementar foi feita no **Orange Data Mining**.

1. **Classificação:** prever a fonte de um empreendimento de geração (Solar, Eólica ou Hidráulica) a partir da potência outorgada e da localização.
2. **Regressão:** estimar a radiação solar horária (W/m²) em Petrolina (PE) a partir de variáveis meteorológicas e da hora do dia.

Em cada tarefa, **três algoritmos** foram treinados e comparados com a mesma configuração de avaliação.

## Dados

| Tarefa | Fonte | Detalhes |
|---|---|---|
| Classificação | [SIGA — ANEEL](https://dadosabertos.aneel.gov.br/dataset/siga-sistema-de-informacoes-de-geracao-da-aneel) (API CKAN) | `UFV` → Solar, `EOL` → Eólica, `UHE/PCH/CGH` → Hidráulica. Até 1200 linhas por sigla (3876 linhas válidas). Entradas: `potencia_kw`, `latitude`, `longitude`. Alvo: `fonte`. O cadastro inclui empreendimentos em diferentes fases e **não mede energia gerada**; as contagens **não** representam a matriz energética brasileira. |
| Regressão | [Open-Meteo histórico](https://open-meteo.com/en/docs/historical-weather-api) | Petrolina (−9,39; −40,50), de **01/04/2025 a 30/06/2025**, fuso `America/Recife`, horas de 7h a 17h (1001 linhas). Dados de modelo/reanálise, não de um painel fotovoltaico. |

## Estrutura do repositório

```
avaliacao_energias_renovaveis.ipynb   notebook completo: consulta às APIs, análise, 6 modelos, métricas e interpretação
aneel_classificacao_orange.csv        dados da classificação (gerado pelo notebook)
meteo_regressao_orange.csv            dados da regressão (gerado pelo notebook)
dividir_meteo_orange.py               divide o CSV da regressão em treino (80% iniciais) e teste (20% finais)
Fluxos_para_Classificacao_e_Regressao.ows   fluxos do Orange (classificação e regressão)
orange/                               capturas dos fluxos do Orange (fluxo_classificacao.png, fluxo_regressao.png)
figuras/                              gráficos gerados pelo notebook
ORANGE.md                             procedimento e análise da atividade no Orange
requirements.txt                      dependências
```

## Como executar

```bash
pip install -r requirements.txt
jupyter notebook avaliacao_energias_renovaveis.ipynb   # Run All (precisa de internet)
```

O notebook roda na ordem das células: consulta as APIs, gera os dois CSVs, faz a análise e treina os seis modelos. Semente fixa: `SEED = 42`. Para a parte do Orange, rode `python dividir_meteo_orange.py` para gerar `meteo_treino_orange.csv` e `meteo_teste_orange.csv`.

## Metodologia (notebook Python)

- **Classificação:** divisão **estratificada 80/20** (`random_state=42`); padronização dentro de um `Pipeline`, ajustada só com o treino. Modelos: Regressão Logística, KNN (k = 7) e Random Forest (300 árvores). Métricas: Accuracy, Precision, Recall e F1 com média **macro**, mais matriz de confusão.
- **Regressão:** divisão **temporal**, com as primeiras 80% das horas para treino e as últimas 20% para teste, sem embaralhar. Modelos: Regressão Linear, Random Forest Regressor e Gradient Boosting Regressor. Métricas: MAE (W/m²), MSE ((W/m²)²) e R², além do gráfico real × previsto. `radiacao_w_m2` e `data_hora` não entram em X.

## Resultados — notebook Python

**Classificação** (teste estratificado de 20%, 776 empreendimentos, médias macro)

| Algoritmo | Accuracy | Precision | Recall | F1 |
|---|---|---|---|---|
| Regressão Logística | 0,8247 | 0,8282 | 0,8214 | 0,8197 |
| KNN (k = 7) | 0,9652 | 0,9668 | 0,9633 | 0,9647 |
| **Random Forest** | **0,9755** | **0,9769** | **0,9741** | **0,9753** |

**Regressão** (teste = últimas 20% das horas, de 12/06 a 30/06/2025)

| Algoritmo | MAE (W/m²) | MSE ((W/m²)²) | R² |
|---|---|---|---|
| Regressão Linear | 145,20 | 30.034 | 0,360 |
| **Random Forest** | **66,40** | **7.210** | **0,846** |
| Gradient Boosting | 67,08 | 7.445 | 0,841 |

## Resultados — Orange Data Mining

No Orange, foram comparados **dois algoritmos por tarefa** (o notebook Python compara três algoritmos por tarefa), com **validação cruzada de 5 folds** (estratificada na classificação). Como a divisão é diferente da usada no notebook, os números **não são diretamente comparáveis** com as tabelas acima. Capturas em `orange/`.

**Classificação** (validação cruzada, 5 folds estratificados, média sobre as classes)

| Algoritmo | CA | Precision | Recall | F1 | AUC |
|---|---|---|---|---|---|
| Logistic Regression | 0,807 | 0,815 | 0,807 | 0,805 | 0,886 |
| kNN | 0,870 | 0,872 | 0,870 | 0,871 | 0,954 |

Na matriz de confusão da Regressão Logística, a maior confusão é **Solar classificada como Eólica** (303 de 1200 solares, 25%).

**Regressão** (validação cruzada aleatória, 5 folds)

| Algoritmo | MAE (W/m²) | MSE ((W/m²)²) | RMSE (W/m²) | R² |
|---|---|---|---|---|
| Linear Regression | > 118 | ≈ 22.800 (RMSE²) | ≈ 151 | 0,652 |
| Tree | 61,44 | ≈ 7.571 (RMSE²) | 87,01 | 0,885 |

## Conclusões

- **Classificação:** no notebook, o Random Forest foi o melhor (F1 macro 0,975), seguido do KNN (0,965), e a Regressão Logística ficou bem abaixo (0,820), pois fronteiras lineares não separam bem as classes. A potência é muito informativa neste cadastro (mediana de 1 kW para solar, cerca de 29,6 MW para eólica e 4 MW para hidráulica; 63% das linhas solares têm exatamente 1 kW) e a localização refina. Os erros do melhor modelo se concentram na classe Solar (recall 0,95), confundida com Hidráulica e Eólica. No Orange, a Regressão Logística também ficou atrás do kNN.
- **Regressão:** no notebook, Random Forest e Gradient Boosting ficaram praticamente empatados (R² ≈ 0,84–0,85) e muito acima da Regressão Linear (R² 0,36), porque a radiação segue um "sino" ao longo do dia que uma relação linear com a hora não representa. A hora é a variável mais importante: sem ela, o R² do Random Forest cai de 0,85 para 0,34. No Orange, o modelo de árvore também superou a Regressão Linear. Como a validação cruzada aleatória mistura horas vizinhas entre treino e teste, o resultado do Orange tende a ser mais otimista que a divisão temporal.
- **Radiação não é geração elétrica:** o alvo é a radiação global horizontal (W/m², estimada por reanálise). A energia gerada por um sistema fotovoltaico (kWh) depende também de inclinação e orientação dos painéis, eficiência dos módulos, temperatura de operação, perdas e potência instalada.

## Limitações

- As proporções entre classes vêm de uma consulta com limite por tipo e **não** representam a matriz energética brasileira.
- Na classificação, o split aleatório deixa empreendimentos vizinhos em treino e teste. Ao dividir por regiões de 0,1°, o Random Forest cai de 0,9755 para cerca de 0,94 de accuracy.
- O período da regressão cobre apenas três meses (abril a junho de 2025), e o teste tem radiação média menor que o treino (373 contra 498 W/m²). Os modelos não foram validados para outras épocas do ano.
- Os resultados dependem da resposta das APIs no momento da execução, então os números podem variar levemente.
