
from flask import Flask, jsonify
import requests
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
API_KEY = "cce595effe8b28f6a4cd6f2b490d441a"

def get_profile(ticker):
    url = f"https://financialmodelingprep.com/api/v3/profile/{ticker}?apikey={API_KEY}"
    r = requests.get(url)
    return r.json()[0] if r.ok and isinstance(r.json(), list) and r.json() else None

def get_ratios_ttm(ticker):
    url = f"https://financialmodelingprep.com/api/v3/ratios-ttm/{ticker}?apikey={API_KEY}"
    r = requests.get(url)
    return r.json()[0] if r.ok and isinstance(r.json(), list) and r.json() else None

@app.route("/api/analise/<ticker>")
def analisar(ticker):
    ticker = ticker.upper()
    profile = get_profile(ticker)
    ratios = get_ratios_ttm(ticker)

    if not profile and not ratios:
        return jsonify({"erro": "Ação não encontrada ou erro na API"}), 404

    pl = ratios.get("peRatioTTM") if ratios else None
    roe = ratios.get("returnOnEquityTTM") if ratios else None
    dy = (profile.get("lastDiv") / profile.get("price") * 100) if profile and profile.get("lastDiv") and profile.get("price") else None

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
    return "API com dados da FMP (indicadores avançados) rodando com sucesso!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
