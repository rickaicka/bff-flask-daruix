from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json
import requests
from generate_json import generate_json_from_html
import subprocess
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

@app.route('/update_deploy', methods=['POST'])
def update_deploy():
    token = request.headers.get('X-DEPLOY-TOKEN')
    if token != os.getenv("DEPLOY_SECRET"):
        return "Unauthorized", 401
    subprocess.run(['git', 'pull', 'origin', 'main'], cwd='/opt/flask-deploy')
    subprocess.run(['docker-compose', 'down'], cwd='/opt/flask-deploy')
    subprocess.run(['docker-compose', 'up', '-d', '--build'], cwd='/opt/flask-deploy')
    return "Deploy realizado com sucesso!", 200

@app.route("/opened-buy-order", methods=["GET"])
def get_opened_buy_order():
    html_url = "http://daruix.com.br/ordemDeCompraEmAberto/cnsOrdemDeCompraEmAberto.html"
    json_output_path = "openedBuyOrder.json"

    try:
        # Faz o download do HTML remoto
        response = requests.get(html_url)
        response.raise_for_status()  # Lança exceção para erros HTTP

        # Passa o conteúdo HTML para a função que gera o JSON
        generate_json_from_html(response.text, json_output_path)

        # Lê o JSON gerado
        with open(json_output_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        return jsonify({
            "status": "success",
            "message": "Dados carregados com sucesso.",
            "pagination": {
                "total": len(data),
                "page": 1,
                "per_page": len(data)
            },
            "data": data
        }), 200

    except requests.exceptions.RequestException as req_err:
        return jsonify({
            "status": "error",
            "message": f"Erro ao acessar o HTML remoto: {str(req_err)}",
            "data": []
        }), 500

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Ocorreu um erro: {str(e)}",
            "data": []
        }), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)