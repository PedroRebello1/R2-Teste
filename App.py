from flask import Flask, render_template, request, jsonify
import requests
import re
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from io import BytesIO
import seaborn as sns


app = Flask(__name__)

API_KEY = "AIzaSyDXlBod6WV_Rtarg6ZFaHmDzz6xpJAxays"

def extract_br(data):
    br_set = set()
    for route in data["routes"]:
        for leg in route["legs"]:
            for step in leg["steps"]:
                instructions = step["html_instructions"]
                br_match = re.search(r'BR-(\d+)', instructions)
                if br_match:
                    br_set.add(int(br_match.group(1)))
    return list(br_set)

def plot_bar_chart(df_risco_agrupado):
    df_top50 = df_risco_agrupado.sort_values(by='risco', ascending=False).head(50)

    plt.figure(figsize=(12, 6))
    sns.barplot(data=df_top50, x='br', y='risco', palette='viridis')
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.title('50 BRs com Maior Risco (Escala Logarítmica 0-10)')
    plt.xlabel('BR')
    plt.ylabel('Risco Médio')

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    image_png = buf.getvalue()
    plot_url1 = base64.b64encode(image_png).decode('utf-8')
    return plot_url1

# Função para gerar o histograma
def plot_histogram(df_risco_agrupado):
    plt.figure(figsize=(10, 6))
    sns.histplot(df_risco_agrupado['risco'], bins=15, kde=True, color='blue')
    plt.title('Distribuição do Risco Médio (Escala Logarítmica)')
    plt.xlabel('Risco Médio')
    plt.ylabel('Frequência')

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    image_png = buf.getvalue()
    plot_url2 = base64.b64encode(image_png).decode('utf-8')
    return plot_url2

# Função ajustada para plotar o gráfico com os nomes corretos das colunas
def plot_acidentes_por_fase_dia(df_acidentes, brs_especificas, df_agrupado):
    # Filtrando o DataFrame para as BRs específicas
    filtered_df = df_acidentes[df_acidentes['br'].isin(brs_especificas)]
    if filtered_df['risco'].isnull().any():
        filtered_df = filtered_df.fillna(0)  # Ou um valor padrão que faça sentido no seu contexto
    average_frequencia = round(filtered_df['frequencia_acidentes'].mean() if not filtered_df.empty else 0)

    return plot_bar_chart(df_agrupado), plot_histogram(df_agrupado), average_frequencia



@app.route('/', methods=['GET', 'POST'])
def index():

    average_risk = None
    plot_url1 = None
    plot_url2 = None
    average_frequencia = None  # Adicionado para armazenar a média de frequência


    if request.method == 'POST':
        origin = request.form['origin']
        destination = request.form['destination']
        
        # Chamada da API para calcular a rota
        api_url = "https://maps.googleapis.com/maps/api/directions/json"
        params = {
            "destination": destination,
            "origin": origin,
            "region": "br",
            "key": API_KEY
        }
        response = requests.get(api_url, params=params)
        data = response.json()

        unique_br = extract_br(data)

        # Carrega o arquivo de risco por BR e filtra para as BRs da rota
        df_risco = pd.read_excel('./Data/df_risco_agrupado_por_br.xlsx')
        filtered_df_risco = df_risco[df_risco['br'].astype(int).isin(unique_br)]
        
        # Calcula o risco médio
        if filtered_df_risco.empty:
            average_risk = "Nenhum número BR correspondente encontrado."
        else:
            average_risk = round(filtered_df_risco['risco'].mean())

        # Carrega o DataFrame de acidentes e plota o gráfico filtrado
        df_acidentes = pd.read_excel('./Data/df_risco_calculado.xlsx')
        df_agrupado = pd.read_excel('./Data/df_risco_agrupado_por_br.xlsx')
        plot_url1, plot_url2, average_frequencia = plot_acidentes_por_fase_dia(df_acidentes, unique_br, df_agrupado)

        data = {
            "average_risk": average_risk,
            "plot_url1": plot_url1,
            "plot_url2": plot_url2,
            "average_frequencia": average_frequencia
        }
        
        return jsonify(data)
    
    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)
