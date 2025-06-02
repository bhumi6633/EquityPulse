from flask import Flask, render_template, request, jsonify
import yfinance as yf

app = Flask(__name__)

def get_stock_price(symbol):
    stock = yf.Ticker(symbol)
    info = stock.info
    data = stock.history(period="1d")
    if data.empty:
        return None
    price = round(data["Close"].iloc[-1], 2)
    prev_close = info.get("previousClose", price)
    change = round(price - prev_close, 2)
    percent = round((change / prev_close) * 100, 2) if prev_close else 0
    return {
        "name": info.get("shortName", symbol),
        "symbol": symbol.upper(),
        "price": price,
        "change": change,
        "percent_change": percent
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_price', methods=['POST'])
def get_price():
    symbol = request.form.get("symbol", "").upper()
    try:
        result = get_stock_price(symbol)
        if not result:
            return jsonify({"error": "Invalid or unknown symbol."})
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/get_history', methods=['POST'])
def get_history():
    symbol = request.form.get("symbol", "").upper()
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="7d")
        if hist.empty:
            return jsonify({"error": "No history available."})
        return jsonify({
            "dates": [d.strftime("%b %d") for d in hist.index],
            "prices": [round(p, 2) for p in hist["Close"]]
        })
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
