import asyncio
from pyrogram.types import Message
from pyrogram import Client, filters, idle
import aiohttp
import logging

# Setup logging for better error tracking
logging.basicConfig(level=logging.INFO)

API_ID = 27655384
API_HASH = "a6a418b023a146e99af9ae1afd571cf4"
SESS = "7236495063:AAF59K5HiCcDybUM5jKPZFaDuwe5BS97foc"

app = Client("test", api_id=API_ID, api_hash=API_HASH, bot_token=SESS)

@app.on_message(filters.command(["song", "play"]))
async def play_command(client: Client, message: Message):
    try:
        await message.delete()
        song_title = message.text.split(" ", 1)[1] if len(message.text.split(" ")) > 1 else None
        if not song_title:
            await message.reply("Please provide a song title!")
            return
        
        song_url = f"http://3.6.210.108:5000/download?query={song_title}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(song_url) as response:
                # Automatically raises an exception for error status codes
                response.raise_for_status()

                # Now that we know the status is 200 (OK), we can parse the response
                data = await response.json()
                print("API response data:", data)  # Debugging print to check response
                
                download_url = data.get("download_url")
                if download_url:
                    await message.reply(f"Here is your download link: {download_url}")
                else:
                    await message.reply("Sorry, could not find the download URL.")
    except aiohttp.ClientResponseError as e:
        # Handle HTTP errors (like 400 or 500 range)
        logging.error(f"HTTP error occurred: {e}")
        await message.reply(f"HTTP error occurred: {e}")
    except Exception as e:
        # Catch all other errors
        logging.error(f"Error: {e}")
        await message.reply("An error occurred while processing your request.")

async def main():
    await app.start()
    print("Main Userbot started")
    await idle()
    await app.stop()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
