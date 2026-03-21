import json

all_actions = {}

with open("../data/binanceDataReturns.txt", "r") as file:
    data = json.load(file)
    print(f"Processing {len(data)} pairs from binanceDataReturns.txt...")

    with open("../data/binanceDataActions.txt", "w") as file:
        file.write("")
        print("Cleared ../data/binanceDataActions.txt for new data...")

    with open("../data/binanceDataActions.txt", "a") as file:
        for pair, returns in data.items():
            action = "HOLD"
            print(f"\nDetermining action for {pair} with returns: {returns}")
            for i in range(1, len(returns)):
                try:
                    curr_return = float(returns[i-1])
                    next_return = float(returns[i])
                    if next_return > curr_return:
                        action = "BUY"
                    else:
                        action = "SELL"
                        break  # If we find a sell signal, we can stop checking further returns for this pair
                except ValueError as e:
                    print(f"Error converting return to float: {e}")
                    print(f"Skipping action determination for index {i} due to invalid return data.")
                    continue

            all_actions[pair] = action
        json.dump(all_actions, file, indent=4)