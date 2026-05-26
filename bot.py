import asyncio
from flask import Flask
from threading import Thread
from pyrogram import Client, filters

# --- CONFIG ---
API_ID = 24707647
API_HASH = "6022e379b387431289139879796e9526"
BOT_TOKEN = "8622373528:AAGC2w-J-tgMN8nJdk6VozDtv9ZB2l8gL-Y"
ADMIN_PASSKEY = "9350359379"

authorized_chats = set()

# --- WEB SERVER (स्टेबिलिटी के लिए) ---
app_flask = Flask(__name__)
@app_flask.route('/')
def home():
    return "JK COM BOT is Live!"

def run_flask():
    app_flask.run(host='0.0.0.0', port=8080)

# --- BOT ---
app = Client("JK_MUSIC_BOT", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("admin"))
async def admin_handler(client, message):
    if len(message.command) > 1 and message.command[1] == ADMIN_PASSKEY:
        authorized_chats.add(message.chat.id)
        await message.reply("✅ **चैट अब ऑथराइज्ड है।**")
    else:
        await message.reply("🔑 **पासकी गलत है!**")

@app.on_message(filters.command("play"))
async def play_handler(client, message):
    if message.chat.id not in authorized_chats:
        return await message.reply("🚫 **आप एडमिन नहीं हैं!**")

    # प्रोफेशनल प्रोसेसिंग एनिमेशन (वॉल्यूम टाइप एनीमेशन)
    animation = [
        "▰▱▱▱▱▱▱▱ 10%",
        "▰▰▱▱▱▱▱▱ 30%",
        "▰▰▰▱▱▱▱▱ 50%",
        "▰▰▰▰▱▱▱▱ 70%",
        "▰▰▰▰▰▰▱▱ 90%",
        "▰▰▰▰▰▰▰▰ 100%"
    ]

    status_msg = await message.reply("🔄 **प्रोसेसिंग शुरू हो रही है...**")

    for frame in animation:
        await asyncio.sleep(0.6)  # एनीमेशन की स्पीड
        await status_msg.edit(f"⚙️ **सिस्टम लोड हो रहा है:**\n\n`{frame}`")

    await status_msg.edit("✅ **सफलता! एपिसोड लाइव हो गया है।**")

if __name__ == "__main__":
    Thread(target=run_flask).start()
    app.run()
