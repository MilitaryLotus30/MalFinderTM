import discord, aiohttp
from discord.ext import commands
import os, re

class scanner(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.virustotal_api_key = self.bot.CONFIGS.virustotal_api_key

    async def scan_with_virustotal(self, resource):
        try:
            url = 'https://www.virustotal.com/vtapi/v2/url/scan'
            params = {'apikey': self.virustotal_api_key, 'url': resource}
            async with aiohttp.ClientSession() as cs:
                async with cs.post(url, data=params) as resp:
                    resp.raise_for_status()
                    return await resp.json()
        except Exception as e:
            self.bot.error(f"Error scanning {self.bot.COLORS.item_name}{resource}{self.bot.COLORS.normal_message} with VirusTotal")
            self.bot.traceback(e)
            return None

    async def get_scan_results(self, resource):
        try:
            url = 'https://www.virustotal.com/vtapi/v2/url/report'
            params = {'apikey': self.virustotal_api_key, 'resource': resource}
            async with aiohttp.ClientSession() as cs:
                async with cs.get(url, params=params) as resp:
                    resp.raise_for_status()
                    return await resp.json()
        except Exception as e:
            self.bot.error(f"Error getting scan results from VirusTotal")
            self.bot.traceback(e)
            return None

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        # Check for attachments
        if message.attachments:
            for attachment in message.attachments:
                result = await self.scan_with_virustotal(attachment.url)
                if result:
                    await message.channel.send(f"Scanning attachment: {attachment.filename}")
                    scan_id = result.get('scan_id')
                    while True:
                        scan_result = self.get_scan_results(scan_id)
                        if scan_result and scan_result.get('response_code') == 1:
                            positives = scan_result.get('positives')
                            detection = "Detected" if positives > 0 else "Not detected"
                            permalink = scan_result.get('permalink')
                            await self.save_to_log(message, detection, permalink)
                            await self.send_scan_result(message.channel, attachment.filename, detection, permalink)
                            break
                        else:
                            await message.channel.send("Error retrieving scan results.")
                            break
                else:
                    await message.channel.send("Error scanning attachment.")
                    # There isn't a need to log the error again, it was already logged in the function
                    break

        # Check for URLs in message content
        urls = re.findall(r'(https?:((//)|(\\\\))+[\\w\\d:#@%/;$()~_?\\+-=\\\\\\.&]*)', message.content)
        for url in urls:
            result = await self.scan_with_virustotal(url)
            if result:
                await message.channel.send(f"Scanning link: {url}")
                scan_id = result.get('scan_id')
                while True:
                    scan_result = await self.get_scan_results(scan_id)
                    if scan_result and scan_result.get('response_code') == 1:
                        positives = scan_result.get('positives')
                        detection = "Detected" if positives > 0 else "Not detected"
                        permalink = scan_result.get('permalink')
                        await self.save_to_log(message, detection, permalink)
                        await self.send_scan_result(message.channel, url, detection, permalink)
                        break
                    else:
                        await message.channel.send("Error retrieving scan results.")
                        break
            else:
                await message.channel.send("Error scanning link.")

        await self.bot.process_commands(message)

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

async def setup(bot: commands.Bot):
	await bot.add_cog(scanner(bot))