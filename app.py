from flask import Flask, render_template, jsonify, request
import yfinance as yf

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/history")
def history():

    symbol = request.args.get("symbol", "RELIANCE.NS")

    data = yf.download(
        symbol,
        period="5d",
        interval="5m",
        progress=False
    )

    candles = []

    for index, row in data.iterrows():
        candles.append({
            "time": int(index.timestamp()),
            "open": float(row["Open"]),
            "high": float(row["High"]),
            "low": float(row["Low"]),
            "close": float(row["Close"])
        })

    return jsonify({"candles": candles})

if __name__ == "__main__":
    app.run(debug=True)