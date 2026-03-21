from getKLines import getKLines
import json

with open("exchange.txt", "r") as file:
    data = json.load(file)

    print(f"Processing {len(data)} pairs from exchange.txt...")
    print(f"Pairs: {data}")

    with open("../data/binanceDataClosingPrices.txt", "a") as file:
        file.write("KLines Data\n")
        for pair in data:
            pair = pair.split("/")[0] + pair.split("/")[1] + "T"  # e.g., Convert "BTC/USD" to "BTCUSDT"
            print(f"\n--- Fetching KLines for {pair} ---")
            closePriceDict = getKLines(pair, "1h", 5)
            json.dump(closePriceDict, file, indent=4)
            file.write("\n\n")