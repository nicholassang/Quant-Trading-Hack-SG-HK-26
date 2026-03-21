from getKLines import getKLines
import json

all_data = []

dataPointsBack = 5

with open("../data/exchange.txt", "r") as file:
    data = json.load(file)

    print(f"Processing {len(data)} pairs from exchange.txt...")
    print(f"Pairs: {data}")

    with open("../data/binanceDataClosingPrices.txt", "a") as file:
        for pair in data:
            pair_str = pair.split("/")[0] + pair.split("/")[1] + "T"
            print(f"\n--- Fetching KLines for {pair_str} ---")
            closePriceDict = getKLines(pair_str, "1h", dataPointsBack)
            all_data.append(closePriceDict)

        with open("../data/binanceDataClosingPrices.txt", "w") as file:
            json.dump(all_data, file, indent=4)