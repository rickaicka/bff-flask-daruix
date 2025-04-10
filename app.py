from flask import Flask, jsonify
from flask_cors import CORS
import os
import json
from generate_json import generate_json_from_html

app = Flask(__name__)
CORS(app)

@app.route("/opened-buy-order", methods=["GET"])
def get_opened_buy_order():
    html_path = "cnsOrdemDeCompraEmAberto.html"
    json_output_path = "openedBuyOrder.json"

    if not os.path.exists(html_path):
        return jsonify({
            "status": "error",
            "message": "Arquivo HTML não encontrado.",
            "data": []
        }), 404

    try:
        generate_json_from_html(html_path, json_output_path)

        with open(json_output_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        return jsonify({
            "status": "success",
            "message": "Dados carregados com sucesso.",
            "pagination": {
                "total": len(data),
                "page": 1,
                "per_page": len(data)  # tudo de uma vez, sem paginação real ainda
            },
            "data": data
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Ocorreu um erro: {str(e)}",
            "data": []
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
