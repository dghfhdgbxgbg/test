import re
import asyncio
from pyrogram.types import Message
from pyrogram import Client, filters
import logging
import aiohttp
from pytgcalls import PyTgCalls
from pytgcalls.types.stream import MediaStream
from pyrogram import Client, filters, idle, enums

API_ID = 27655384
API_HASH = "a6a418b023a146e99af9ae1afd571cf4"
SESS = "BQEh3pAAQRDgoapwBLBzbSw5BTHQtB1Ir_Sww9xJOiJiyadFa1mLwcGscziW5ye6vasI4nKgeJnuo_7nyqPyoCULFi4lnnFEI8_vl1jqe7Es41NaU8iY_Yz2D67R3zvkIM9HcXIaTQjiNNhoP1CiYsgMYLtxHkHvSs3ZkRG1k4Suflan-KMWT7vuOa_WpUwCqhHQyqb0sRtNA4ZNyhdgdNzE0RcWAJ0L00sDfDsWqLB0BqKCpEZOfFh_kVtfZkXNOz5s0zhYTitvVWKKbro9ZjTv3YPCNgaxxjvdaS8mWOfjfF2dxsxC4aoOZOOochoW09lS7jpWr_VsJ39K7Uhca9hjJ5qRtQAAAAGwYEf_AA"

# Initialize the Pyrogram Client
app = Client("test", api_id=API_ID, api_hash=API_HASH, session_string=SESS)

# Initialize PyTgCalls
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

        async with aiohttp.ClientSession() as session:
            async with session.get(song_url) as response:
                if response.status != 200:
                    await message.reply("Error retrieving song data!")
                    return
                data = await response.json()

                if 'links' in data and len(data['links']) > 0:
                    stream_url = data['links'][0]['url']
                    if stream_url.startswith('https://rr2-sn-ab5l6nrl.googlevideo.com/videoplayback'):
                        stream_url = stream_url.replace(
                            "https://rr2-sn-ab5l6nrl.googlevideo.com/videoplayback", 
                            "https://rr2---sn-ab5l6nrl.googlevideo.com/videoplayback"
                        )
                    await ass.play(message.chat.id, MediaStream(stream_url))
                    print(stream_url)
                    await message.reply(f"Playing <code>{stream_url}</code> in the voice chat!")
                else:
                    await message.reply("No links found in the response.")

    except aiohttp.ClientError as e:
        await message.reply("An error occurred while trying to fetch song data.")
    except Exception as e:
        await message.reply(f"An unexpected error occurred: {str(e)}")

# Run the Pyrogram client first
async def main():
    await app.start()
    print("Assis started")
    await ass.start()
    print("Main Userbot started")
    print("PyTgCalls started For Assis")
    await idle()
    await app.stop()
    await ass.stop()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
