"""Divide meteo_regressao_orange.csv em treino (80% iniciais) e teste (20% finais),
preservando a ordem cronológica, para usar em Test & Score (Test on test data) no Orange.
Uso: python dividir_meteo_orange.py
"""
import pandas as pd

df = pd.read_csv("meteo_regressao_orange.csv", encoding="utf-8-sig").sort_values("data_hora")
corte = int(len(df) * 0.80)               # mesmo corte do notebook
df.iloc[:corte].to_csv("meteo_treino_orange.csv", index=False, encoding="utf-8-sig")
df.iloc[corte:].to_csv("meteo_teste_orange.csv", index=False, encoding="utf-8-sig")
print(f"treino: {corte} linhas | teste: {len(df) - corte} linhas")
