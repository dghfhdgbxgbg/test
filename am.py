from pyrogram import Client, filters
from pyrogram.errors import FloodWait
import time
import re
import asyncio
from pyrogram import Client, filters
from typing import Callable
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import Message
from pyrogram import Client, filters, enums
import random
from pyrogram.enums import ChatMembersFilter, ChatMemberStatus, ChatType
from pyrogram.types import (
    CallbackQuery,
    ChatMemberUpdated,
    ChatPermissions,
    ChatPrivileges,
    Message,
)
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import (
    ChatAdminRequired,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client, filters
from pyrogram.enums import ChatMembersFilter
import re
from pyrogram import filters
from pyrogram.enums import ChatAction, ChatType, MessageEntityType
from pyrogram.types import Message
import socket
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

API_ID = 27655384
API_HASH = "a6a418b023a146e99af9ae1afd571cf4"
SESS = "BQEh3pAAQRDgoapwBLBzbSw5BTHQtB1Ir_Sww9xJOiJiyadFa1mLwcGscziW5ye6vasI4nKgeJnuo_7nyqPyoCULFi4lnnFEI8_vl1jqe7Es41NaU8iY_Yz2D67R3zvkIM9HcXIaTQjiNNhoP1CiYsgMYLtxHkHvSs3ZkRG1k4Suflan-KMWT7vuOa_WpUwCqhHQyqb0sRtNA4ZNyhdgdNzE0RcWAJ0L00sDfDsWqLB0BqKCpEZOfFh_kVtfZkXNOz5s0zhYTitvVWKKbro9ZjTv3YPCNgaxxjvdaS8mWOfjfF2dxsxC4aoOZOOochoW09lS7jpWr_VsJ39K7Uhca9hjJ5qRtQAAAAGwYEf_AA"

app = Client("test", api_id=API_ID, api_hash=API_HASH, session_string=SESS)

ass = PyTgCalls(app)

@app.on_message(filters.command(["start","help"], prefixes=["/","!"]))
async def start_command(client, message):
    await message.delete()
    await message.reply("HII")
    
    

@app.on_message(filters.command("play", prefixes=["/", "!"]))
async def play_command(client: Client, message):
    song_title = message.text.split(" ", 1)[1] if len(message.text.split(" ")) > 1 else None
    if song_title:
        song_url = f"http://3.6.210.108:5000/download?query={song_title}"
        try:
            response = requests.get(song_url)
            response.raise_for_status()
            data = response.json()

            # Get the OPUS format link
            audio_link = next((link['url'] for link in data['links'] if link['format'] == 'OPUS'), None)
            
            if audio_link:
                # Assuming `audio_link` is the streamable URL
                stream = AudioVideoPiped(
                    audio_link,  # Correctly use `audio_link` here
                    audio_parameters=HighQualityAudio(),
                    video_parameters=MediumQualityVideo(),
                )
                await ass.join_group_call(message.chat.id, stream)
            else:
                await message.reply("No OPUS audio link found.")
        
        except requests.exceptions.RequestException as e:
            await message.reply(f"An error occurred: {str(e)}")
        except Exception as e:
            await message.reply(f"An unexpected error occurred: {str(e)}")
    else:
        await message.reply("Please provide a song title.")

app.run()
ass.run()
