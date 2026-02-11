from flask import Flask, jsonify
import socket
import os
from datetime import datetime, timezone

app = Flask(__name__)


def get_db_connection():
    """return a postgres connection if db env vars are set, otherwise none."""
    db_host = os.environ.get('DB_HOST')
    if not db_host:
        return None
    import psycopg2
    return psycopg2.connect(
        host=db_host,
        port=os.environ.get('DB_PORT', '5432'),
        dbname=os.environ.get('DB_NAME', 'appdb'),
        user=os.environ.get('DB_USER', 'appuser'),
        password=os.environ.get('DB_PASSWORD', 'apppass')
    )


def init_db():
    """create the visits table if postgres is available."""
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS visits (
                id SERIAL PRIMARY KEY,
                hostname VARCHAR(255),
                visited_at TIMESTAMP DEFAULT NOW()
            )
        """)
        conn.commit()
        cur.close()
        conn.close()


# initialize database on startup
init_db()


@app.route('/')
def index():
    conn = get_db_connection()
    if conn:
        # record this visit and get total count
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO visits (hostname) VALUES (%s)",
            (socket.gethostname(),)
        )
        conn.commit()
        cur.execute("SELECT COUNT(*) FROM visits")
        visit_count = cur.fetchone()[0]
        cur.close()
        conn.close()
        return jsonify({
            "message": "hello from docker compose!",
            "hostname": socket.gethostname(),
            "visit_count": visit_count,
            "endpoints": ["/", "/health", "/visits"]
        })

    # fallback: no database, original behavior for standalone docker demos
    return jsonify({
        "message": "Hello from Docker!",
        "hostname": socket.gethostname(),
        "endpoints": ["/", "/health"]
    })


@app.route('/health')
def health():
    health_info = {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT 1")
            cur.close()
            conn.close()
            health_info["database"] = "connected"
        except Exception:
            health_info["database"] = "disconnected"
    else:
        health_info["database"] = "not configured"

    return jsonify(health_info)


@app.route('/visits')
def visits():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "database not configured"}), 503

    cur = conn.cursor()
    cur.execute(
        "SELECT id, hostname, visited_at FROM visits ORDER BY visited_at DESC LIMIT 10"
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify({
        "recent_visits": [
            {"id": r[0], "hostname": r[1], "visited_at": r[2].isoformat()}
            for r in rows
        ]
    })


@app.route('/cs1660')
def cs():
    return jsonify({
        "status": "in-progress"
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
