import json

with open("../data/binanceDataClosingPrices.txt", "r") as file:
    data = json.load(file)
    print(f"Processing {len(data)} pairs from binanceDataClosingPrices.txt...")

    with open("../data/binanceDataReturns.txt", "w") as f:
        f.write("")
        print("Cleared ../data/binanceDataReturns.txt for new data...")

    with open("../data/binanceDataReturns.txt", "a") as file:
        for pair, closePrices in data.items():
            returns = []
            for i in range(1, len(closePrices)):
                try:
                    prev_price = float(closePrices[i-1])
                    curr_price = float(closePrices[i])
                    ret = (curr_price - prev_price) / prev_price
                    returns.append(ret)
                except ValueError as e:
                    print(f"Error converting close price to float: {e}")
                    print(f"Skipping return calculation for index {i} due to invalid price data.")
                    continue

            json.dump({pair: returns}, file, indent=4)