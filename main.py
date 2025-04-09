from flask import Flask, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def home():
    return "Scraper de vacantes Comfama activo 🚀"

@app.route("/scraper", methods=["GET"])
def scraper():
    cargo = request.args.get("cargo", "")
    if not cargo:
        return {"error": "Falta el parámetro 'cargo'"}, 400

    try:
        url = f"https://empleo.comfama.com/ofertas?keyword={cargo}"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        card = soup.select_one(".card-job")
        if not card:
            return {"mensaje": f"No se encontraron vacantes para '{cargo}'"}

        titulo = card.select_one(".title-job").text.strip()
        empresa = card.select_one(".company-job").text.strip()
        link = "https://empleo.comfama.com" + card.select_one("a")["href"]

        return {
            "cargo": cargo,
            "titulo": titulo,
            "empresa": empresa,
            "link": link
        }

    except Exception as e:
        return {"error": str(e)}, 500

app.run(host="0.0.0.0", port=3000)
