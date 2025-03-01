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

API_ID = 27655384
API_HASH = "a6a418b023a146e99af9ae1afd571cf4"
SESS = "BQEh3pAAQRDgoapwBLBzbSw5BTHQtB1Ir_Sww9xJOiJiyadFa1mLwcGscziW5ye6vasI4nKgeJnuo_7nyqPyoCULFi4lnnFEI8_vl1jqe7Es41NaU8iY_Yz2D67R3zvkIM9HcXIaTQjiNNhoP1CiYsgMYLtxHkHvSs3ZkRG1k4Suflan-KMWT7vuOa_WpUwCqhHQyqb0sRtNA4ZNyhdgdNzE0RcWAJ0L00sDfDsWqLB0BqKCpEZOfFh_kVtfZkXNOz5s0zhYTitvVWKKbro9ZjTv3YPCNgaxxjvdaS8mWOfjfF2dxsxC4aoOZOOochoW09lS7jpWr_VsJ39K7Uhca9hjJ5qRtQAAAAGwYEf_AA"

app = Client("test", api_id=API_ID, api_hash=API_HASH, session_string=SESS)

ass = PyTgCalls(app)

@app.on_message(filters.command("play", prefixes=["/", "!"]))
async def play_command(client: Client, message):
    try:
        song_title = message.text.split(" ", 1)[1] if len(message.text.split(" ")) > 1 else None
        if not song_title:
            await message.reply("Please provide a song title!")
            return
        song_url = f"http://3.6.210.108:5000/download?query={song_title}"
        response = requests.get(song_url)
        if response.status_code != 200:
            await message.reply("Error retrieving song data!")
            return
        
        data = response.json()  
        print(data)  
        # Example: await ass.join_group_call(message.chat.id, stream)

    except KeyError as e:
        await message.reply("Key error encountered while processing the request.")
        print(f"KeyError: {e}")
    except ValueError as e:
        await message.reply("Value error encountered while processing the request.")
        print(f"ValueError: {e}")
    except requests.exceptions.RequestException as e:
        await message.reply("Request failed, please try again later.")
        print(f"RequestException: {e}")
    except PeerIdInvalid as e:
        await message.reply("Invalid peer ID.")
        print(f"PeerIdInvalid: {e}")

        


app.run()
ass.run()
print("bot Started")
