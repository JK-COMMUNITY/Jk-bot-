import asyncio
import json
import gspread
from pyrogram import Client, filters
from pytgcalls import PyTgCalls, idle
from pytgcalls.types import AudioPreamble, MediaStream
from oauth2client.service_account import ServiceAccountCredentials

# --- CONFIGURATION ---
API_ID = 24707647
API_HASH = "6022e379b387431289139879796e9526"
BOT_TOKEN = "8622373528:AAGC2w-J-tgMN8nJdk6VozDtv9ZB2l8gL-Y"
PRIVATE_CHANNEL_ID = -1001234567890

# --- GOOGLE SHEETS SETUP (JSON INCLUDED IN CODE) ---
json_data = {
    "type": "service_account",
    "project_id": "civic-environs-450612-v6",
    "private_key_id": "fad29f536816663c797e498da001d16cc0da4cac",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCagmqclstBgOD2\nwMWa2WhOKUx9Dcly70rqKvG4Mo7stg8sSejpGdt7ovjBpJujbOe0Q3qyWoinstEj\nxhcqYOM26l1sZwbOs/Q1bgfWsSWgAS5NLokuUNVfLWnNbEs/j5N9zkIq5WJzPHo1\nMi+SSZq3LhqK2CDyYPCEqvf6kFoQZy7w+DQNDLzq8AUqMoc81qQNQv+oOVAtn5J/\nWrq4UfESDoyGSBjxtqFAmW5AZzhL/QHn7o+/uPBE4QwbuuYQc2O77OXcr8l5qzIO\n4yhbGoMmgEEmlMuPlTHU9ErD4TWZefRN0FxeVEUFNJa3+YNzO9tFC5SlYdb6P+ZM\n8YeI/8RpAgMBAAECggEAPcOghpQpEDhKtZj95Ra/gW806lCWlOFfWxhrpCxhwfJN\nQnERMA1sFZJiSlZY+Q1R2leXNrDGK/Npcxl+rSwp6Avr6KeOqxZ4qtsfOw15curF\n7YiKwf8CLJfk0X9W3UOxu/q1rJwhrNsiJx22so3F0TAW4CXhlcJ2ozINCxalSiS2\nNjJZ1vWH/zy/2NzpquvHZLNtaoDl4alpBqsqTrgWrOr21m0PbJJ3AG061KpZnca3\nNBPw4vtzU5VuM6fAGzGaFnTfihnyJ25W/luW3SdVSS1Egv84a5EvRAJ7LRsNNbk2\nshOWZw6niHU1O7PclnT1ulqbMKwRZ0oW9qkKvboYWQKBgQDIXxxXrGB+aLnYP3zE\naMz4MUmW+UJlk02wzQskIHqHpf05he0m7EmbWkyZ9FVpM5iGzqE1JdNHpI8PLmYZ\nbTHmYWx0ozxYqRgV9mlOAo2pRGf27DZdyWMlavKZbAZcQlsjNNSqFrbiJzC9kovT\nqJJZtfq+DP7NLSW1b8PyMzMOSwKBgQDFZ8a25mU7vtkFSVUEAeRmGppjLEEyiXDy\n8+CcYQ6lyDf7zeofU5nSI8gY5VFmk1ZXYpk7V5Ux97sYTAAUqm5eVmNhlIJPjs5X\nhT/Q/zIMPeKbaLWFLfmoTPytk0jMKRJiDvlitkJ21G51/kWtqIYrb/0Gj9+HjNkq\n0VWsQIw3mwKBgANEseSoNia5tJZXasSVZQqDW0zwIeogPfstTQo40WbXCUtf6N9i\nqUy0a11zg9Ukd09znWONi2W2xHKd8iJmCpNUcX1xkDFuCKuLCmqwVfk12XBIqBZd\ni5V3qh9giLYGixAG85UWq8MCmqPs+QTp0gFOm5lwAtP78YqFGTAhL6sDAoGAec3c\nyUJEOKc71Y04De709SN5G7RUzlAMB3z/nL4ugZCXKqIV0hqNkSJO9z2YCoji/6xx\nDDKwdlJ7eTR74ESBMWhwjedKuLhPDaXEiLrOMMuGpYnoZzLFF1nZl2iHxKGbHDJN\nIuF/BT9yoQ+yAsM3dln1cDUaIdOAtHDSQiTZ3/0CgYAFhDpXKxx9gaB7hFY5zOgm\nOQCeGxktendARfjW94rBCvPkmAtyoVO/p7ui+Lh71sbKT4R446DNDBE/E+wGBJEn\nwcHnX03f231OLhTo8cLgwbkAlW3AyrOzoTrrUKE8pdLeYCTnfNfTczKnKApC1RtJ\nVLOY1NGnGplIbILsAy0miQ==\n-----END PRIVATE KEY-----",
    "client_email": "jk-bot-database@civic-environs-450612-v6.iam.gserviceaccount.com",
    "client_id": "102443320267586720857",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/jk-bot-database%40civic-environs-450612-v6.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

creds = ServiceAccountCredentials.from_json_keyfile_dict(json_data, ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'])
client_gs = gspread.authorize(creds)
sheet = client_gs.open_by_key('1WI2ZUIQ0Vw2HzGg1_aw8n_INjKeivbsVFAQV3ShIf4').sheet1

app = Client("JK_MUSIC_BOT", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
pytgcalls = PyTgCalls(app)

# --- BOT LOGIC ---
@app.on_message(filters.command("play"))
async def play_handler(client, message):
    await message.reply("🙏 **नमस्ते! मैं हूँ JK COM BOT, मुझे JK COMMUNITY ने बनाया है। आप सबको नमस्ते!**")
    
    status_msg = await message.reply("🔍 **चैनल की ID चेक की जा रही है...**")
    chat_id = str(message.chat.id)
    allowed_ids = [str(x) for x in sheet.col_values(1)]
    
    if chat_id not in allowed_ids:
        return await status_msg.edit("❌ **एरर: इस चैनल को एक्सेस नहीं मिला है।**")
    
    await status_msg.edit("✅ **चैनल की ID मिल गई!**")
    await status_msg.edit("🎙️ **वॉइस चैट ऑन कर रहा हूँ...**")
    await asyncio.sleep(1)
    
    await status_msg.edit("🎵 **एपिसोड प्ले हो रहा है, सब जॉइन करो!**")

print("JK Bot is Active and Ready...")
app.run()
