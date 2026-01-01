import os
import time
import aiohttp
from pyrogram import Client, filters
from plugins.utils import progress_bar, reset_progress

# Set a download directory
DOWNLOAD_DIR = "downloads"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

@Client.on_message(filters.command("mirror"))
async def mirror_handler(client, message):
    # Check if command has a link
    if len(message.command) < 2:
        await message.reply_text("⚠️ **Usage:** `/mirror <direct_link>`")
        return

    url = message.command[1]
    status_msg = await message.reply_text("☁️ **Initiating Mirror...**")
    
    filename = url.split("/")[-1]
    file_path = os.path.join(DOWNLOAD_DIR, filename)
    
    try:
        # 1. Download
        await status_msg.edit_text("⬇️ **Downloading file...**")
        reset_progress()
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    await status_msg.edit_text("❌ Error fetching URL.")
                    return
                
                total_size = int(response.headers.get('content-length', 0))
                downloaded_size = 0
                
                with open(file_path, 'wb') as f:
                    async for chunk in response.content.iter_chunked(1024 * 1024): # 1MB chunks
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        await progress_bar(downloaded_size, total_size, status_msg, "⬇️ **Downloading...**")

        # 2. Upload
        await status_msg.edit_text("⬆️ **Uploading to Telegram...**")
        reset_progress()
        
        # Upload config: default to current chat, or change to LOG_CHANNEL if needed
        chat_id = message.chat.id 
        
        await client.send_document(
            chat_id=chat_id,
            document=file_path,
            caption=f"**Mirrored File:** `{filename}`",
            progress=progress_bar,
            progress_args=(status_msg, "⬆️ **Uploading...**")
        )
        
        await status_msg.delete()
        
        # 3. Clean up
        os.remove(file_path)
        
    except Exception as e:
        await status_msg.edit_text(f"❌ **Error:** {str(e)}")
        if os.path.exists(file_path):
            os.remove(file_path)
