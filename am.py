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
                    stream_url = f"https://rr2---sn-qi4pcxgoxu-cf5e.googlevideo.com/videoplayback?expire=1740853570&ei=4vzCZ9uuLfSFy_sPooWKuAY&ip=156.248.108.146&id=o-AIV72wjfOJVCnq9JnurkdWfNwJkz3Z_luY2-Y3pmPFlS&itag=140&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&rms=au%2Cau&bui=AUWDL3zGLpfkRLdJroYaSYMkv1q46zYFhmyi9H9YOwLm976s1asUicmhgC6LDAaUSGueufDKSmEmQ9e0&spc=RjZbSQM8cQ9bPr7PgzQ3R3kOiKFPQrey4k0TdPYR0Cv9XbyJZPdC3HwW0RQqQtM&vprv=1&svpuc=1&mime=audio%2Fmp4&ns=HUSdzO14e-TmYRhrP_imO2UQ&rqh=1&gir=yes&clen=5318525&dur=328.562&lmt=1726352263756647&keepalive=yes&fexp=24350590,24350737,24350827,24350961,24351063,24351173,24351202,24351270,24351340,51326932,51355912,51411871&c=WEB&sefc=1&txp=4532434&n=6kLN_W9fV8DlvA&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Cns%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AJfQdSswRQIgdImhcY9DnYlvV1ZlnJmoZyd8Dp6TdIwufvAcyfbgsPkCIQDUncoq0RrHedc09MOnNgmCmuzeNnuHotnWpj7sj0xJEw%3D%3D&pot=MnRtEbvHtUs9sG0pHiVgF8QmQ7_7gs60DQrVNnFIByQaJkjLNBQbTmDuprq_SSb_EGHmssuA3nOFUxE_pvJX9TF2ukvv89iaLiT9KFZnBO2kb1ScBAWuX0kS5BZ8eozTO5JfXxuWvqxTW-_w9h-fa_dMqbvwCw%3D%3D&range=0-&redirect_counter=1&rm=sn-p5qell7s&rrc=104&req_id=2920d8a10f55a6e9&cms_redirect=yes&cmsv=e&ipbypass=yes&met=1740832007,&mh=WI&mip=2405:acc0:1504:5ef8:88f4:ba8d:8b87:ab79&mm=31&mn=sn-qi4pcxgoxu-cf5e&ms=au&mt=1740831660&mv=m&mvi=2&pl=55&lsparams=ipbypass,met,mh,mip,mm,mn,ms,mv,mvi,pl,rms&lsig=AFVRHeAwRAIgBoyiuywJSnq_SFhT4XMAc-tY8x9vRdKk68trLgpvwukCIAgChiezzO6ekT8tDC71fg3gfcq2wsVsAmlq_vLYhMRl"  # Get the stream URL
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
