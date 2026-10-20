from flask import Flask, jsonify, request, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)
START_TIME = time.time()

REQUEST_COUNT = Counter(
    "http_requests_total", "Total HTTP requests", ["method", "endpoint", "status"]
)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds", "Request latency in seconds", ["endpoint"]
)


@app.before_request
def start_timer():
    request.start_time = time.time()


@app.after_request
def record_metrics(response):
    # Use the route pattern, not the raw path. Otherwise every random 404 URL
    # creates a new time series and memory grows without limit.
    endpoint = request.url_rule.rule if request.url_rule else "unmatched"
    REQUEST_COUNT.labels(request.method, endpoint, response.status_code).inc()
    REQUEST_LATENCY.labels(endpoint).observe(time.time() - request.start_time)
    return response


@app.route("/")
def home():
    return jsonify({"message": "Hello DevOps!"})


@app.route("/health")
def health():
    return jsonify({"status": "ok", "uptime_seconds": round(time.time() - START_TIME, 2)})


@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
