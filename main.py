import discord
from discord.ext import commands
import aiohttp
import os
import re

virustotal_api_key = 'VIRUSTOTAL_API_KEY'
discord_token = "DISCORD_BOT_TOKEN"

bot = commands.Bot(command_prefix='!')

async def scan_with_virustotal(resource):
    try:
        url = 'https://www.virustotal.com/vtapi/v2/url/scan'
        params = {'apikey': virustotal_api_key, 'url': resource}
        async with aiohttp.ClientSession() as cs:
            async with cs.post(url, data=params) as resp:
                resp.raise_for_status()
                return await resp.json()
    except Exception as e:
        print(f"Error scanning with VirusTotal: {e}")
        write_to_log(f"Error scanning with VirusTotal: {e}")
        return None

async def get_scan_results(resource):
    try:
        api_key = 'YOUR_VIRUSTOTAL_API_KEY'
        url = 'https://www.virustotal.com/vtapi/v2/url/report'
        params = {'apikey': api_key, 'resource': resource}
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url, params=params) as resp:
                resp.raise_for_status()
                return await resp.json()
    except Exception as e:
        print(f"Error getting scan results from VirusTotal: {e}")
        write_to_log(f"Error getting scan results from VirusTotal: {e}")
        return None

@bot.event
async def on_ready():
    print('Bot is ready.')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Check for attachments
    if message.attachments:
        for attachment in message.attachments:
            result = await scan_with_virustotal(attachment.url)
            if result:
                await message.channel.send(f"Scanning attachment: {attachment.filename}")
                scan_id = result.get('scan_id')
                while True:
                    scan_result = get_scan_results(scan_id)
                    if scan_result and scan_result.get('response_code') == 1:
                        positives = scan_result.get('positives')
                        detection = "Detected" if positives > 0 else "Not detected"
                        permalink = scan_result.get('permalink')
                        await save_to_log(message, detection, permalink)
                        await send_scan_result(message.channel, attachment.filename, detection, permalink)
                        break
                    else:
                        await message.channel.send("Error retrieving scan results.")
                        write_to_log(f"Error retrieving scan results for attachment: {attachment.url}")
                        break
            else:
                await message.channel.send("Error scanning attachment.")
                write_to_log("Error scanning attachment.")
                break

    # Check for URLs in message content
    urls = re.findall(r'(https?:((//)|(\\\\))+[\\w\\d:#@%/;$()~_?\\+-=\\\\\\.&]*)', message.content)
    for url in urls:
        result = scan_with_virustotal(url)
        if result:
            await message.channel.send(f"Scanning link: {url}")
            scan_id = result.get('scan_id')
            while True:
                scan_result = get_scan_results(scan_id)
                if scan_result and scan_result.get('response_code') == 1:
                    positives = scan_result.get('positives')
                    detection = "Detected" if positives > 0 else "Not detected"
                    permalink = scan_result.get('permalink')
                    await save_to_log(message, detection, permalink)
                    await send_scan_result(message.channel, url, detection, permalink)
                    break
                else:
                    await message.channel.send("Error retrieving scan results.")
                    write_to_log(f"Error retrieving scan results for link: {url}")
                    break
        else:
            await message.channel.send("Error scanning link.")
            write_to_log("Error scanning link.")

    await bot.process_commands(message)

async def save_to_log(message, detection, permalink):
    with open('log.txt', 'a') as file:
        file.write(f"Message: {message.jump_url}, Detection: {detection}, VirusTotal: {permalink}\n")

async def send_scan_result(channel, resource, detection, permalink):
    color = discord.Color.red() if detection == "Detected" else discord.Color.green()
    embed = discord.Embed(title=f"Scan results for {resource}", color=color)
    embed.add_field(name="Detection", value=detection, inline=False)
    embed.add_field(name="View full scan", value=f"[here]({permalink})", inline=False)
    await channel.send(embed=embed)

def write_to_log(message):
    with open('log.txt', 'a') as file:
        file.write(f"{message}\n")

# Check if log.txt exists, if not, create it
if not os.path.exists('log.txt'):
    with open('log.txt', 'w') as file:
        file.write('')

bot.run(discord_token)