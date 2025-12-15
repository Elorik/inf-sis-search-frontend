from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs

from data_layer import add_document, load_documents
from search_engine import search_documents

HOST = "127.0.0.1"
PORT = 8000


class Handler(BaseHTTPRequestHandler):
    def _send_json(self, status: int, payload: dict | list):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(json.dumps(payload, ensure_ascii=False).encode("utf-8"))

    def do_OPTIONS(self):
        self._send_json(200, {})

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/":
            docs = load_documents()
            self._send_json(200, {"status": "ok", "docs_count": len(docs)})
            return

        if parsed.path == "/search":
            params = parse_qs(parsed.query)
            query = params.get("query", [""])[0]
            doc_type = params.get("doc_type", ["all"])[0]          # all | news | opinion | scientific
            entity_type = params.get("entity_type", ["all"])[0]    # all | PER | ORG | LOC | DATE
            entity_value = params.get("entity_value", [""])[0]

            results = search_documents(
                query=query,
                doc_type=doc_type,
                entity_type=entity_type,
                entity_value=entity_value,
            )
            self._send_json(200, results)
            return

        self._send_json(404, {"error": "not found"})

    def do_POST(self):
        parsed = urlparse(self.path)

        if parsed.path == "/admin/documents":
            length = int(self.headers.get("Content-Length", 0))
            body_bytes = self.rfile.read(length)

            try:
                payload = json.loads(body_bytes.decode("utf-8"))
            except json.JSONDecodeError:
                self._send_json(400, {"error": "invalid json"})
                return

            doc = add_document(payload)
            self._send_json(200, doc)
            return

        self._send_json(404, {"error": "not found"})


def run():
    print("DEBUG: app.py started")
    server = HTTPServer((HOST, PORT), Handler)
    print(f"Server running at http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    run()

print("DEBUG: app.py started", flush=True)
print(f"Server running at http://{HOST}:{PORT}", flush=True)
