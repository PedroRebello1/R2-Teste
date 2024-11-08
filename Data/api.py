import requests
import re
import pandas as pd

api_url = "https://maps.googleapis.com/maps/api/directions/json"
params = {
    "destination": "Patos de Minas",
    "origin": "Brasilia",
    "region": "br",
    "key": "AIzaSyDXlBod6WV_Rtarg6ZFaHmDzz6xpJAxays"
}

response = requests.get(api_url, params=params)
data = response.json()

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

unique_br = extract_br(data)
print("Unique BR numbers:", unique_br)

df = pd.read_excel('df_risco_agrupado_por_br.xlsx')

# Calculate the mean risk for the unique BRs
filtered_df = df[df.iloc[:, 0].astype(int).isin(unique_br)]

if filtered_df.empty:
    print("No matching BR numbers found in the DataFrame.")
else:
    print(filtered_df)
    average_risk = filtered_df.iloc[:, 1].mean()
    print(f"Risco médio da rota: {average_risk}")
