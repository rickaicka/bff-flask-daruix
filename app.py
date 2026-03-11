from flask import Flask, jsonify
from flask_cors import CORS
import json
import requests
from generate_json import generate_json_from_html
from flask import send_file
from ftplib import FTP
import io
from flask import Response
from ftp_client import FTPClient

app = Flask(__name__)
CORS(app)

BASE_PATH = "http://daruix.com.br"

@app.route("/opened-buy-order", methods=["GET"])
def get_opened_buy_order():
    html_url = f"{BASE_PATH}/ordemDeCompraEmAberto/cnsOrdemDeCompraEmAberto.html"
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

@app.route("/pdf/<pc>", methods=["GET"])
def list_pdfs(pc):

    try:

        if ".." in pc:
            return jsonify({"error": "Parâmetro inválido"}), 400

        ftp = FTPClient.get_connection()
        ftp.cwd(pc)

        files = ftp.nlst()

        pdf_files = [f for f in files if f.lower().endswith(".pdf")]

        return jsonify({
            "status": "success",
            "pc": pc,
            "total": len(pdf_files),
            "files": pdf_files
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/pdf/<pc>/<cod>", methods=["GET"])
def get_pdf(pc, cod):

    try:

        if ".." in pc or ".." in cod:
            return jsonify({"error": "Parâmetro inválido"}), 400

        ftp = FTPClient.get_connection()

        # gerar nome do arquivo
        pc_num = pc.replace("PC", "")
        sufixo = cod[len(pc_num):]
        arquivo = f"{pc_num}-{sufixo}.pdf"

        ftp.cwd(pc)

        def generate():

            buffer = io.BytesIO()

            def callback(data):
                buffer.write(data)
                buffer.seek(0)
                yield_data = buffer.read()
                buffer.seek(0)
                buffer.truncate()
                yield yield_data

            ftp.retrbinary(f"RETR {arquivo}", callback)

        return Response(
            generate(),
            mimetype="application/pdf",
            headers={
                "Content-Disposition": f"inline; filename={arquivo}"
            }
        )

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8000)