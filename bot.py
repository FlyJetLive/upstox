import os
import asyncio
import websockets
import json
from flask import Flask, request
from telebot import TeleBot

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv("BOT_TOKEN", "8162063342:AAGxQN9hq_M5xTvuRcBt0ONtqCZLkgbXeBI")
CHAT_ID = os.getenv("-4669657171")

bot = TeleBot(TELEGRAM_BOT_TOKEN)

# Flask App Setup
app = Flask(__name__)

# WebSocket URL (Aviator API URL)
WS_URL = "wss://game9.apac.spribegaming.com/BlueBox/websocket"

# Signal Prediction Logic
async def aviator_signal():
    async with websockets.connect(WS_URL) as ws:
        print("✅ Connected to WebSocket")

        signals = []  # List to store 10 signals

        while True:
            try:
                message = await ws.recv()
                data = json.loads(message)

                # Example data extraction (Modify as per data format)
                if 'crash_point' in data:
                    crash_point = data['crash_point']

                    # Add signal to the list
                    signals.append(f"{crash_point}x")

                    # Send signal when 10 predictions are ready
                    if len(signals) == 10:
                        signal_text = "\n".join(signals)
                        bot.send_message(CHAT_ID, f"🚨 **Aviator Signals** 🚨\n{signal_text}")
                        signals.clear()  # Clear the list for new predictions

            except Exception as e:
                print(f"❌ Error: {e}")
                await asyncio.sleep(5)  # Retry after 5 seconds

# Flask Route for Testing
@app.route('/')
def home():
    return "Flyjet Aviator Bot is Running!"

@app.route('/aviator', methods=['POST'])
def aviator_webhook():
    try:
        data = request.get_json()
        if not data:
            return "No data received", 400
        
        signal = data.get('signal')
        if signal:
            bot.send_message(CHAT_ID, f"📊 **Aviator Signal Alert:** {signal}")
            return "✅ Signal Sent Successfully", 200
        else:
            return "❗ No Signal Found", 400

    except Exception as e:
        print(f"❌ Error: {e}")
        return "❌ Internal Server Error", 500
