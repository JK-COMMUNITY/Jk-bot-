import asyncio
import json
import os
from flask import Flask
from threading import Thread
from pyrogram import Client, filters

# --- CONFIG ---
API_ID = 24707647
API_HASH = "6022e379b387431289139879796e9526"
BOT_TOKEN = "8622373528:AAGC2w-J-tgMN8nJdk6VozDtv9ZB2l8gL-Y"
ADMIN_PASSKEY = "9350359379"
AUTH_FILE = "auth.json"

# IDs
EPISODE_BOT_ID = 3976861482
STORE_JSON_ID = 3904683398

# Data Handling
def load_auth():
    if os.path.exists(AUTH_FILE):
        with open(AUTH_FILE, "r") as f:
            return set(json.load(f))
    return set()

authorized_chats = load_auth()

def save_auth():
    with open(AUTH_FILE, "w") as f:
        json.dump(list(authorized_chats), f)

# --- WEB SERVER ---
app_flask = Flask(__name__)
@app_flask.route('/')
def home():
    return "JK DUAL-MIND BOT is Operational!"

def run_flask():
    app_flask.run(host='0.0.0.0', port=8080)

# --- BOT ---
app = Client("JK_DUAL_BOT", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("admin"))
async def admin_handler(client, message):
    # Sirf Store JSON bot ya main admin handle karega
    if len(message.command) > 1 and message.command[1] == ADMIN_PASSKEY:
        chat_id = message.chat.id
        authorized_chats.add(chat_id)
        save_auth()
        await message.reply(f"✅ **Database Updated!**\nSubscriber ID `{chat_id}` ko JSON mein permanent save kar diya gaya hai.")
    else:
        await message.reply("❌ **Unauthorized Access!**")

@app.on_message(filters.command("play"))
async def play_handler(client, message):
    # Check if chat id exists in JSON database
    if message.chat.id not in authorized_chats and message.chat.id != EPISODE_BOT_ID:
        return await message.reply("🚫 **Access Denied!** Pehle admin panel se register karein.")

    status_msg = await message.reply("🔄 **Episode Fetching...**")
    
    # Processing Animation
    for i in range(1, 6):
        await asyncio.sleep(0.5)
        await status_msg.edit(f"⚙️ **Processing (Mind-{EPISODE_BOT_ID}):** {'▰' * i} {i*20}%")
    
    await status_msg.edit("✅ **Episode Ready!**\n📢 **Play Command Executed successfully.**")

if __name__ == "__main__":
    Thread(target=run_flask).start()
    app.run()
