import asyncio

import discord
from discord.ext import commands

class tasks(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        asyncio.create_task(self.change_status())
    
    async def change_status(self):
        while True:
            try:
                while True:
                    # [activity, the game, delay, status]
                    guild_count = len(self.bot.guilds)
                    statuses = [
                        [discord.ActivityType.watching, f"{guild_count} guild{'s' if guild_count != 1 else ''}!", 60, discord.Status.online],
                        [discord.ActivityType.playing, f"https://github.com/MilitaryLotus30/MalFinderTM/", 60, discord.Status.online]
                    ]
                    for status in statuses:
                        try:
                            await self.bot.change_presence(status=status[3], activity=discord.Activity(type=status[0], name=status[1]))
                            self.bot.info(f"Status changed to {self.bot.COLORS.item_name}{status[1]}{self.bot.COLORS.normal_message} with activity {self.bot.COLORS.item_name}{status[0].name}{self.bot.COLORS.normal_message} for {self.bot.COLORS.item_name}{status[2]}{self.bot.COLORS.normal_message} seconds")
                            await asyncio.sleep(status[2])
                        except Exception as e:
                            self.bot.warn(f"An error occurred while attempting to change the bot's status: {self.bot.COLORS.item_name}{e}")
            except Exception as e:
                self.bot.warn(f"An error occurred in the {self.bot.COLORS.item_name}change_status{self.bot.COLORS.normal_message} task: {self.bot.COLORS.item_name}{e}")
                self.bot.info(f"Restarting task in {self.bot.COLORS.item_name}5{self.bot.COLORS.normal_message} seconds")
                await asyncio.sleep(5)

async def setup(bot):
	await bot.add_cog(tasks(bot))