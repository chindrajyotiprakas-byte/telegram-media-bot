from pyrogram import Client, filters

@Client.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "👋 **Hello! I am your Multi-Utility Bot.**\n\n"
        "🔗 **Link Bypasser**: Send me any shortened link.\n"
        "📦 **TeraBox**: Send me a TeraBox link to check accessibility.\n"
        "☁️ **Mirror**: Use `/mirror <link>` to download & upload files."
    )
