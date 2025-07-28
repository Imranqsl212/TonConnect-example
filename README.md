# 💸 TON Wallet Integration Demo – Vakuum AutoBuy

This project is a **full-stack example** that demonstrates how to connect a [TON blockchain](https://ton.org/) wallet using **TonConnect**, process payments in **TON**, and update user purchase records via a **Flask** backend with a **SQLite** database.

> 🔐 It includes front-end and back-end code for a working system that tracks purchases of “stars” (in-app currency) tied to different Telegram bots.

---

## 🚀 Features

* **TON Wallet Integration** via TonConnect.
* **Dynamic Transaction Calculation** based on TON/USD price.
* **Real-time wallet connection detection** and user identification.
* **Backend in Flask** to:

  * Save connected wallet and username.
  * Store user balances per “strategy”.
  * Get real-time TON price from CoinMarketCap API.
* **Frontend in HTML + JS** with:

  * Wallet UI
  * Strategy selector
  * TON payment & API requests

---

## 🌐 Live Frontend (HTML + JS)

```html
<script src="https://unpkg.com/@tonconnect/ui@latest/dist/tonconnect-ui.min.js"></script>
```

* When a user connects their wallet:

  * They’re asked to enter their Telegram username.
  * Username + Wallet Address are saved to backend (`/save-user`).
* User selects a strategy (like `@VakuumAutoBot150`) and enters how many stars to buy.
* App calculates USD cost → converts to TON (via `/ton-price`).
* Sends TON transaction.
* On success:

  * Stars are issued via external API (`/v1/stars/payment`)
  * Database updates via `/update-strategy`.

---

## 🧠 Technologies Used

| Tech                                        | Purpose                       |
| ------------------------------------------- | ----------------------------- |
| HTML + JS                                   | Frontend, UI interactions     |
| [TonConnect UI](https://ton.org/tonconnect) | Crypto wallet connection      |
| Flask                                       | REST backend                  |
| SQLite                                      | Lightweight local database    |
| CoinMarketCap API                           | Fetching real-time TON price  |
| CORS                                        | Cross-Origin Request Handling |

---

## 🛠 Backend Setup (Flask)

```bash
pip install flask flask-cors requests
```

Then run:

```bash
python app.py
```

Runs server on: `http://127.0.0.1:5001/`

### 📂 Endpoints

| Method | URL                | Description                       |
| ------ | ------------------ | --------------------------------- |
| GET    | `/ton-price`       | Returns TON price in USD          |
| POST   | `/save-user`       | Saves or updates user wallet info |
| POST   | `/update-strategy` | Increases star count for user     |

---

## 🧪 Example Transaction Flow

1. User connects wallet via TonConnect.
2. Prompted to input Telegram username (stored in `localStorage`).
3. Selects strategy and stars amount.
4. JS fetches TON/USD price.
5. Calculates TON amount + 10% fee.
6. Sends TON payment.
7. Updates backend with new star count.
8. Calls external Telegram API to issue stars.

---

## 📦 Database Schema (SQLite)

```sql
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    wallet TEXT,
    stars_50 INTEGER DEFAULT 0,
    stars_100 INTEGER DEFAULT 0,
    ... -- one column for each strategy
);
```

Each column like `stars_5000`, `stars_250`, etc. holds the user's balance per strategy.

---

## 📌 Notes

* You need a [CoinMarketCap API Key](https://coinmarketcap.com/api/) and replace the placeholder in the Flask code.
* Replace `"your frag api key"` with your actual `stars/payment` API key.
* Works best with local server setup (or deploy via Render, Replit, Railway, etc.).

---

## 🧠 Why this Project is Useful

This is a great **starter template** for:

* Telegram bot monetization via TON.
* Web3 onboarding with TonConnect.
* Learning backend + wallet integration.
* Creating strategy-based purchases tracked per user.

---

## 💬 Contact

Made with ❤️ by [Imran Zakirov](https://t.me/gothamneedme)

