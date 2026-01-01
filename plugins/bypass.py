from pyrogram import Client, filters
from plugins.bypass_v2 import bypasser

@Client.on_message(filters.text & filters.regex(r'^https?://') & ~filters.command('start'))
async def bypass_link(client, message):
    url = message.text.strip()
    status_msg = await message.reply_text("🔎 **Checking Link...**")
    
    try:
        final_url = bypasser.bypass_url(url)
        
        if final_url and final_url != url:
            await status_msg.edit_text(
                f"✅ **Bypassed / Resolved**\n\n"
                f"**Original:** {url}\n"
                f"**Result:** {final_url}",
                disable_web_page_preview=True
            )
        else:
             await status_msg.edit_text(
                f"ℹ️ **Direct Link / Failed**\n\n"
                f"The link appears to be direct or I couldn't bypass it.\n"
                f"{final_url if final_url else url}",
                disable_web_page_preview=True
            )
            
    except Exception as e:
        await status_msg.edit_text(f"❌ **Error:** {str(e)}")
