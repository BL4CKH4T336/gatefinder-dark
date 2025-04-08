from flask import Flask
import subprocess
import threading
import time
import os
import psutil

app = Flask(__name__)

bot_process = None

def is_bot_running():
    """Check if bot.py is running."""
    for proc in psutil.process_iter(['pid', 'cmdline']):
        if proc.info['cmdline'] and 'bot.py' in proc.info['cmdline']:
            return True
    return False

def run_bot():
    """Run bot.py in background forever."""
    global bot_process
    if not is_bot_running():
        print("[INFO] Starting bot.py...")
        bot_process = subprocess.Popen(['python3', 'bot.py'])
    else:
        print("[INFO] bot.py already running.")

def monitor_bot():
    """Keep checking bot.py every 10 minutes."""
    while True:
        if not is_bot_running():
            print("[WARNING] bot.py is not running! Restarting...")
            run_bot()
        else:
            print("[INFO] bot.py is alive.")
        time.sleep(600)  # check every 10 minutes

@app.route('/')
def home():
    return '<h1 style="color:white; background:black; padding:50px; text-align:center;">Welcome to the real world of <span style="color:lime;">darkkk</span></h1>'

if __name__ == '__main__':
    print("[INIT] Launching Flask app and monitoring bot.py")
    threading.Thread(target=monitor_bot, daemon=True).start()
    run_bot()
    app.run(host='0.0.0.0', port=5000)
