# Atividade complementar — Orange Data Mining

Ferramenta: Orange (versão usada: ______ ). Capturas dos fluxos: `orange/fluxo_classificacao.png` e `orange/fluxo_regressao.png`.

## 1. Classificação — ANEEL

**Fluxo:** `File` → `Data Table` → `Select Columns` → (`Distributions`) → `Test & Score` ← {`Logistic Regression`, `kNN`, `Random Forest`} → `Confusion Matrix`.

1. **File:** abra `aneel_classificacao_orange.csv`. Confira os tipos (3 numéricos + `fonte` categórica).
2. **Select Columns:** *Features* = `potencia_kw`, `latitude`, `longitude`; *Target* = `fonte`.
3. **Distributions** (opcional): ligue ao `Select Columns`, escolha `fonte` para ver o desequilíbrio entre classes.
4. **Learners** ligados ao `Test & Score` (mesma configuração para os três):
   - Logistic Regression (Regularização Ridge L2, C = 1)
   - kNN (nº de vizinhos = 7, métrica Euclidiana, peso uniforme)
   - Random Forest (300 árvores)
   - Em `Test & Score`: **Cross validation, 5 folds, estratificada** (ou *Random sampling* 80/20 repetido); marque *Stratified*. Dados sem padronização manual: o `Test & Score` aplica pré-processamento dentro dos folds; se necessário, adicione o widget `Preprocess` (Normalize features) **antes** de kNN e Logistic Regression, como aprendiz.
5. **Métricas** (aba de avaliação de classificação): CA (accuracy), Precision, Recall, F1 — marque *Average over classes* (equivale à média `macro`... confira e registre qual opção aparece na sua versão; em Orange 3 a média padrão é *weighted*).
6. **Confusion Matrix:** ligue ao `Test & Score` e veja cada modelo (selecione o modelo na lista do widget).

### Resultados (preencher com o que aparecer no seu Orange)

| Algoritmo | CA | Precision | Recall | F1 |
|---|---|---|---|---|
| Logistic Regression | | | | |
| kNN (k=7) | | | | |
| Random Forest | | | | |

Procedimento: ______ (ex.: validação cruzada estratificada 5 folds, média ______).

**Análise (2–4 frases):** quais classes foram mais confundidas (ver Confusion Matrix) e por que potência + localização não bastam (não há dados de recurso natural; coordenadas aproximadas; cadastro com fases diferentes; amostra limitada por tipo, então as contagens **não** representam a matriz energética do Brasil).

## 2. Regressão — Open-Meteo

**Fluxo:** dois `File` (treino e teste) → `Select Columns` → `Test & Score` (**Test on test data**) ← {`Linear Regression`, `Random Forest`, `Gradient Boosting`} → `Predictions` / `Scatter Plot`.

1. Rode `python dividir_meteo_orange.py` (gera `meteo_treino_orange.csv` = 80% iniciais e `meteo_teste_orange.csv` = 20% finais, em ordem cronológica).
2. Dois widgets **File**: um com o treino, outro com o teste. Em ambos, no *File*, defina `data_hora` como **meta** (ou no `Select Columns`), `radiacao_w_m2` como **target** e as demais como features.
3. **Select Columns:** *Features* = `temperatura_c`, `umidade_pct`, `nuvens_pct`, `vento_kmh`, `hora`; *Target* = `radiacao_w_m2`; *Meta* = `data_hora`. (Faça o mesmo para o conjunto de teste; ou use um único `Select Columns` por arquivo.)
4. Visualização: `Scatter Plot` (x = `nuvens_pct` ou `hora`, y = `radiacao_w_m2`) e `Distributions`.
5. **Test & Score:** entrada *Data* = treino, *Test Data* = teste, opção **Test on test data**. Aprendizes: Linear Regression, Random Forest (300 árvores), Gradient Boosting (scikit-learn).
6. **Métricas:** MAE, MSE (se sua versão mostrar só RMSE, registre **MSE = RMSE²**) e R².
7. **Predictions:** ligue ao `Test & Score` para ver previsto × real; ou `Scatter Plot` com o valor real vs. a coluna de predição.

### Resultados (preencher)

| Algoritmo | MAE (W/m²) | MSE ((W/m²)²) | R² |
|---|---|---|---|
| Linear Regression | | | |
| Random Forest | | | |
| Gradient Boosting | | | |

Procedimento: treino = 80% iniciais, teste = 20% finais (divisão temporal, sem embaralhar).

**Análise (2–4 frases):** papel da hora (posição do sol, formato de sino ao longo do dia) e por que radiação (W/m² horizontal, estimada por reanálise) **não** é geração elétrica (depende de inclinação/orientação dos painéis, eficiência, temperatura, perdas, potência instalada; e é energia em kWh).

## Comparação com o notebook

A comparação numérica com o notebook só é direta se as divisões e os algoritmos forem equivalentes: na regressão a divisão temporal é a mesma; na classificação, o notebook usa um único split estratificado 80/20 e o Orange (se usar validação cruzada) reporta a média dos folds, então pequenas diferenças são esperadas.
