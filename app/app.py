from flask import Flask, jsonify
import socket
from datetime import datetime, timezone

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        "message": "Hello from Docker!",
        "hostname": socket.gethostname(),
        "endpoints": ["/", "/health"]
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
