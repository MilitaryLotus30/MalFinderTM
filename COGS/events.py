import datetime

import discord
from discord.ext import commands

class events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener("on_command")
    async def commandwasrun(self, ctx: commands.Context):
        self.bot.print(f'{self.bot.COLORS.command_logs}[COMMAND] {self.bot.COLORS.user_name}{ctx.author.name}{self.bot.COLORS.normal_message} ran command {self.bot.COLORS.item_name}{ctx.command.qualified_name}{self.bot.COLORS.normal_message} on the guild {self.bot.COLORS.item_name}{ctx.guild.name}{self.bot.COLORS.normal_message}. Full command: {self.bot.COLORS.item_name}{ctx.message.content}')


    @commands.Cog.listener("on_message")
    async def messagemoment(self, message: discord.Message):
        if self.bot.user.id in message.raw_mentions and len(message.raw_user_mentions) == 1:
            if message.content.strip() == f"@{self.bot.user.display_name}":
                try:
                    await message.reply(embed=discord.Embed(title="That's Me!",description=f"Hi, {message.author.mention}! My prefix is `{(await (self.bot.command_prefix)(self.bot, message))[0]}`.\nPlease check `{(await (self.bot.command_prefix)(self.bot, message))[0]}help` for more info."), private=message.private)
                    self.bot.print(f'{self.bot.COLORS.command_logs}[COMMAND] {self.bot.COLORS.user_name}{message.author.name}{self.bot.COLORS.normal_message} ran command {self.bot.COLORS.item_name}@PING{self.bot.COLORS.normal_message} on the guild {self.bot.COLORS.item_name}{message.guild.name}{self.bot.COLORS.normal_message}. Full command: {self.bot.COLORS.item_name}{message.content}')
                except:
                    pass
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        me = guild.me
        self.bot.info(f"{self.bot.COLORS.user_name}{self.bot.user.name}{self.bot.COLORS.normal_message} joined the guild {self.bot.COLORS.item_name}{guild.name}")
        channel_id = self.bot.CONFIGS.join_leave_logs
        if channel_id:
            channel = self.bot.get_partial_messageable(channel_id)
            embedig = discord.Embed(title=f"{self.bot.user.name} joined a guild!", description="**{}**".format(guild.name), color=0x363942)
            embedig.timestamp = datetime.datetime.now(datetime.timezone.utc)
            try:
                await channel.send(embed=embedig)
            except:
                pass
        if not me.guild_permissions.administrator:
            self.bot.error(f"Bot does not have administrator privileges on the guild {self.bot.COLORS.item_name}{guild.name}")

            # TODO, don't leave and warn that no permissions are given
            await guild.leave()
        

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        self.bot.info(f"{self.bot.COLORS.user_name}{self.bot.user.name}{self.bot.COLORS.normal_message} left the guild {self.bot.COLORS.item_name}{guild.name}")
        channel_id = self.bot.CONFIGS.join_leave_logs
        if channel_id:
            channel = self.bot.get_partial_messageable(channel_id)
            embedig = discord.Embed(title=f"{self.bot.user.name} left a guild.", description=f'**{guild.name}**', color=0x363942)
            embedig.timestamp = datetime.datetime.now(datetime.timezone.utc)
            try:
                await channel.send(embed=embedig)
            except:
                pass
            

async def setup(bot):
	await bot.add_cog(events(bot))