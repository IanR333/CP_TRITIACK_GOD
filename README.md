# APIs, energias renováveis e aprendizado de máquina

## Objetivo
Consultar duas APIs públicas (sem token) e resolver duas tarefas independentes, comparando **três algoritmos em cada uma**:

1. **Classificação:** prever a fonte de um empreendimento (Solar, Eólica ou Hidráulica) a partir de potência outorgada e localização.
2. **Regressão:** estimar a radiação solar horária (W/m²) em Petrolina (PE) a partir de variáveis meteorológicas e da hora.

## Dados
| Tarefa | Fonte | Detalhes |
|---|---|---|
| Classificação | [SIGA — ANEEL](https://dadosabertos.aneel.gov.br/dataset/siga-sistema-de-informacoes-de-geracao-da-aneel) (API CKAN, sem token) | `UFV` → Solar, `EOL` → Eólica, `UHE/PCH/CGH` → Hidráulica; até 1200 linhas por sigla; entradas: `potencia_kw`, `latitude`, `longitude`; alvo: `fonte`. Cadastro com empreendimentos em várias fases; **não mede energia gerada** e as contagens **não** representam a matriz energética. |
| Regressão | [Open-Meteo histórico](https://open-meteo.com/en/docs/historical-weather-api) (sem token) | Petrolina (−9,39; −40,50), **01/04/2025 a 30/06/2025**, fuso `America/Recife`, horas de 7h a 17h; dados de modelo/reanálise, não de um painel. |

## Como executar
```bash
pip install -r requirements.txt
jupyter notebook avaliacao_energias_renovaveis.ipynb   # Run All (precisa de internet)
```
O notebook roda na ordem das células: consulta as APIs, gera `aneel_classificacao_orange.csv` e `meteo_regressao_orange.csv`, e faz toda a análise. As figuras vão para `figuras/`. Semente fixa: `SEED = 42`.
Para a parte no Orange: veja [`ORANGE.md`](ORANGE.md) e rode `python dividir_meteo_orange.py` para gerar treino/teste temporal.

## Metodologia
- **Classificação:** split **estratificado 80/20**, `random_state=42`; padronização dentro de `Pipeline` (só no treino); modelos: **Regressão Logística**, **KNN (k=7)**, **Random Forest (300 árvores)**; métricas Accuracy, Precision, Recall e F1 com média **macro** (F1 weighted como referência) e matriz de confusão.
- **Regressão:** **primeiras 80% das horas para treino, últimas 20% para teste** (ordem temporal preservada); modelos: **Regressão Linear**, **Random Forest Regressor**, **Gradient Boosting Regressor**; métricas MAE (W/m²), MSE ((W/m²)²) e R²; gráfico real × previsto. `radiacao_w_m2` e `data_hora` não entram em X.

## Resultados

**Classificação** (teste estratificado 20%, 776 empreendimentos, `random_state=42`, médias macro)

| Algoritmo | Accuracy | Precision | Recall | F1 |
|---|---|---|---|---|
| Regressão Logística | 0,8247 | 0,8282 | 0,8214 | 0,8197 |
| KNN (k=7) | 0,9652 | 0,9668 | 0,9633 | 0,9647 |
| **Random Forest** | **0,9755** | **0,9769** | **0,9741** | **0,9753** |

**Regressão** (teste = últimas 20% das horas, 201 horas, de 12/06 a 30/06/2025)

| Algoritmo | MAE (W/m²) | MSE ((W/m²)²) | R² |
|---|---|---|---|
| Regressão Linear | 145,20 | 30.034 | 0,360 |
| **Random Forest** | **66,40** | **7.210** | **0,846** |
| Gradient Boosting | 67,08 | 7.445 | 0,841 |

Figuras em `figuras/` (exploração, matrizes de confusão, real × previsto, série do teste, importância das variáveis).

## Conclusões
- **Classificação:** o Random Forest foi o melhor (F1 macro 0,975), seguido do KNN; a Regressão Logística ficou bem abaixo (0,820), pois fronteiras lineares não separam bem as classes. A potência é muito informativa neste cadastro (mediana de 1 kW para solar, cerca de 29,6 MW para eólica e 4 MW para hidráulica; 63% das linhas solares têm exatamente 1 kW) e a localização refina. Os erros do Random Forest se concentram na classe Solar (recall 0,95), confundida com Hidráulica (7 casos) e Eólica (5). Limitações: sem dados de recurso natural, coordenadas aproximadas, cadastro com várias fases, classe Hidráulica que mistura UHE/PCH/CGH, amostra limitada por tipo (as contagens **não** representam a matriz energética) e um split aleatório que deixa empreendimentos vizinhos em treino e teste, o que tende a otimizar o resultado.
- **Regressão:** Random Forest e Gradient Boosting ficaram praticamente empatados (MAE ≈ 66–67 W/m², R² ≈ 0,84–0,85) e muito melhores que a Regressão Linear (R² 0,36), porque a radiação segue um "sino" ao longo do dia que uma relação linear com a hora não representa. A hora é a variável mais importante (importância 0,49; sem ela, o R² do Random Forest cai de 0,85 para 0,34). Os erros são maiores no meio do dia (cerca de 70–95 W/m² entre 9h e 15h, contra 23 W/m² às 7h). O teste tem radiação média menor que o treino (373 contra 498 W/m²), o que limita a generalização. Estimar radiação **não equivale a prever geração elétrica**: esta depende de inclinação/orientação, eficiência dos módulos, temperatura de operação, perdas, potência instalada, e é medida em kWh.
- **Orange:** capturas e análise em [`ORANGE.md`](ORANGE.md) e `orange/`.

## Estrutura
```
avaliacao_energias_renovaveis.ipynb   notebook completo
aneel_classificacao_orange.csv        (gerado pelo notebook)
meteo_regressao_orange.csv            (gerado pelo notebook)
dividir_meteo_orange.py               divisão temporal para o Orange
ORANGE.md                             fluxos e análise no Orange
figuras/                              gráficos gerados
```
