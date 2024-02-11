import discord
from discord.ext import commands

class information(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command(name='help', description='Help for every command this bot has!', aliases=['h'])
    async def help(self, ctx:commands.Context, *, command:str=None):
        '''
        Help command
        '''
        if command:
            command = command.lower()
        prefixdata = ctx.prefix
        if command:
            if command.startswith(prefixdata):
                command = command[len(prefixdata):len(command)]
        helpcmd = []
        if command:
            helpcmd = None
            for i in self.bot.commands:
                if (i.qualified_name).lower() == command or command in i.aliases:
                    helpcmd = i
                    break
        else:
            for i in self.bot.commands:
                helpcmd.append(i.qualified_name)
        if command is None:
            embedig = discord.Embed(
                title='Command Help',
                description=f'Command Count: `{len(self.bot.commands)}`\n**Do {prefixdata}help <command> for more info!**'
            )
            embedig.add_field(name="Commands", value=", ".join(helpcmd), inline=False)
        elif command:
            if not helpcmd:
                return await ctx.reply('Command not found.', private=True)
            embedig = discord.Embed(
                title='Command Help',
                description=f'Command `{helpcmd.qualified_name}`\'s information.'
            )
            embedig.add_field(name='Command Description', value=f'{helpcmd.description}')
            aliases = helpcmd.aliases
            if (", ".join(aliases)).strip() == '':
                aliases = 'None'
            else:
                aliases = ", ".join(aliases)
            embedig.add_field(name='Command Aliases', value=f'{aliases}')
        await ctx.reply(embed=embedig, private=ctx.message.private)

    @commands.command(name='prefix', description='Return the bot\'s current prefix!')
    async def prefix(self, ctx: commands.Context):
        prefixdata = (await self.bot.get_prefix(ctx.message))[0]
        embedig = discord.Embed(
            title='Guild Prefix',
            description=f'The current prefix for this guild is `{prefixdata}`.'
        )
        await ctx.reply(embed=embedig, private=ctx.message.private)

    @commands.command(name='ping', description='Check if the bot is online, as well as the latency of it!')
    async def pong(self, ctx: commands.Context):
        embedig = discord.Embed(
            title='🏓 Pong'
        )
        embedig.add_field(name='Bot Latency',value=f'`{round(self.bot.latency*1000, 3)}` ms',inline=False)
        await ctx.reply(embed=embedig, private=ctx.message.private)


async def setup(bot):
	await bot.add_cog(information(bot))