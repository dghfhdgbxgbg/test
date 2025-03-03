import asyncio
from pyrogram.types import Message
from pyrogram import Client, filters, idle
import aiohttp
import os
import logging
import asyncio
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
                response.raise_for_status()
                data = await response.json()
                download_url = data.get("download_url")
                title = data.get("title")
                thumb = data.get("thumb")
                url = data.get("url")
                if download_url:
                    download_folder = "downloads"
                    os.makedirs(download_folder, exist_ok=True)
                    file_name = f"{song_title}.mp3" 
                    file_path = os.path.join(download_folder, file_name)
                    async with session.get(download_url) as file_response:
                        file_response.raise_for_status() 
                        with open(file_path, 'wb') as f:
                            while True:
                                chunk = await file_response.content.read(1024)
                                if not chunk:
                                    break
                                f.write(chunk)
                    await client.send_document(message.chat.id, file_path, caption=f"Here is your song: {title}\nYoutube : {url}")
                    await asyncio.sleep(18000)  # Sleep for 5 hours
                    if os.path.exists(file_path):
                        os.remove(file_path)
                else:
                    pass
    except aiohttp.ClientResponseError as e:
        pass
    except Exception as e:
        pass

async def main():
    await app.start()
    print("Main Userbot started")
    await idle()
    await app.stop()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
