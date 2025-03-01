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


@app.on_message(filters.command("play", prefixes=["/", "!"]))
async def play_command(client: Client, message):
    song_title = message.text.split(" ", 1)[1] if len(message.text.split(" ")) > 1 else None
    song_url = f"http://3.6.210.108:5000/download?query={song_title}"
    response = requests.get(song_url)
    response.raise_for_status()
    data = response.json()
    audio_link = "https://rr2---sn-qi4pcxgoxu-cf5e.googlevideo.com/videoplayback?expire=1740845125&ei=5dvCZ630M5qCy_sPsrmZ6QU&ip=156.248.106.19&id=o-AOic4sY0rWcEPUcEJ4QoAVE1xQGITUz5bnEZ36mUwosX&itag=251&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&rms=au,au&bui=AUWDL3xX9mDk4lY96Pv82sDzrsGvctOldfLnrngEI5AzqbsSTVCA4Xz05SP_nDC6ewEjUvw0qIZtcXnB&spc=RjZbSWIKbAXBbNyj8fVeLDo8MnjXYBa3uB8Xqyh9ugXpg8TuVAgF-4_gfy7LhWU&vprv=1&svpuc=1&mime=audio/webm&ns=QdTpNQgMkDKdR_1JtR5TC7kQ&rqh=1&gir=yes&clen=5600908&dur=328.521&lmt=1726352360495845&keepalive=yes&fexp=24350590,24350737,24350827,24350961,24351064,24351146,24351173,24351202,24351270,24351341,51326932,51355912&c=WEB&sefc=1&txp=4532434&n=x5LXchj5bdiomg&sparams=expire,ei,ip,id,itag,source,requiressl,xpc,bui,spc,vprv,svpuc,mime,ns,rqh,gir,clen,dur,lmt&sig=AJfQdSswRAIgUi5MWPy1KyfTrzi1VyjyRsDd2DjwIZMdmMytjjwQu84CIGclgyFNcux1rjtnsiinq3RkMIBITzdpvVXxEBFUj13K&pot=MnQ0V2xRj78I5zRvvDVQvlwOHM7PUTCjt2FZuyPY609qLrSzUMVy63_tYpW-V_Q35GlJ5vGoNApS3Ls5Mpi-rUG-1_sfBFrRvsEOvVizaRODGxHRnWL-Lv2WFVxorZWESAiytraKkEda5lFLetMlDdte9Vuzgg%3D%3D&range=0-&redirect_counter=1&rm=sn-ab5eek7l&rrc=104&req_id=e0b0f1d308e3a6e9&cms_redirect=yes&cmsv=e&ipbypass=yes&met=1740823583,&mh=WI&mip=2405:acc0:1504:5ef8:d10f:f5a:485:9924&mm=31&mn=sn-qi4pcxgoxu-cf5e&ms=au&mt=1740822583&mv=u&mvi=2&pl=55&lsparams=ipbypass,met,mh,mip,mm,mn,ms,mv,mvi,pl,rms&lsig=AFVRHeAwRQIhAIa34BxyK9zvOkkI3-I5foUgjhXetLVk_nBUH9L5-_C9AiAE5jJsPNB0BYtox7mvwQttDPNchljzsugtTF76U2ST4w%3D%3D"
    stream = AudioVideoPiped(
                audio_link,  
                audio_parameters=HighQualityAudio(),
                video_parameters=MediumQualityVideo(),
                )
    await ass.join_group_call(message.chat.id, stream)

        


app.run()
ass.run()
print("bot Started")
