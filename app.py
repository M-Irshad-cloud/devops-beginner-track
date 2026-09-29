from flask import Flask, jsonify
import time

app = Flask(__name__)
START_TIME = time.time()

@app.route("/")
def home():
    return jsonify({"message": "Hello DevOps!"})

@app.route("/health")
def health():
    return jsonify({"status": "ok", "uptime_seconds": round(time.time() - START_TIME, 2)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
