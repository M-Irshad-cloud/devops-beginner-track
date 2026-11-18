import json
from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        try:
            payload = json.loads(body)
        except ValueError:
            payload = {}
        for alert in payload.get("alerts", []):
            labels = alert.get("labels", {})
            notes = alert.get("annotations", {})
            print(
                "[" + alert.get("status", "?").upper() + "] "
                + str(labels.get("alertname")) + " severity=" + str(labels.get("severity"))
                + " :: " + str(notes.get("summary"))
                + " (since " + str(alert.get("startsAt")) + ")",
                flush=True,
            )
        self.send_response(200)
        self.end_headers()

    def log_message(self, *args):
        pass


print("webhook receiver listening on :9000", flush=True)
HTTPServer(("0.0.0.0", 9000), Handler).serve_forever()
