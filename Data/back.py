import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import MinMaxScaler  # This line imports MinMaxScaler
import matplotlib.pyplot as plt


# Ler o arquivo (bota a porra desse encoding certo se não tudo explode)
df = pd.read_csv('datatran2023.csv', encoding='ISO-8859-1', sep=';', on_bad_lines='skip')

# Filtrar as colunas
colunas_desejadas = [
    'uf', 'br', 'km', 'causa_acidente', 'tipo_acidente',
    'fase_dia', 'condicao_metereologica',
    'tipo_pista', 'tracado_via', 'mortos'
]
df = df[colunas_desejadas]

# Adicionar coluna mortalidade - da pra usar case_when no R, igual no desafio do hackaton >>
# mutate(
#     Classificacao = case_when(
#       Força_Total < 200 ~ "Força Baixa",
#       Força_Total > 400 ~ "Força Alta",
#       TRUE ~ "Força Média"
#     )
df['mortalidade'] = np.where(df['mortos'] >= 2, "Alta",
                                np.where(df['mortos'] >= 1, "Moderada", "Baixa"))

# Essa porra tem q ser na mão mesmo, bota esse dicionário inteiro se não tudo explode
mapa_causas = {
    'Ausência de reação do condutor': 'Falha Humana',
    'Reação tardia ou ineficiente do condutor': 'Falha Humana',
    'Manobra de mudança de faixa': 'Falha Humana',
    'Acessar a via sem observar a presença dos outros veículos': 'Falha Humana',
    'Condutor deixou de manter distância do veículo da frente': 'Falha Humana',
    'Ingestão de álcool pelo condutor': 'Falha Humana',
    'Trafegar com motocicleta (ou similar) entre as faixas': 'Falha Humana',
    'Velocidade Incompatível': 'Falha Humana',
    'Condutor Dormindo': 'Falha Humana',
    'Demais falhas mecânicas ou elétricas': 'Falha Humana',
    'Chuva': 'Problemas da Via',
    'Entrada inopinada do pedestre': 'Problemas da Via',
    'Avarias e/ou desgaste excessivo no pneu': 'Falha Humana',
    'Pedestre cruzava a pista fora da faixa': 'Falha Humana',
    'Pista Escorregadia': 'Problemas da Via',
    'Acumulo de óleo sobre o pavimento': 'Problemas da Via',
    'Conversão proibida': 'Falha Humana',
    'Mal súbito do condutor': 'Falha Humana',
    'Transitar na contramão': 'Falha Humana',
    'Animais na Pista': 'Problemas da Via',
    'Acesso irregular': 'Problemas da Via',
    'Ultrapassagem Indevida': 'Falha Humana',
    'Transitar no Acostamento': 'Falha Humana',
    'Desrespeitar a preferência no cruzamento': 'Falha Humana',
    'Acumulo de água sobre o pavimento': 'Problemas da Via',
    'Frear bruscamente': 'Falha Humana',
    'Estacionar ou parar em local proibido': 'Falha Humana',
    'Problema com o freio': 'Falha Humana',
    'Curva acentuada': 'Problemas da Via',
    'Pedestre andava na pista': 'Falha Humana',
    'Ingestão de substâncias psicoativas pelo condutor': 'Falha Humana',
    'Área urbana sem a presença de local apropriado para a travessia de pedestres': 'Problemas da Via',
    'Ingestão de álcool ou de substâncias psicoativas pelo pedestre': 'Falha Humana',
    'Objeto estático sobre o leito carroçável': 'Problemas da Via',
    'Restrição de visibilidade em curvas horizontais': 'Problemas da Via',
    'Acumulo de areia ou detritos sobre o pavimento': 'Problemas da Via',
    'Carga excessiva e/ou mal acondicionada': 'Problemas da Via',
    'Ingestão de álcool e/ou substâncias psicoativas pelo pedestre': 'Falha Humana',
    'Deficiência do Sistema de Iluminação/Sinalização': 'Problemas da Via',
    'Transitar na calçada': 'Falha Humana',
    'Problema na suspensão': 'Falha Humana',
    'Obstrução na via': 'Problemas da Via',
    'Condutor usando celular': 'Falha Humana',
    'Demais Fenômenos da natureza': 'Problemas da Via',
    'Falta de acostamento': 'Problemas da Via',
    'Acostamento em desnível': 'Problemas da Via',
    'Redutor de velocidade em desacordo': 'Problemas da Via',
    'Falta de elemento de contenção que evite a saída do leito carroçável': 'Problemas da Via',
    'Suicídio (presumido)': 'Falha Humana',
    'Ausência de sinalização': 'Problemas da Via'
}

# Fala se alguma coisa foi falha humana ou não
# tem que ter uma coluna so pra isso, acredite
df['grupo'] = df['causa_acidente'].map(mapa_causas)


# Define pesos pra calcular o risco de cada via 
# tirei diretamente do olho do meu cu, nois pode discutir um valor melhor depois
pesos_mortalidade = {'Baixa': 2, 'Moderada': 10, 'Alta': 40}
pesos_causa = {'Falha Humana': 5, 'Problemas da Via': 15}

# Botei essas duas colunas so pra facilitar o calculo, elas sao excluidas antes de salvar o arquivo final
df['peso_mortalidade'] = df['mortalidade'].map(pesos_mortalidade)
df['peso_causa'] = df['grupo'].map(pesos_causa)

# Calcula o risco

# Agrupa tudo, pra contar quantos acidentes teve por BR
# divide por 12, pra frequencia de acidentes ser anual
df['frequencia_acidentes'] = (np.ceil(df.groupby('br')['br'].transform('count') / 12))

# calcula o risco com a formula no meu boga
df['risco'] = df['frequencia_acidentes'] * df['peso_mortalidade'] * df['peso_causa']

# ordena as vias pelo risco em ordem decrescente
# so pra ficar mais facil de visualizar
# e tira as colunas de peso que nn sao mais uteis
df = df.sort_values(by='risco', ascending=False)
df = df.drop(columns=['peso_mortalidade', 'peso_causa'])

# Exporta o df para Excel
output_path = 'df_risco_calculado.xlsx'
df.to_excel(output_path, index=False)

print(f"Salvo como: {output_path}\n No diretório: {os.getcwd()}")







# Gráfico de dispersão: fase_dia (eixo X) e condicao_metereologica (eixo Y), com o tamanho dos pontos representando a quantidade de acidentes
plt.figure(figsize=(10, 6))
scatter_data = df.groupby(['fase_dia', 'condicao_metereologica']).size().reset_index(name='quantidade_acidentes')

# Plotando os pontos com o tamanho proporcional à quantidade de acidentes
plt.scatter(
    scatter_data['fase_dia'],
    scatter_data['condicao_metereologica'],
    s=scatter_data['quantidade_acidentes'] * 10,  # Ajuste do tamanho dos pontos
    alpha=0.6,
    color='b'
)

# Configurando os eixos e o título
plt.xlabel('Fase do Dia')
plt.ylabel('Condição Meteorológica')
plt.title('Quantidade de Acidentes por Fase do Dia e Condição Meteorológica')
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

# Exibindo o gráfico
plt.show()




# -------------- #
# Essa parte é pra calcular o risco
# -------------- #



# Agrupa o DataFrame por BR e soma os valores de risco para cada BR
df_risco_agrupado = df.groupby('br', as_index=False).agg({'risco': 'sum'})

# Aplica escala logaritmca
df_risco_agrupado['Log_Risk'] = np.log10(df_risco_agrupado['risco'] + 1)  # Adding 1 to avoid log(0)

# normaliza os valores entre 0 e 10
scaler = MinMaxScaler(feature_range=(0, 10))
df_risco_agrupado['risco'] = scaler.fit_transform(df_risco_agrupado['Log_Risk'].values.reshape(-1, 1))

# joga a coluna dos logaritmo na casa do caralho
df_risco_agrupado = df_risco_agrupado.drop(columns='Log_Risk')

# Ordena de baixo pra cima de cima pra baixo
df_risco_agrupado = df_risco_agrupado.sort_values(by='risco', ascending=False)

# Exporta pra Excel
output_path_agrupado = 'df_risco_agrupado_por_br.xlsx'
df_risco_agrupado.to_excel(output_path_agrupado, index=False)

print(f"Salvo como {output_path_agrupado}\n no diretório: {os.getcwd()}")

