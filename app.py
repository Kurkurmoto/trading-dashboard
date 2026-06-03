from flask import Flask, render_template, jsonify, request
import yfinance as yf
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/history")
def history():

    try:
        symbol = request.args.get("symbol", "RELIANCE.NS")

        data = yf.download(
            symbol,
            period="5d",
            interval="5m",
            progress=False
        )

        candles = []

        for index, row in data.iterrows():

            open_price = float(row["Open"].iloc[0]) if hasattr(row["Open"], "iloc") else float(row["Open"])
            high_price = float(row["High"].iloc[0]) if hasattr(row["High"], "iloc") else float(row["High"])
            low_price = float(row["Low"].iloc[0]) if hasattr(row["Low"], "iloc") else float(row["Low"])
            close_price = float(row["Close"].iloc[0]) if hasattr(row["Close"], "iloc") else float(row["Close"])

            candles.append({
                "time": int(index.timestamp()),
                "open": open_price,
                "high": high_price,
                "low": low_price,
                "close": close_price
            })

        return jsonify({"candles": candles})

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


@app.route("/test")
def test():
    return "Server Working"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)