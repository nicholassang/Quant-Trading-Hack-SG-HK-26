import json
from util import get_balance, place_order, get_exchange_info, get_ticker, query_order

# -------------------------------
# Load data and exchange info
# -------------------------------

with open("./data/binanceDataActions.txt", "r") as f:
    actions = json.load(f)

exchange_info = get_exchange_info()
trade_pairs_info = exchange_info.get("TradePairs", {})

balances = get_balance()  # {"BTC": 0.5, "ETH": 1.2, "USD": 5000}

# -------------------------------
# Execute trades
# -------------------------------

for pair, action in actions.items():
    coin = pair.replace("USDT", "")
    pair_on_exchange = pair.replace("USDT", "/USD")

    if pair_on_exchange not in trade_pairs_info:
        print(f"Skipping {pair}: not available on exchange.")
        continue

    min_usd_order = trade_pairs_info[pair_on_exchange].get("MiniOrder", 1.0)
    amount_precision = trade_pairs_info[pair_on_exchange].get("AmountPrecision", 2)

    if action.upper() == "SELL":
        balance = float(balances.get(coin, 0)) if balances else 0
        if balance > 0:
            ticker = get_ticker(pair_on_exchange)
            last_price = ticker.get("Data", {}).get(pair_on_exchange, {}).get("LastPrice", 0)
            if last_price * balance < min_usd_order:
                print()
                print(f"Cannot SELL {coin}: order value ${last_price*balance:.2f} below MiniOrder ${min_usd_order}")
                print()
                continue
            balance = round(balance, amount_precision)
            print()
            print(f"Selling ALL {balance} {coin} for {pair}")
            result = place_order(coin, side="SELL", quantity=balance)
            print(f"Order result: {result}")
            print()
        else:
            print(f"No {coin} to sell, skipping SELL.")

    elif action.upper() == "BUY":
        usd_to_spend = max(10, min_usd_order)
        ticker = get_ticker(pair_on_exchange)
        last_price = ticker.get("Data", {}).get(pair_on_exchange, {}).get("LastPrice", 0)
        if last_price <= 0:
            print()
            print(f"Skipping {pair}: cannot get valid last price.")
            print()
            continue
        coin_qty = round(usd_to_spend / last_price, amount_precision)
        if coin_qty * last_price < min_usd_order:
            coin_qty = round(min_usd_order / last_price, amount_precision)
            print(f"Adjusted coin quantity to meet MiniOrder: {coin_qty:.{amount_precision}f} {coin}")
        print()
        print(f"Buying {coin_qty:.{amount_precision}f} {coin} (~${usd_to_spend}) for {pair}")
        result = place_order(coin, side="BUY", quantity=coin_qty)
        print(f"Order result: {result}")
        print()

# -------------------------------
# Print final balances
# -------------------------------
balances = get_balance()
print("\nUpdated wallet balances:")
for coin, amt in balances.items():
    print(f"{coin}: {amt}")

# -------------------------------
# Query all orders per pair
# -------------------------------
print("\nQuerying all orders for traded pairs... Please be patient as this may take a moment.")
all_orders = {}
for pair, _ in actions.items():
    pair_on_exchange = pair.replace("USDT", "/USD")
    queried = query_order(pair=pair_on_exchange)
    all_orders[pair] = queried

# Save queried order data
with open("./data/query_order_results.txt", "w") as f:
    json.dump(all_orders, f, indent=4)

print("\nTrading bot execution completed. Query results saved to query_order_results.txt")