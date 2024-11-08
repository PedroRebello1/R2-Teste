import pandas as pd
import openpyxl

df = pd.read_excel('df_risco_calculado.xlsx')
print(f"colunas df_risco_calculado.xlsx : {df.columns}")

df2 = pd.read_excel('df_risco_agrupado_por_br.xlsx')
print(f"colunas df_risco_agrupado_por_br.xlsx : {df2.columns}")