import os
import subprocess
import sys
import schedule
import time

def do_strat():
    print("Starting strategy execution...")
    files = [
        "./BinanceDataCollection/getBinanceData.py", 
        "./DataTransformReturns/transform_returns.py", 
        "./DataBuyOrSell/determine_action.py", 
        "./bot.py"
    ]

    for file in files:
        script_path = os.path.abspath(file)
        script_dir = os.path.dirname(script_path)
        print(f"Running {file} from {script_dir}...")
        # Set working directory to script directory so relative paths inside the script resolve correctly
        subprocess.run([sys.executable, script_path], cwd=script_dir, check=True)

    print("All files finished.")

# Run the strategy immediately on startup
do_strat()

# Schedule the job to run every hour
schedule.every().hour.do(do_strat)

# Keep the script running to check for pending jobs
while True:
    schedule.run_pending()
    time.sleep(1)