from flask import Flask, render_template, request, jsonify
import yfinance as yf

app = Flask(__name__)

# Function to fetch stock price
def get_stock_price(symbol):
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")
        return round(data["Close"].iloc[-1], 2)
    except Exception as e:
        return str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_price', methods=['POST'])
def get_price():
    symbol = request.form.get("symbol").upper()
    price = get_stock_price(symbol)
    return jsonify({"symbol": symbol, "price": price})

if __name__ == '__main__':
    app.run(debug=True)
