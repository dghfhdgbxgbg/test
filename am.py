import re
import asyncio
from pyrogram.types import Message
from pyrogram import Client, filters
import logging
import aiohttp
from pytgcalls import PyTgCalls
from pyrogram import Client, filters, idle, enums
from pytgcalls.types import AudioQuality
from pytgcalls.types import MediaStream
from pytgcalls.types import VideoQuality
import requests
import os 

API_ID = 27655384
API_HASH = "a6a418b023a146e99af9ae1afd571cf4"
SESS = "BQEh3pAAQRDgoapwBLBzbSw5BTHQtB1Ir_Sww9xJOiJiyadFa1mLwcGscziW5ye6vasI4nKgeJnuo_7nyqPyoCULFi4lnnFEI8_vl1jqe7Es41NaU8iY_Yz2D67R3zvkIM9HcXIaTQjiNNhoP1CiYsgMYLtxHkHvSs3ZkRG1k4Suflan-KMWT7vuOa_WpUwCqhHQyqb0sRtNA4ZNyhdgdNzE0RcWAJ0L00sDfDsWqLB0BqKCpEZOfFh_kVtfZkXNOz5s0zhYTitvVWKKbro9ZjTv3YPCNgaxxjvdaS8mWOfjfF2dxsxC4aoOZOOochoW09lS7jpWr_VsJ39K7Uhca9hjJ5qRtQAAAAGwYEf_AA"

app = Client("test", api_id=API_ID, api_hash=API_HASH, session_string=SESS)

ass = PyTgCalls(app)


@app.on_message(filters.command("play", prefixes=["/", "!"]))
async def play_command(client: Client, message: Message):
    await message.delete()
    try:
        song_title = message.text.split(" ", 1)[1] if len(message.text.split(" ")) > 1 else None
        if not song_title:
            logging.warning("No song title provided.")
            await message.reply("Please provide a song title!")
            return
        song_url = f"http://3.6.210.108:5000/download?query={song_title}"
        response = requests.get(song_url)
        if response.status_code == 200:
            data = response.json()
            download_url = data.get("download_url")
            if download_url:
                await message.reply(f"Here is your download link: {download_url}")
            else:
                await message.reply("Sorry, could not find the download URL.")
        else:
            await message.reply("Sorry, an error occurred while fetching the song.")
    except Exception as e:
        await message.reply("An error occurred while processing your request.")
            
                    


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
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
