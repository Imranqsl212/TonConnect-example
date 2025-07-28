from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

CMC_API_KEY = "9c4ff8f7-112c-4113-abfa-cd3e203653e8"
def init_db():
    with sqlite3.connect("users.db") as conn:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            wallet TEXT,
            stars_50 INTEGER DEFAULT 0,
            stars_100 INTEGER DEFAULT 0,
            stars_150 INTEGER DEFAULT 0,
            stars_200 INTEGER DEFAULT 0,
            stars_300 INTEGER DEFAULT 0,
            stars_350 INTEGER DEFAULT 0,
            stars_500 INTEGER DEFAULT 0,
            stars_1000 INTEGER DEFAULT 0,
            stars_1500 INTEGER DEFAULT 0,
            stars_2000 INTEGER DEFAULT 0,
            stars_2500 INTEGER DEFAULT 0,
            stars_5000 INTEGER DEFAULT 0,
            stars_10000 INTEGER DEFAULT 0,
            stars_15000 INTEGER DEFAULT 0,
            stars_20000 INTEGER DEFAULT 0,
            stars_25000 INTEGER DEFAULT 0,
            stars_250 INTEGER DEFAULT 0
        )
        """)
        conn.commit()


@app.route("/ton-price")
def get_ton_price():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    params = {"symbol": "TON"}
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": CMC_API_KEY
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        return jsonify({
            "price": data["data"]["TON"]["quote"]["USD"]["price"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/save-user", methods=["POST"])
def save_user():
    data = request.json
    username = data.get("username")
    wallet = data.get("wallet")

    if not username or not wallet:
        return jsonify({"error": "Missing username or wallet"}), 400

    try:
        with sqlite3.connect("users.db") as conn:
            cur = conn.cursor()

            cur.execute("SELECT * FROM users WHERE username = ?", (username,))
            existing = cur.fetchone()

            if existing:
                cur.execute("UPDATE users SET wallet = ? WHERE username = ?", (wallet, username))
            else:
                cur.execute("""
                    INSERT INTO users (username, wallet)
                    VALUES (?, ?)
                """, (username, wallet))

            conn.commit()

        return jsonify({"message": "User saved"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route("/update-strategy", methods=["POST"])
def update_strategy():
    data = request.json
    username = data.get("username")
    strategy = data.get("strategy")
    amount = data.get("amount")

    if not username or not strategy or amount is None:
        return jsonify({"error": "Missing parameters"}), 400

    col_name = f"stars_{strategy}"
    if col_name not in {
        "stars_50", "stars_100", "stars_150", "stars_200", "stars_250",
        "stars_300", "stars_350", "stars_500", "stars_1000", "stars_1500",
        "stars_2000", "stars_2500", "stars_5000", "stars_10000", "stars_15000",
        "stars_20000", "stars_25000"
    }:
        return jsonify({"error": "Invalid strategy"}), 400

    try:
        with sqlite3.connect("users.db") as conn:
            cur = conn.cursor()
            cur.execute(f"""
                UPDATE users
                SET {col_name} = COALESCE({col_name}, 0) + ?
                WHERE username = ?
            """, (amount, username))
            conn.commit()

        return jsonify({"message": "Strategy updated"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5001)