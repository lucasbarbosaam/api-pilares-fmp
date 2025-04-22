
from flask import Flask, jsonify
import requests

app = Flask(__name__)
API_KEY = "cce595effe8b28f6a4cd6f2b490d441a"

def buscar_dados_fmp(ticker):
    url = f"https://financialmodelingprep.com/api/v3/profile/{ticker.upper()}?apikey={API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    return data[0] if data else None

@app.route("/api/analise/<ticker>")
def analisar(ticker):
    dados = buscar_dados_fmp(ticker.upper())
    if not dados:
        return jsonify({"erro": "Ação não encontrada ou erro na API"}), 404

    pl = dados.get("pe")
    roe = dados.get("returnOnEquity")
    dy = dados.get("lastDiv") / dados.get("price") * 100 if dados.get("lastDiv") and dados.get("price") else None

    resultados = {
        "1": "Aprovado" if pl and pl < 10 else "Reprovado",
        "4": "Aprovado" if roe and roe > 10 else "Reprovado",
        "6": "Aprovado" if dy and dy > 5 else "Reprovado"
    }

    historico = {
        "1": [pl] * 5 if pl else [],
        "4": [roe] * 5 if roe else [],
        "6": [dy] * 5 if dy else []
    }

    return jsonify({"resultados": resultados, "historico": historico})

@app.route("/")
def home():
    return "API com dados da FMP rodando com sucesso!"

import os
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
