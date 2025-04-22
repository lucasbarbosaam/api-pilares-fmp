
from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)
API_KEY = "cce595effe8b28f6a4cd6f2b490d441a"

def buscar_dados_fmp(ticker):
    url = f"https://financialmodelingprep.com/api/v3/profile/{ticker.upper()}?apikey={API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return None
        data = response.json()
        return data[0] if isinstance(data, list) and data else None
    except:
        return None

@app.route("/api/analise/<ticker>")
def analisar(ticker):
    dados = buscar_dados_fmp(ticker)
    if not dados:
        return jsonify({"erro": "Ação não encontrada ou erro na API"}), 404

    pl = dados.get("pe")
    roe = dados.get("returnOnEquity")
    dy = None
    if dados.get("lastDiv") is not None and dados.get("price"):
        dy = (dados.get("lastDiv") / dados.get("price")) * 100

    resultados = {
        "1": "Aprovado" if pl is not None and pl < 10 else "Reprovado",
        "4": "Aprovado" if roe is not None and roe > 10 else "Reprovado",
        "6": "Aprovado" if dy is not None and dy > 5 else "Reprovado"
    }

    historico = {
        "1": [pl] * 5 if pl is not None else [],
        "4": [roe] * 5 if roe is not None else [],
        "6": [dy] * 5 if dy is not None else []
    }

    return jsonify({"resultados": resultados, "historico": historico})

@app.route("/")
def home():
    return "API com dados da FMP (ações americanas) rodando com sucesso!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
