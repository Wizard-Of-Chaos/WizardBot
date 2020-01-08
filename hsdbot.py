#!/usr/bin/env python
# HSDBot code by Wizard of Chaos#2459 and virtuNat#7998
import calendar
from datetime import datetime
import asyncio as aio
import discord as dc
from discord.ext import commands
from guildconfig import GuildConfig
from rolesaver import RoleSaver
# import logging as log

# log.basicConfig(level=log.INFO)
bot = commands.Bot(command_prefix='>')
bot.remove_command('help')
guild_config = GuildConfig(bot, 'config.pkl')
role_saver = RoleSaver(bot, 'roles.pkl')

CONST_BAD_ID = 148346796186271744 # You-know-who

def get_token():
    with open('token.dat', 'r') as tokenfile:
        return ''.join(
            chr(int(''.join(c), 16))
            for c in zip(*[iter(tokenfile.read().strip())]*2)
            )

def monthdelta(date, delta):
    m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
    if not m: m = 12
    d = min(date.day, calendar.monthrange(y, m)[1])
    return date.replace(day=d, month=m, year=y)

async def get_last_seen(member, pendant=None):
    lastseen = None
    for channel in member.guild.text_channels:
        lastmsg = await channel.history(limit=None, after=pendant).get(author__name=member.display_name)
        if lastmsg and (lastseen is None or lastseen < lastmsg.created_at):
            lastseen = lastmsg.created_at
    return lastseen

@bot.event
async def on_ready():
    print('Ready!')

@bot.event
async def on_guild_join(): # Most likely unnecessary
    pass
    
@bot.event
async def on_message(msg):
    if msg.content == 'good work arquius':
        await msg.channel.send(':sunglasses:')
    else:
        await bot.process_commands(msg)

@bot.event
async def on_message_edit(bfr, aft):
    if bfr.author == bot.user:
        return
    if not hasattr(bfr.channel, 'guild'):
        return
    guild_id = bfr.channel.guild.id
    if guild_id in guild_config.mod_channels:
        embed = dc.Embed(color=dc.Color.gold(), timestamp=aft.created_at)
        embed.set_author(
            name=f'@{bfr.author} edited a message in #{bfr.channel}:',
            icon_url=bfr.author.avatar_url,
            )
        embed.add_field(name='**Before:**', value=bfr.content, inline=False)
        embed.add_field(name='**After:**', value=aft.content, inline=False)
        embed.add_field(name='**MESSAGE ID:**', value=f'`{aft.id}`')
        embed.add_field(name='**USER ID:**', value=f'`{bfr.author.id}`')
        await bot.get_channel(guild_config.mod_channels[guild_id]['msglog']).send(
            embed=embed
            )

@bot.event
async def on_message_delete(msg):
    if not hasattr(msg.channel, 'guild'):
        return
    guild_id = msg.channel.guild.id
    if guild_id in guild_config.mod_channels:
        embed = dc.Embed(
            color=dc.Color.darker_grey(),
            timestamp=msg.created_at,
            description=msg.content,
            )
        embed.set_author(
            name=f'@{msg.author} deleted a message in #{msg.channel}:',
            icon_url=msg.author.avatar_url,
            )
        embed.add_field(name='**MESSAGE ID:**', value=f'`{msg.id}`')
        embed.add_field(name='**USER ID:**', value=f'`{msg.author.id}`')
        await bot.get_channel(guild_config.mod_channels[guild_id]['msglog']).send(
            embed=embed
            )
            
@bot.event
async def on_member_join(member):
    guild = member.guild 
    if guild.id in guild_config.mod_channels:
        await role_saver.load_roles(member)
        embed = dc.Embed(
            color=dc.Color.green(),
            timestamp=datetime.utcnow(),
            description=f':green_circle: **{member}** has joined **{guild}**!\n'
            f'The guild now has {len(guild.members)} members!\n'
            f'This account was created on `{member.created_at.strftime("%d/%m/%Y %H:%M:%S")}`'
            )
        embed.set_author(name=f'A user has joined the server!')
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name='**USER ID:**', value=f'`{member.id}`')
        await bot.get_channel(guild_config.mod_channels[guild.id]['usrlog']).send(
            embed=embed
            )

@bot.event
async def on_member_remove(member):
    guild = member.guild
    if guild.id in guild_config.mod_channels:
        role_saver.save_roles(member)
        timestamp = datetime.utcnow()
        lastseen = await get_last_seen(member, monthdelta(timestamp, -1)) # Moved grabbing last seen to a function
        if lastseen is not None:
            lastseenmsg = f'This user was last seen on `{lastseen.strftime("%d/%m/%Y %H:%M:%S")}`'
        else:
            lastseenmsg = 'This user has not spoken for at least 1 month!'
        embed = dc.Embed(
            color=dc.Color.red(),
            timestamp=timestamp,
            description=f':red_circle: **{member}** has left **{guild}**!\n'
            f'The guild now has {len(guild.members)} members!\n{lastseenmsg}'
            )
        embed.set_author(name=f'A user left or got beaned!')
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(
            name='**ROLES SNAGGED:**',
            value=(', '.join(
                    f'`{guild.get_role(role).name}`'
                    for role in role_saver.get_roles(member)
                    )
                or None),
            inline=False)
        embed.add_field(name='**USER ID:**', value=f'`{member.id}`')
        await bot.get_channel(guild_config.mod_channels[guild.id]['usrlog']).send(
            embed=embed
            )

@bot.event
async def on_member_update(bfr, aft): # Log role and nickname changes
    guild = bfr.guild
    if guild.id in guild_config.mod_channels:
        changetype = None
        if bfr.nick != aft.nick:
            changetype = 'Nickname Update:'
            changelog = f'**{bfr}** had their nickname changed to **{aft.nick}**'
        if bfr.roles != aft.roles:
            changetype = 'Role Update:'
            diffrole = next(iter(set(aft.roles) ^ set(bfr.roles)))
            difftype = 'added' if len(bfr.roles) < len(aft.roles) else 'removed'
            changelog = f'**{aft}** had the following role {difftype}: `{diffrole.name}`'
        if changetype is not None:
            embed = dc.Embed(
                color=dc.Color.blue(),
                timestamp=datetime.utcnow(),
                description=changelog,
                )
            embed.set_author(name=changetype, icon_url=aft.avatar_url)
            embed.add_field(name='**USER ID:**', value=f'`{aft.id}`', inline=False)
            await bot.get_channel(guild_config.mod_channels[guild.id]['usrlog']).send(
                embed=embed
                )

@bot.event
async def on_user_update(bfr, aft): # Log avatar, name, discrim changes
    for guild in bot.guilds:
        if guild.get_member(bfr.id) is not None:
            changetype = None
            if bfr.name != aft.name:
                changetype = 'Username Update:'
                changelog = f'@{bfr} has changed their username to {aft}'
            if bfr.discriminator != aft.discriminator:
                changetype = 'Discriminator Update:'
                changelog = (
                    f'@{bfr} had their discriminator changed from '
                    f'{bfr.discriminator} to {aft.discriminator}'
                    )
            if bfr.avatar != aft.avatar:
                changetype = 'Avatar Update:'
                changelog = f'@{bfr} has changed their avatar to:'
            if changetype is not None:
                embed = dc.Embed(
                    color=dc.Color.purple(),
                    timestamp=datetime.utcnow(),
                    description=changelog,
                    )
                embed.set_author(name=changetype, icon_url=bfr.avatar_url)
                if changetype.startswith('Avatar'):
                    embed.set_thumbnail(url=f'{aft.avatar_url}')
                embed.add_field(name='**USER ID:**', value=f'`{aft.id}`', inline=False)
                await bot.get_channel(guild_config.mod_channels[guild.id]['usrlog']).send(
                    embed=embed
                    )

@bot.command()
async def help(ctx):
    embed = dc.Embed(
        color=ctx.author.color,
        timestamp=ctx.message.created_at,
        description=f'It seems you have asked about the Homestuck and Hiveswap Discord Utility Bot:tm:.'
        f'This is a bot designed to cater to the server\'s moderation, utility, and statistic '
        f'tracking needs. If the functions herein described are not performing to the degree '
        f'that is claimed, please direct your attention to Wizard of Chaos#2459.\n\n'
        f'**Command List:**',
        )
    embed.set_author(name='Help message', icon_url=bot.user.avatar_url)
    embed.add_field(name='`help`', value='Display this message.', inline=False)
    embed.add_field(
        name='`info [username]`',
        value='Grabs user information. Leave username empty to get your own info.',
        inline=False
        )
    embed.add_field(name='`ping`', value='Pong!', inline=False)
    embed.add_field(
        name='`config (msglog|usrlog)`',
        value='(Manage Server only) Sets the appropriate log channel.',
        inline=False
        )
    await ctx.send(embed=embed)

@bot.command()
async def info(ctx, member : str=None):
    if member is not None:
        for gmember in ctx.guild.members:
            if member == gmember.display_name:
                member = gmember
                break
        else:
            await ctx.send(
                'It seems that user can\'t be found. Please check your spelling. '
                'Alternatively, try adding double quotes ("") around the name.'
                )
            return
    else:
        member = ctx.author
    timestamp = datetime.utcnow()
    lastseen = await get_last_seen(member, monthdelta(timestamp, -1))
    if lastseen is not None:
        lastseenmsg = lastseen.strftime("%d/%m/%Y %H:%M:%S")
    else:
        lastseenmsg = 'This user has not spoken for at least 1 month!'
    embed = dc.Embed(color=member.color, timestamp=timestamp)
    embed.set_author(name=f'Information for {member}')
    embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(name='User ID:', value=f'{member.id}')
    embed.add_field(name='Last Seen:', value=lastseenmsg, inline=False)
    embed.add_field(name='Account Created On:', value=member.created_at.strftime('%d/%m/%Y %H:%M:%S'))
    embed.add_field(name='Guild Joined On:', value=member.joined_at.strftime('%d/%m/%Y %H:%M:%S'))
    embed.add_field(name='Roles:', value=', '.join(f'`{role.name}`' for role in member.roles[1:]), inline=False)
    if ctx.author != member:
        msg = 'It seems you\'re a bit of a stalker, aren\'t you?'
    else:
        msg = None
    await ctx.send(msg, embed=embed)

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong, <@!{ctx.message.author.id}>!')

@bot.group()
async def config(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send(
            'It seems that you have attempted to run a nonexistent command. '
            'Would you like to try again? Redos are free, you know.'
            )

@config.command()
async def usrlog(ctx):
    if ctx.author.guild_permissions.manage_guild == True:
        await ctx.send(guild_config.setlog(ctx, 'usrlog'))
    else:
        await ctx.send("It seems that you don't have the appropriate permissions for this command.")
        
@config.command()
async def msglog(ctx):
    if ctx.author.guild_permissions.manage_guild == True:
        await ctx.send(guild_config.setlog(ctx, 'msglog'))
    else:
        await ctx.send("It seems that you don't have the appropriate permissions for this command.")

if __name__ == '__main__':
    bot.run(get_token())
