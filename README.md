# Quantitative Trading Bot

A Python-based automated trading bot that collects cryptocurrency price data from Binance, analyzes it using a simple quantitative strategy, and executes buy/sell orders on a mock trading exchange.

## Description

This project implements a basic quantitative trading system that:
- Fetches historical price data (K-lines) from Binance API
- Calculates price returns from the collected data
- Applies a momentum-based trading strategy to determine buy/sell signals
- Executes trades automatically on a mock exchange API (Roostoo)
- Manages wallet balances and order history

The bot uses a simple strategy: if the next period's return is expected to be higher than the current period's return, it buys; otherwise, it sells.

## Features

- **Data Collection**: Automated fetching of cryptocurrency price data from Binance
- **Data Transformation**: Calculation of price returns from raw closing prices
- **Trading Strategy**: Momentum-based decision making for buy/sell actions
- **Order Execution**: Automated placement of market orders on the exchange
- **Balance Management**: Real-time wallet balance tracking
- **Order Querying**: Historical order lookup and status checking
- **Mock Environment**: Safe testing environment using mock API

## Prerequisites

- Python 3.8 or higher
- API keys for the mock exchange (Roostoo)
- Internet connection for API calls

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd quant-trading-hack
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Create a `.env` file in the root directory:
   ```
   API_KEY=your_api_key_here
   SECRET_KEY=your_secret_key_here
   ```

2. Ensure you have valid API credentials for the Roostoo mock exchange.

## Usage

### Running the Full Trading Bot

Execute the main trading bot:
```bash
python bot.py
```

This will:
1. Load trading actions from `data/binanceDataActions.txt`
2. Check exchange information and wallet balances
3. Execute buy/sell orders based on the predetermined actions
4. Display updated balances
5. Query and save order history

### Data Collection Pipeline

To collect fresh data and generate new trading signals:

1. **Collect Exchange Data** (if needed):
   - Ensure `data/exchange.txt` contains the trading pairs you want to monitor

2. **Fetch Price Data**:
   ```bash
   cd BinanceDataCollection
   python getBinanceData.py
   ```

3. **Transform Data to Returns**:
   ```bash
   cd ../DataTransformReturns
   python transform_returns.py
   ```

4. **Determine Trading Actions**:
   ```bash
   cd ../DataBuyOrSell
   python determine_action.py
   ```

5. **Run the Bot**:
   ```bash
   cd ..
   python bot.py
   ```

### Testing

The `testing/` directory contains test scripts and sample data for validation:
- `test.py`: General testing utilities
- `getExchangeInfo.py`: Test exchange information retrieval
- Sample data files in `data/` directory

## Project Structure

```
quant-trading-hack/
├── bot.py                      # Main trading bot script
├── util.py                     # API utility functions and helpers
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── BinanceDataCollection/      # Data collection modules
│   ├── getBinanceData.py       # Orchestrates data collection
│   └── getKLines.py            # Fetches K-line data from Binance
├── DataTransformReturns/       # Data processing
│   └── transform_returns.py    # Calculates price returns
├── DataBuyOrSell/              # Trading strategy
│   └── determine_action.py     # Generates buy/sell signals
├── data/                       # Data storage
│   ├── exchange.txt            # Trading pairs configuration
│   ├── binanceDataClosingPrices.txt  # Raw price data
│   ├── binanceDataReturns.txt  # Calculated returns
│   ├── binanceDataActions.txt  # Trading actions
│   └── query_order_results.txt # Order history
└── testing/                    # Test utilities
    ├── test.py
    ├── getExchangeInfo.py
    └── ... (other test files)
```

## How It Works

1. **Data Collection**: The bot fetches recent K-line (candlestick) data from Binance for configured trading pairs.

2. **Return Calculation**: Price returns are calculated as percentage changes between consecutive periods.

3. **Strategy Application**: A simple momentum strategy analyzes return patterns:
   - If the next return > current return, signal BUY
   - Otherwise, signal SELL

4. **Order Execution**: The bot places market orders on the mock exchange based on the signals, respecting minimum order sizes and available balances.

5. **Monitoring**: All orders are tracked and results are saved for analysis.

## API Endpoints Used

- **Binance API**: `api/v3/klines` for historical price data
- **Roostoo Mock API**:
  - `/v3/exchangeInfo` - Get trading pairs info
  - `/v3/balance` - Get wallet balances
  - `/v3/place_order` - Execute trades
  - `/v3/query_order` - Check order status
  - `/v3/ticker` - Get current prices

## Important Notes

- This bot operates on a **mock trading exchange** for educational purposes
- Always test thoroughly before using with real funds
- The trading strategy is simplified and not intended for real-world use
- API rate limits and trading fees are not considered in this implementation
- Ensure your API keys are kept secure and never committed to version control

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational purposes only. Use at your own risk.