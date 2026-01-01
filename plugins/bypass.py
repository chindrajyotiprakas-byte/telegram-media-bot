from pyrogram import Client, filters
import cloudscraper
import time

# Initialize scraper to handle Cloudflare protections
scraper = cloudscraper.create_scraper()

@Client.on_message(filters.text & filters.regex(r'^https?://') & ~filters.command('start'))
async def bypass_link(client, message):
    url = message.text.strip()
    status_msg = await message.reply_text("🔎 **Checking Link...**")
    
    try:
        # Request with cloudscraper
        # timeout is important to not hang the bot
        response = scraper.get(url, allow_redirects=True, timeout=15)
        
        final_url = response.url
        
        if final_url != url:
            await status_msg.edit_text(
                f"✅ **Bypassed / Resolved**\n\n"
                f"**Original:** {url}\n"
                f"**Result:** {final_url}",
                disable_web_page_preview=True
            )
        else:
             await status_msg.edit_text(
                f"ℹ️ **Direct Link**\n\n"
                f"The link appears to be direct or I couldn't bypass it.\n"
                f"{final_url}",
                disable_web_page_preview=True
            )
            
    except Exception as e:
        await status_msg.edit_text(f"❌ **Error:** {str(e)}")
