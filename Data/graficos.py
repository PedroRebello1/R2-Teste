import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar os DataFrames
df = pd.read_excel('df_risco_calculado.xlsx')
df_risco_agrupado = pd.read_excel('df_risco_agrupado_por_br.xlsx')

# Converter a coluna 'br' para string para evitar problemas de merge
df['br'] = df['br'].astype(str)
df_risco_agrupado['br'] = df_risco_agrupado['br'].astype(str)

# Ordenar o DataFrame pelos maiores riscos e selecionar as top 20 BRs
df_top50 = df_risco_agrupado.sort_values(by='risco', ascending=False).head(50)

# Gráfico de Barras: Top 20 BRs com maior risco
plt.figure(figsize=(12, 6))
sns.barplot(data=df_top50, x='br', y='risco', palette='viridis')
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.title('50 BRs com Maior Risco (Escala Logarítmica 0-10)')
plt.xlabel('BR')
plt.ylabel('Risco Médio')
plt.show()

# 2. Histograma: Distribuição do Risco em Escala Logarítmica
plt.figure(figsize=(10, 6))
sns.histplot(df_risco_agrupado['risco'], bins=15, kde=True, color='blue')
plt.title('Distribuição do Risco Médio (Escala Logarítmica)')
plt.xlabel('Risco Médio')
plt.ylabel('Frequência')
plt.show()
