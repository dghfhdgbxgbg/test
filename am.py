import re
import asyncio
from pyrogram.types import Message
from pyrogram import Client, filters
import logging
import aiohttp
from pytgcalls import PyTgCalls
from pytgcalls.types.stream import MediaStream
from pyrogram import Client, filters, idle, enums
from pytgcalls.types import AudioQuality
from pytgcalls.types import MediaStream
from pytgcalls.types import VideoQuality
import requests
import os 

API_ID = 27655384
API_HASH = "a6a418b023a146e99af9ae1afd571cf4"
SESS = "BQEh3pAAQRDgoapwBLBzbSw5BTHQtB1Ir_Sww9xJOiJiyadFa1mLwcGscziW5ye6vasI4nKgeJnuo_7nyqPyoCULFi4lnnFEI8_vl1jqe7Es41NaU8iY_Yz2D67R3zvkIM9HcXIaTQjiNNhoP1CiYsgMYLtxHkHvSs3ZkRG1k4Suflan-KMWT7vuOa_WpUwCqhHQyqb0sRtNA4ZNyhdgdNzE0RcWAJ0L00sDfDsWqLB0BqKCpEZOfFh_kVtfZkXNOz5s0zhYTitvVWKKbro9ZjTv3YPCNgaxxjvdaS8mWOfjfF2dxsxC4aoOZOOochoW09lS7jpWr_VsJ39K7Uhca9hjJ5qRtQAAAAGwYEf_AA"

# Initialize the Pyrogram Client
app = Client("test", api_id=API_ID, api_hash=API_HASH, session_string=SESS)

# Initialize PyTgCalls
ass = PyTgCalls(app)

@app.on_message(filters.command("song"))
async def song_dill(client, message):
    try:
        song_title = message.text.split(" ", 1)[1] if len(message.text.split(" ")) > 1 else None
        if song_title is None:
            await message.reply("Please provide a song title after the command.")
            return
        api_url = f"http://3.6.210.108:5000/download?query={song_title}"
        response = requests.get(api_url)
        data = response.json()
        if data and "links" in data:
            links = data["links"]
            download_link = links[0]["url"]
            await message.reply("Downloading the song... Please wait.")
            fpath = None
            for ext in ['mp3', 'm4a', 'webm']:
                fpath = f"downloads/{song_title}.{ext}"
                if os.path.exists(fpath):
                    return fpath
            res = requests.get(download_link, stream=True)
            res.raise_for_status() 

            fpath = f"downloads/{song_title}.mp3" 
            with open(fpath, "wb") as f:
                for chunk in res.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            await message.reply_document(fpath, caption="Here is your song!")

        else:
            await message.reply("Could not find any song data. Please try again later.")
    
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")

@app.on_message(filters.command("play", prefixes=["/", "!"]))
async def play_command(client: Client, message: Message):
    await message.delete()
    try:
        song_title = message.text.split(" ", 1)[1] if len(message.text.split(" ")) > 1 else None
        if not song_title:
            logging.warning("No song title provided.")
            await message.reply("Please provide a song title!")
            return
        
        # Constructing the URL for the song
        song_url = f"http://3.6.210.108:5000/download?query={song_title}"

        async with aiohttp.ClientSession() as session:
            async with session.get(song_url) as response:
                if response.status != 200:
                    await message.reply("Error retrieving song data!")
                    return
                data = await response.json()

                # Check if the response contains valid links
                if 'links' in data and len(data['links']) > 0:
                    stream_url = data['links'][0]['url']

                    # Replace part of the URL if needed
                    if stream_url.startswith('https://rr2-sn-ab5l6nrl.googlevideo.com/videoplayback'):
                        stream_url = stream_url.replace(
                            "https://rr2-sn-ab5l6nrl.googlevideo.com/videoplayback", 
                            "https://rr2---sn-ab5l6nrl.googlevideo.com/videoplayback"
                        )

                    # Save the stream URL to a file for debugging
                    with open("url.txt", "w", encoding="utf-8") as file:
                        file.write(stream_url)
                    
                    # Log the URL for debugging
                    logging.info(f"Streaming URL: {stream_url}")
                    # Play the song in the voice chat
                    await ass.play(
                        message.chat.id,
                        MediaStream(
                            stream_url,
                            AudioQuality.HIGH,
                            VideoQuality.HD_720p,
                        ),
                    )

                    # Send the URL file back to the user as confirmation
                    ok = await message.reply_document(document="url.txt", caption="Here is the streaming URL!")

                else:
                    await message.reply("No valid links found in the response.")
    except aiohttp.ClientError as e:
        logging.error(f"AIOHTTP error occurred: {e}")
        await message.reply("An error occurred while trying to fetch song data.")
    except Exception as e:
        logging.error(f"Unexpected error occurred: {str(e)}")
        await message.reply(f"An unexpected error occurred: {str(e)}")

# Main async function to run the app and PyTgCalls
async def main():
    await app.start()
    print("Assis started")
    await ass.start()
    print("Main Userbot started")
    print("PyTgCalls started for Assis")
    await idle()
    await app.stop()
    await ass.stop()

if __name__ == "__main__":
    # Running the event loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
