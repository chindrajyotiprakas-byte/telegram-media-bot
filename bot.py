from pyrogram import Client, idle
from config import API_ID, API_HASH, BOT_TOKEN

# Initialize the Client
app = Client(
    "my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins")
)

if __name__ == "__main__":
    print("Starting Bot...")
    app.start()
    print("Bot Started! Press Ctrl+C to stop.")
    idle()
    app.stop()
