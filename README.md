# Quantitative Trading Bot

A Python-based automated trading bot that collects cryptocurrency price data from Binance, analyzes it using a simple quantitative strategy, and executes buy/sell orders on a mock trading exchange. The bot runs a complete trading cycle every hour, automatically collecting fresh data and executing trades based on momentum indicators.

## Description

This project implements a basic quantitative trading system with automated hourly execution that:
- Fetches historical price data (K-lines) from Binance API
- Calculates price returns from the collected data
- Applies a momentum-based trading strategy to determine buy/sell signals
- Executes trades automatically on a mock exchange API (Roostoo)
- Manages wallet balances and order history
- Runs the entire pipeline on a scheduled interval

The bot uses a simple momentum strategy: if the current 1h-period's return is expected to be higher than the previous period's return for five consecutive 1h-periods, it buys; otherwise, it sells. The complete cycle (data collection → analysis → trading) runs automatically every hour.

## Features

- **Automated Pipeline**: Single command to run the complete data collection → analysis → trading cycle
- **Hourly Execution**: Automatically repeats the full trading strategy every hour using the `schedule` library
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

   This installs:
   - `requests`: For API calls to Binance and Roostoo
   - `python-dotenv`: For secure credential management
   - `schedule`: For hourly task scheduling

## Configuration

1. Create a `.env` file in the root directory:
   ```
   API_KEY=your_api_key_here
   SECRET_KEY=your_secret_key_here
   ```

2. Ensure you have valid API credentials for the Roostoo mock exchange.

## Usage

### Quick Start - Run the Complete Trading Pipeline

The simplest way to run the entire trading bot is with a single command:

```bash
python main.py
```

This will:
1. Immediately fetch fresh price data from Binance
2. Calculate returns for all configured trading pairs
3. Determine buy/sell signals based on the momentum strategy
4. Execute trades on the exchange
5. Query and save order history
6. **Automatically repeat this entire cycle every hour** until you stop the script

### Running Continuously

The bot runs indefinitely once started:

```bash
python main.py
```

The script will:
- Execute the full trading cycle immediately on startup
- Check every second for pending scheduled tasks
- Automatically run the entire strategy again one hour after the last execution
- Continue this cycle while the script is running

To stop the bot, press `Ctrl+C` in the terminal.

### Manual Execution - Run Individual Steps

If you prefer to run the trading pipeline manually without scheduling, you can execute each step separately:

1. **Collect Price Data from Binance**:
   ```bash
   cd BinanceDataCollection
   python getBinanceData.py
   ```

2. **Transform Data to Returns**:
   ```bash
   cd ../DataTransformReturns
   python transform_returns.py
   ```

3. **Determine Trading Actions**:
   ```bash
   cd ../DataBuyOrSell
   python determine_action.py
   ```

4. **Execute Trades**:
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
├── main.py                     # ⭐ Entry point - orchestrates the complete trading cycle
├── bot.py                      # Executes trades based on determined actions
├── util.py                     # API utility functions and helpers
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── BinanceDataCollection/      # Data collection from Binance
│   ├── getBinanceData.py       # Fetches K-line data from Binance API
│   └── getKLines.py            # Helper for K-line requests
├── DataTransformReturns/       # Data processing/analysis
│   └── transform_returns.py    # Calculates returns from prices
├── DataBuyOrSell/              # Trading signal generation
│   └── determine_action.py     # Generates BUY/SELL/HOLD signals
├── data/                       # Data storage and configuration
│   ├── exchange.txt            # ⭐ Configured trading pairs (customize this)
│   ├── binanceDataClosingPrices.txt  # Raw price data (generated)
│   ├── binanceDataReturns.txt  # Calculated returns (generated)
│   ├── binanceDataActions.txt  # Trading signals (generated)
│   └── query_order_results.txt # Order history (generated)
└── testing/                    # Test utilities
    ├── test.py
    ├── getExchangeInfo.py
    └── ... (other test files)
```

**Key files:**
- `main.py` - Start here! Runs everything automatically and on schedule
- `data/exchange.txt` - Edit this to customize which trading pairs to monitor
- `.env` - Create this with your API credentials

## How It Works

### Complete Pipeline Orchestration

`main.py` is the orchestrator that handles the complete trading workflow. When you run `python main.py`, it executes four sequential scripts that form the complete trading cycle:

1. **Data Collection** (`getBinanceData.py`):
   - Reads configured trading pairs from `data/exchange.txt`
   - Fetches recent K-line (candlestick) data from Binance API
   - Saves raw closing prices to `data/binanceDataClosingPrices.txt`

2. **Return Calculation** (`transform_returns.py`):
   - Reads raw price data from `binanceDataClosingPrices.txt`
   - Calculates percentage returns between consecutive time periods
   - Saves returns to `data/binanceDataReturns.txt`

3. **Strategy Application** (`determine_action.py`):
   - Analyzes return patterns using a momentum-based strategy
   - Compares consecutive returns to generate BUY/SELL/HOLD signals
   - Outputs trading actions to `data/binanceDataActions.txt`

4. **Order Execution** (`bot.py`):
   - Loads predetermined trading actions
   - Checks wallet balances and exchange trading pair info
   - Places market orders on the mock exchange
   - Saves order history to `data/query_order_results.txt`

### Automatic Scheduling

After the initial execution, `main.py`:
- Uses the `schedule` library to register a job
- Automatically repeats the entire 4-step cycle every hour
- Checks for pending jobs every second
- Continues indefinitely until the script is manually stopped

This means fresh market data is collected and fresh trades are executed automatically every hour without any manual intervention.

### Trading Strategy Details

The momentum strategy works as follows for each trading pair:
- If the next period's expected return > current period's return → **BUY**
- If the next period's expected return ≤ current period's return → **SELL**
- Respects minimum order sizes and available wallet balances
- Skips trading pairs not available on the exchange

## API Endpoints Used

- **Binance API**: `api/v3/klines` for historical price data
- **Roostoo Mock API**:
  - `/v3/exchangeInfo` - Get trading pairs info
  - `/v3/balance` - Get wallet balances
  - `/v3/place_order` - Execute trades
  - `/v3/query_order` - Check order status
  - `/v3/ticker` - Get current prices

## Important Notes

- This bot operates on a **mock trading exchange** for educational and testing purposes
- **Requires `.env` file** with valid API credentials to run (see Configuration section)
- The bot will run indefinitely once started with `python main.py` - use `Ctrl+C` to stop
- Each trading cycle fetches fresh data and executes new trades, so **network connectivity is required**
- Trading happens every hour automatically - monitor the console output to verify successful execution
- The trading strategy is simplified and not intended for real-world production use
- API rate limits and trading fees are not considered in this implementation
- **Always secure your `.env` file** - never commit API keys to version control
- Test thoroughly in this mock environment before considering any real trading scenarios

## Configuration

### Customize Trading Pairs

Edit `data/exchange.txt` to specify which cryptocurrency pairs to trade:

```json
[
    "BTC/USD",
    "ETH/USD",
    "SOL/USD",
    "XRP/USD"
]
```

The bot will automatically fetch and trade these pairs.

### API Credentials

Create a `.env` file in the project root:

```
API_KEY=your_roostoo_api_key
SECRET_KEY=your_roostoo_secret_key
```

These credentials are required for placing orders on the mock exchange.