import traceback
import discord
from discord.ext import commands

class developer(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='load', description='Loads a cog.')
    async def load(self, ctx:commands.Context, *, cog_name: str):
        if not ctx.author.id in self.bot.CONFIGS.owners:
            return await ctx.reply('No.', private=ctx.message.private)

        if not cog_name.startswith(f'{self.bot.CONFIGS.cogs_dir[:-1]}.'):
            cog_name = f'{self.bot.CONFIGS.cogs_dir[:-1]}.' + cog_name
        try:
            await self.bot.load_extension(cog_name)
            self.bot.print(f'{self.bot.COLORS.cog_logs}[COGS] {self.bot.COLORS.normal_message}Loaded cog {self.bot.COLORS.item_name}{cog_name}')
        except Exception as e:
            em = discord.Embed(description="Failed to load cog.", color=0x363942)
            await ctx.reply(embed=em, private=ctx.message.private)
            self.bot.traceback(e)
        else:
            em = discord.Embed(description="**Cog loaded.**", color=0x363942)
            await ctx.reply(embed=em, private=ctx.message.private)

    @commands.command(name='unload', description='Unloads a cog.')
    async def unload(self, ctx:commands.Context, *, cog_name: str):
        if not ctx.author.id in self.bot.CONFIGS.owners:
            return await ctx.reply('No.', private=ctx.message.private)
        if not cog_name.startswith(f'{self.bot.CONFIGS.cogs_dir[:-1]}.'):
            cog_name = f'{self.bot.CONFIGS.cogs_dir[:-1]}.' + cog_name

        if cog_name in self.bot.extensions:
            await self.bot.unload_extension(cog_name)
            self.bot.print(f'{self.bot.COLORS.cog_logs}[COGS] {self.bot.COLORS.normal_message}Unloaded cog {self.bot.COLORS.item_name}{cog_name}')
            em = discord.Embed(description="**Cog unloaded.**", color=0x363942)
            await ctx.reply(embed=em, private=ctx.message.private)
        else:
            em = discord.Embed(description="That cog isn't loaded.", color=0x363942)
            await ctx.reply(embed=em, private=ctx.message.private)

    @commands.command(name='reload', description='Reloads a cog.')
    async def reload(self, ctx:commands.Context, *, cog_name: str = None):
        if not ctx.author.id in self.bot.CONFIGS.owners:
            return await ctx.reply('No.', private=ctx.message.private)
        if not cog_name.startswith(f'{self.bot.CONFIGS.cogs_dir[:-1]}.'):
            cog_name = f'{self.bot.CONFIGS.cogs_dir[:-1]}.' + cog_name

        try:
            await self.bot.reload_extension(cog_name)
            self.bot.print(f'{self.bot.COLORS.cog_logs}[COGS] {self.bot.COLORS.normal_message}Reloaded cog {self.bot.COLORS.item_name}{cog_name}')
        except Exception as e:
            em = discord.Embed(description="Failed to reload cog.", color=0x363942)
            await ctx.reply(embed=em, private=ctx.message.private)
            self.bot.traceback(e)
        else:
            em = discord.Embed(description="**Cog reloaded.**", color=0x363942)
            await ctx.reply(embed=em, private=ctx.message.private)

    @commands.command(name='eval', aliases=['exec'], description='eval/exec something for devs only')
    async def asyncexecute(self, ctx:commands.Context):
        if not ctx.author.id in self.bot.CONFIGS.owners:
            return await ctx.reply('No.', private=ctx.message.private)
        async def aexec(code, message):
            exec(f'async def __ex(message):\n    '+(''.join(f'\n    {l}'for l in code.split('\n'))).strip(), globals(), locals())
            return (await locals()['__ex'](message))
        
        message = ctx.message
        cmd = message.content.splitlines()
        del cmd[0]
        del cmd[0]
        del cmd[-1]
        cmd = "\n".join(cmd)
        try:
            await aexec(cmd, message)
        except Warning as e:
            result = ("".join(traceback.format_exception(e, e, e.__traceback__))).replace('`', '\`')
            await message.reply(f'**Eval ran with an warning:**\n\n```python\n{result}\n```')
            await message.add_reaction('⚠️')
        except Exception as e:
            result = ("".join(traceback.format_exception(e, e, e.__traceback__))).replace('`', '\`')
            await message.reply(f'**Eval failed with Exception:**\n\n```python\n{result}\n```')
            await message.add_reaction('❌')
        else:
            await message.add_reaction('✅')

async def setup(bot):
	await bot.add_cog(developer(bot))