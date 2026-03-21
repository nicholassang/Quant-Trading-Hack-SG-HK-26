import requests

# Define the API endpoint URL
url = "https://api.binance.com/api/v3/klines"

def getKLines(symbol, interval, limit):
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }

    closePriceDict = {}

    # Send a GET request to the URL
    response = requests.get(url, params=params)

    # Check if the request was successful 
    if response.status_code == 200:
        data = response.json()
        closePriceArr = []
        for kline in data:
            closePriceArr.append(kline[4])  # Append the close price (index 4) of each kline
        closePriceDict[symbol] = closePriceArr
        print(f"Close prices for {symbol}: {closePriceDict}")
    else:
        print(f"Failed to fetch {symbol}. Status code: {response.status_code}")
        print(f"Response body: {response.text}")

    return closePriceDict

""" getKLines("BTCUSDT", "1h", 5) """