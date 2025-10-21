from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import urllib.request
import json

def consultar_cep(cep):
    """Consulta um único CEP na API ViaCEP."""
    url = f"https://viacep.com.br/ws/{cep}/json/"
    try:
        with urllib.request.urlopen(url) as response:
            dados = json.loads(response.read().decode())
            if "erro" in dados:
                return {"cep": cep, "erro": "CEP não encontrado"}
            return dados
    except Exception as e:
        return {"cep": cep, "erro": str(e)}

class MeuServidor(BaseHTTPRequestHandler):
    def do_GET(self):
        """Trata requisições GET, ex: /?ceps=01001000,30140071"""
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)

        if "ceps" not in query_params:
            self.send_response(400)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"erro": "Parâmetro 'ceps' obrigatório"}).encode("utf-8"))
            return

        ceps_lista = query_params["ceps"][0].split(",")
        resultados = [consultar_cep(cep.strip()) for cep in ceps_lista]

        resposta = json.dumps(resultados, ensure_ascii=False, indent=4)
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(resposta.encode("utf-8"))

if __name__ == "__main__":
    porta = 8000
    servidor = HTTPServer(("0.0.0.0", porta), MeuServidor)
    print(f"🚀 Servidor rodando em http://localhost:{porta}")
    print("👉 Exemplo: http://localhost:8000/?ceps=01001000,30140071")
    servidor.serve_forever()
