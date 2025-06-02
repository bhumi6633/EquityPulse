from flask import Flask, render_template, request, jsonify
import yfinance as yf

app = Flask(__name__)

# Function to fetch stock info
def get_stock_price(symbol):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="2d")  # Get 2 days of data
        if hist.empty or len(hist) < 2:
            return {"error": "No data found for the given symbol."}

        current_price = round(hist["Close"].iloc[-1], 2)
        previous_price = round(hist["Close"].iloc[-2], 2)
        change = round(current_price - previous_price, 2)
        percent_change = round((change / previous_price) * 100, 2)

        info = stock.info
        name = info.get("shortName", symbol)

        return {
            "symbol": symbol.upper(),
            "name": name,
            "price": current_price,
            "change": change,
            "percent_change": percent_change
        }
    except Exception as e:
        return {"error": str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_price', methods=['POST'])
def get_price():
    symbol = request.form.get("symbol", "").upper()
    data = get_stock_price(symbol)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
