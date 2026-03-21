import json

all_returns = {}

with open("../data/binanceDataClosingPrices.txt", "r") as file:
    data = json.load(file)
    print(f"Processing {len(data)} pairs from binanceDataClosingPrices.txt...")

    with open("../data/binanceDataReturns.txt", "w") as file:
        file.write("")
        print("Cleared ../data/binanceDataReturns.txt for new data...")

    with open("../data/binanceDataReturns.txt", "a") as file:
        for pair_dict in data:
            for pair, closePrices in pair_dict.items():
                returns = []
                print(f"\nCalculating returns for {pair} with close prices: {closePrices}")
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
                all_returns[pair] = returns
                
        json.dump(all_returns, file, indent=4)
