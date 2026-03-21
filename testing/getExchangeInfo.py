import json
from util import get_exchange_info

info = get_exchange_info()

print("Exchange Info fetched successfully. Writing to exchangeInfo.txt...")
with open("../data/exchangeInfo.txt", "w") as file:
    json.dump(info, file, indent=4, sort_keys=True)