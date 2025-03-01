import re
import asyncio
from typing import Callable
from pyrogram.types import Message
from pyrogram import Client, filters, enums
import random
from pyrogram.types import (
    CallbackQuery,
    ChatMemberUpdated,
    ChatPermissions,
    ChatPrivileges,
    Message,
)
import json
import os
from typing import Dict, List, Union
import json, os, random, asyncio
import requests
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.exceptions import (
    AlreadyJoinedError,
    NoActiveGroupCall,
    TelegramServerError,
)
from pytgcalls.types import Update
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio, MediumQualityVideo
from pytgcalls.types.stream import StreamAudioEnded
from pyrogram.errors import FloodWait, PeerIdInvalid
import aiohttp
from pytgcalls.types.input_stream import AudioParameters
from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream import InputStream
from pytgcalls.types.input_stream import InputVideoStream
from pytgcalls.types.input_stream import VideoParameters

API_ID = 27655384
API_HASH = "a6a418b023a146e99af9ae1afd571cf4"
SESS = "BQEh3pAAQRDgoapwBLBzbSw5BTHQtB1Ir_Sww9xJOiJiyadFa1mLwcGscziW5ye6vasI4nKgeJnuo_7nyqPyoCULFi4lnnFEI8_vl1jqe7Es41NaU8iY_Yz2D67R3zvkIM9HcXIaTQjiNNhoP1CiYsgMYLtxHkHvSs3ZkRG1k4Suflan-KMWT7vuOa_WpUwCqhHQyqb0sRtNA4ZNyhdgdNzE0RcWAJ0L00sDfDsWqLB0BqKCpEZOfFh_kVtfZkXNOz5s0zhYTitvVWKKbro9ZjTv3YPCNgaxxjvdaS8mWOfjfF2dxsxC4aoOZOOochoW09lS7jpWr_VsJ39K7Uhca9hjJ5qRtQAAAAGwYEf_AA"

app = Client("test", api_id=API_ID, api_hash=API_HASH, session_string=SESS)

ass = PyTgCalls(app)

@app.on_message(filters.command("play", prefixes=["/", "!"]))
async def play_command(client: Client, message: Message):
    await message.delete()
    try:
        # Extract song title from the message
        song_title = message.text.split(" ", 1)[1] if len(message.text.split(" ")) > 1 else None
        if not song_title:
            await message.reply("Please provide a song title!")
            return

        # Create the song URL
        song_url = f"http://3.6.210.108:5000/download?query={song_title}"

        async with aiohttp.ClientSession() as session:
            async with session.get(song_url) as response:
                if response.status != 200:
                    await message.reply("Error retrieving song data!")
                    return
                
                # Process the song data
                data = await response.json()
                if 'links' in data and len(data['links']) > 0:
                    stream_url = data['links'][0]['url']  # Get the stream URL
                    plays = AudioVideoPiped(
                        stream_url,
                        audio_parameters=HighQualityAudio(),
                        video_parameters=MediumQualityVideo(),
                    )
                    
                    # Join the group call and play the stream
                    await ass.join_group_call(
                        message.chat.id,
                        plays,
                        stream_type=StreamType().pulse_stream,
                    )
                    await message.reply(f"Playing `{stream_url}` in the voice chat!")
                else:
                    await message.reply("No links found in the response.")
    
    except aiohttp.ClientError as e:
        # Handle errors with the request (e.g., network issues)
        await message.reply("An error occurred while trying to fetch song data.")
    except Exception as e:
        # Catch any other unexpected errors
        await message.reply(f"An unexpected error occurred: {str(e)}")

app.run()
ass.run()
print("bot Started")
