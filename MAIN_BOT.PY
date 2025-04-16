import discord
from discord.ext import commands
import datetime
import discord
from discord.ext import commands
from discord.ui import View, Button, Modal ,TextInput
import io
from datetime import datetime, timezone , timedelta
import csv
import re
import time
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os
import aiofiles





TOKEN = "Place your Discord bot token here"
intents = discord.Intents.all()  # Enables all privileged and non-privileged intents

# Initialize the bot and disable the default help command
# To change the command prefix, replace '?' with your desired symbol or letter
bot = commands.Bot(command_prefix='?', intents=intents, help_command=None)

# ========================== REQUIRED SETUP VARIABLES ==========================

# If you're unsure how to get these IDs, please refer to the README file (you *were* supposed to read it first 😐)

# IMPORTANT: You must configure ALL the following fields correctly for the bot to work as expected

GUILD_ID = 123456789  # Main server ID (used for Ban Appeals)
APPEAL_SERVER_ID = 123456789  # Appeal server ID where banned users can appeal and open tickets
ADMIN_LOG_CHANNEL_ID = 123456789  # Channel for logging all admin and bot command actions
TRANSCRIPT_CHANNEL_ID = 123456789  # Channel where ticket transcripts will be sent
APPEAL_CATEGORY_ID = 123456789  # Category in the appeal server where tickets should be created
MAIN_TICKET_CATEGORY_ID = 123456789  # Category in the main server for admin-side tickets
APPEAL_SERVER_INVITE = "appeal server link here"  # Invite link to your appeal server
MAINSERVER = "Main server link here"  # Invite link to your main server

# Roles that the auto-mod system should ignore
IGNORED_ROLES = {
    1286638864466841703, 1336694091085512704, 1353719582837440512,
    1353718725718704180, 1351875347414650941, 1352201574663061524
}

# Channels where link posting is blocked
BLOCKED_LINK_CHANNELS = {1286631860818153504, 1296057932093587526}

# Moderator role IDs (used to authorize mod-level commands)
MODERATOR_ROLES = {
    1336694091085512704, 1353719582837440512,
    1352201574663061524, 1351875347414650941
}

INSTA_NOTI_CHANNEL_ID = 123456789  # Channel for Instagram notifications
BOOST_CHANNEL_ID = 123456789  # Channel for sending server boost messages
BOOSTER_ROLE_ID = 123456789  # Role given to server boosters (optional)
NO_XP_ROLE_ID = 123456789  # Users with this role won't gain XP or be moderated
BOT_COMMAND_ID = 123456789  # Channel where level-up messages will be sent
setup_channel_id = 123456789  # Channel in the appeal server to send the appeal button
welcome_channel = 1286649056252264489  # Channel where welcome messages are sent
REACTION_CHANNEL_ID = 1351944866313273495 #Self Roles Channel
SERVER_NAME = "Defender xD  की सेना"  # Name of your server for customization

# These roles should also exist in your server
Banned_role = 1353076332707188868  # Role assigned to banned users
Appeal_role = 1352939183894691870  # Role assigned when a user is appealing



# TICKET_CHANNEL_ID: The channel where the embed is sent (such as a 'ticket creation' or 'support notification' channel)
TICKET_CHANNEL_ID = 1346130286626472040  # Replace with the channel where embed is sent

# TICKET_CATEGORY_ID: The ID of the category where ticket channels should be created. It helps in organizing ticket channels.
TICKET_CATEGORY_ID = 1346130175905103882  # Category where ticket channels go

# TRANSCRIPT_LOG_CHANNEL_ID: The ID of the channel where the transcript of tickets will be sent. 
# This could be an admin channel where all ticket transcriptions are logged.
TRANSCRIPT_LOG_CHANNEL_ID = 1352199804570304583

# SUPPORT_ROLES: Set of role IDs that represent the support team. 
# Members with these roles will have access to the ticket channels (read messages, send messages).
SUPPORT_ROLES = {1353258424149741629, 1336694091085512704, 1352201574663061524, 1353719582837440512}

# Example usage (for context):
# - When creating a ticket, this category and these support roles will be used.
# - The TICKET_CHANNEL_ID will be where notifications or embeds related to tickets are sent.
# - The TICKET_CATEGORY_ID ensures all ticket channels go into a specific category.
# - The SUPPORT_ROLES ensures only specific members can access the ticket channels.


# ========================== AUTO MOD CONFIGURATION ==========================

# You can ignore this section if you're not familiar with how auto moderation works

SPAM_TIMEFRAME = 5  # Seconds within which spam messages are counted
SPAM_MESSAGE_LIMIT = 5  # Max messages allowed in the timeframe
SPAM_WARNING_COOLDOWN = 5  # Cooldown before sending another spam warning
REPEATED_MESSAGE_LIMIT = 3  # Max repeated messages allowed
XP_PER_MESSAGE = 15  # XP given per valid message

# Tracking dictionaries for spam detection and message analysis
user_message_timestamps = {}
user_last_warning = {}
spam_warnings = {}  # {user_id: last_warning_time}
user_messages = {}  # {user_id: [message_id1, message_id2, ...]}
ticket_mappings = {}  # Mapping of appeal tickets for cross-server communication

# List of offensive words detected by the bot
BAD_WORDS = {
    "ngga", "niga", "fck", "f***", "bitch", "bastard", "slut", "whore", 
    "asshole", "dumbass", "shithead", "dickhead", "retard", "cunt",
    "chutiya", "bhosdike", "madarchod", "behenchod", "lund", "gand", 
    "haraamzada", "randi", "kutta", "kamina", "gaand", "suar", "bakchodi"
}

# 👇 Define emojis and their role IDs here
emoji_role_map = {
    "<:bgmi:1354174612383994148>": 1354183320220602379,
    "<:valorant:1354174622236676359>": 1354183395877589062,
    "<:minecraft:1354174618923044956>": 1354183427968073769,
    "<:cod:1354174616142090410>": 1354183518430953775,
    "<:ps:1354174641861824572>": 1354183651465887885,
    "<:AE:1354174629538697337>": 1354183686169301256,
    "<:blender:1354174632810385529>": 1354183623594610798,
    "<:male:1354174639349432361>": 1354183719685984276,
    "<:female:1354174636178280569>": 1354183754683518986,
}

# Compiled regex for detecting bad words
BAD_WORDS_REGEX = re.compile(r"\b(" + "|".join(re.escape(word) for word in BAD_WORDS) + r")\b", re.IGNORECASE)

# ========================== FILES USED BY THE BOT ==========================

CSV_FILE = "xp_data.csv"  # Stores XP data
WARN_FILE = "warns.csv"  # Stores warning data
LINK_REGEX = r"(https?:\/\/[^\s]+|www\.[^\s]+)"  # Regex to detect links

# ========================== OPTIONAL NOTE FOR ADMINS ==========================

# If you want moderators to use admin-only commands:
# Add this line under your command instead of requiring administrator permission:
# @commands.check(lambda ctx: ctx.author.guild_permissions.administrator or any(role.id in MODERATOR_ROLES for role in ctx.author.roles))

 


# 👑 Admin-Only Commands (Accessible only to users with admin permissions)
@bot.command()
@commands.has_permissions(administrator=True)
async def ping(ctx):
    await ctx.send("Pong!")
        
# Custom help command (admin only) 
#command = ?helpadmin
@bot.command(name='helpadmin')
@commands.has_permissions(administrator=True)   
async def custom_help(ctx):
    embed = discord.Embed(
        title="Help - Available Commands",
        description="Here are the commands you can use:",
        color=discord.Color.from_rgb(255, 255, 255)
    )
    
    embed.add_field(
        name="?ban <@user> reason | proof ",
        value="Ban a user from the server.",
        inline=False
    )
    embed.add_field(
        name="?aboutowner",
        value="Display information about the server owner.",
        inline=False
    )
    embed.add_field(
        name="?rules",
        value="Show server rules.",
        inline=False
    )
    embed.add_field(
        name="?selfroles  ",
        value="Sends self roles  .",
        inline=False
    )

    embed.add_field(
        name="?ping",
        value="Tells the bot is working ",
        inline=False
    )
    embed.add_field(
        name="?unban <@user>  ",
        value="UnBan a user from the server.",
        inline=False
    )
    embed.add_field(
        name="?kick <@user> reason ",
        value="Kicks a user from the server .",
        inline=False
    )
    embed.add_field(
        name="?mute <@user> time reason (time is in minutes)",
        value="Mutes a user  .",
        inline=False
    )
    embed.add_field(
        name="?unmute <@user> ",
        value="Unmutes a User  .",
        inline=False
    )
    embed.add_field(
        name="?warn <@user> reason ",
        value="Warns a user  .",
        inline=False
    )
    embed.add_field(
        name="?warns <@user> ",
        value="See how many warns he has   .",
        inline=False
    )
    embed.add_field(
        name="?clearwarn <@user> ",
        value="Clears his warn  .",
        inline=False
    )
    embed.add_field(
        name="?purge <amount of messsages> ",
        value="Deletes the message , cant do more than 100 .",
        inline=False
    )
    embed.add_field(
        name="?insta_noti <link> ",
        value=f"Sends Instagram Notification **https://discord.com/channels/1286631860197392396/1287082090587754588**  .",
        inline=False
    )
    embed.add_field(
        name="?reset <@user> ",
        value=f"Resets the user exp  .",
        inline=False
    )
    embed.add_field(
        name="?reset_all ",
        value=f"Resets the server exp and leaderboard   .",
        inline=False
    )
    embed.add_field(
        name="?addxp <@user> ",
        value=f"Adds exp to the user   .",
        inline=False
    )

    
    embed.timestamp = ctx.message.created_at
    await ctx.send(embed=embed)
    await ctx.message.delete()





@bot.command(name='helpadminstatus')
@commands.has_permissions(administrator=True)
async def custom_help(ctx):
    embed = discord.Embed(
        title="Help - Available Status Commands",
        description="Here are the commands you can use for status :",
        color=discord.Color.from_rgb(255, 255, 255)
    )

    embed.add_field(
        name="?setstatus livestream <link>",
        value="Set the bot's status to 'Live on Stream!' with a link to your stream.",
        inline=False
    )
    embed.add_field(
        name="?setstatus video <link>",
        value="Set the bot's status to watching the new video with link",
        inline=False
    )
    embed.add_field(
        name="?setstatus watching <content>",
        value="Set the bot's status to 'Watching <content>' (e.g., Watching a movie).",
        inline=False
    )
    embed.add_field(
        name="?setstatus listening <content>",
        value="Set the bot's status to 'Listening to <content>' (e.g., Listening to music).",
        inline=False
    )
    embed.add_field(
        name="?setstatus playing <game>",
        value="Set the bot's status to 'Playing <game>' (e.g., Playing Fortnite).",
        inline=False
    )
    embed.add_field(
        name="?setstatus custom <content>",
        value="Set a custom status for the bot (e.g., Custom message or status).",
        inline=False
    )
    embed.add_field(
        name="?setstatus idle",
        value="Set the bot's status to 'Idle'. This status appears as if the bot is not actively online.",
        inline=False
    )
    embed.add_field(
        name="?setstatus dnd <content>",
        value="Set the bot's status to 'Do Not Disturb' with a custom message (e.g., Do Not Disturb - Busy).",
        inline=False
    )
    embed.add_field(
        name="?setstatus invisible <content>",
        value="Set the bot's status to 'Invisible'. The bot appears offline while still being able to interact.",
        inline=False
    )
    
    embed.timestamp = ctx.message.created_at
    await ctx.send(embed=embed)
    await ctx.message.delete()




@bot.command()
@commands.has_permissions(administrator=True)
async def setstatus(ctx, mode: str, *, content):
    log_channel = bot.get_channel(ADMIN_LOG_CHANNEL_ID)

    if mode.lower() == "livestream":
        stream_title = "Live on Youtube!"
        stream_url = content
        activity = discord.Streaming(name=stream_title, url=stream_url)
        await bot.change_presence(activity=activity)

        button = Button(label="🎥 Watch Stream", url=stream_url, style=discord.ButtonStyle.link)
        view = View()
        view.add_item(button)

        embed = discord.Embed(
            title="📡 Bot Status Updated!",
            description=f"Now streaming: **{stream_title}**",
            color=discord.Color.purple()
        )
        await ctx.send(embed=embed, view=view, delete_after=3)
        await ctx.message.delete()

        if log_channel:
            log_embed = discord.Embed(
                title="🔧 Status Changed to Livestream",
                description=f"**By:** {ctx.author.mention}\n**Stream URL:** [Click Here]({stream_url})",
                color=discord.Color.purple()
            )
            log_embed.set_footer(text=f"User ID: {ctx.author.id}")
            await log_channel.send(embed=log_embed)
            await ctx.message.delete()

    # Video status (new mode to watch a video)
    elif mode.lower() == "video":
        video_title = "New Video"
        video_url = content
        activity = discord.Streaming(name=video_title, url=video_url)
        await bot.change_presence(activity=activity)

        # Create a button
        button = Button(label="▶️ Watch Video", url=video_url, style=discord.ButtonStyle.link)
        view = View()
        view.add_item(button)

        embed = discord.Embed(
            title="📺 Bot Status Updated!",
            description=f"Now watching: **{video_title}**",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed, view=view, delete_after=3)
        await ctx.message.delete()

    # Watching status
    elif mode.lower() == "watching":
        activity = discord.Activity(type=discord.ActivityType.watching, name=content)
        await bot.change_presence(activity=activity)
        await ctx.send(f"✅ Status updated to: Watching {content}")

        # Log to admin channel
        if log_channel:
            log_embed = discord.Embed(
                title="🔧 Status Changed to Watching",
                description=f"**By:** {ctx.author.mention}\n**New Status:** Watching {content}",
                color=discord.Color.green()
            )
            log_embed.set_footer(text=f"User ID: {ctx.author.id}")
            await log_channel.send(embed=log_embed)
            await ctx.message.delete()

    # Listening status
    elif mode.lower() == "listening":
        activity = discord.Activity(type=discord.ActivityType.listening, name=content)
        await bot.change_presence(activity=activity)
        await ctx.send(f"✅ Status updated to: Listening to {content}")

        # Log to admin channel
        if log_channel:
            log_embed = discord.Embed(
                title="🔧 Status Changed to Listening",
                description=f"**By:** {ctx.author.mention}\n**New Status:** Listening to {content}",
                color=discord.Color.green()
            )
            log_embed.set_footer(text=f"User ID: {ctx.author.id}")
            await log_channel.send(embed=log_embed)
            await ctx.message.delete()

    # Playing status
    elif mode.lower() == "playing":
        activity = discord.Game(name=content)
        await bot.change_presence(activity=activity)
        await ctx.send(f"✅ Status updated to: Playing {content}")

        # Log to admin channel
        if log_channel:
            log_embed = discord.Embed(
                title="🔧 Status Changed to Playing",
                description=f"**By:** {ctx.author.mention}\n**New Status:** Playing {content}",
                color=discord.Color.green()
            )
            log_embed.set_footer(text=f"User ID: {ctx.author.id}")
            await log_channel.send(embed=log_embed)
            await ctx.message.delete()

    # Custom status
    elif mode.lower() == "custom":
        activity = discord.Activity(type=discord.ActivityType.custom, name=content)
        await bot.change_presence(activity=activity)
        await ctx.send(f"✅ Custom status set to: {content}")

        # Log to admin channel
        if log_channel:
            log_embed = discord.Embed(
                title="🔧 Custom Status Set",
                description=f"**By:** {ctx.author.mention}\n**Custom Status:** {content}",
                color=discord.Color.green()
            )
            log_embed.set_footer(text=f"User ID: {ctx.author.id}")
            await log_channel.send(embed=log_embed)
            await ctx.message.delete()

    # Idle status (changes actual presence status)
    elif mode.lower() == "idle":
        activity = discord.Game(name=content)
        await bot.change_presence(status=discord.Status.idle, activity=activity)
        await ctx.send(f"✅ Status updated to: Idle - {content}")

        # Log to admin channel
        if log_channel:
            log_embed = discord.Embed(
                title="🔧 Status Changed to Idle",
                description=f"**By:** {ctx.author.mention}\n**New Status:** Idle - {content}",
                color=discord.Color.orange()
            )
            log_embed.set_footer(text=f"User ID: {ctx.author.id}")
            await log_channel.send(embed=log_embed)
            await ctx.message.delete()

    # Do Not Disturb (DND) status (changes actual presence status)
    elif mode.lower() == "dnd":
        activity = discord.Game(name=content)
        await bot.change_presence(status=discord.Status.dnd, activity=activity)
        await ctx.send(f"✅ Status updated to: Do Not Disturb - {content}")

        # Log to admin channel
        if log_channel:
            log_embed = discord.Embed(
                title="🔧 Status Changed to DND",
                description=f"**By:** {ctx.author.mention}\n**New Status:** DND - {content}",
                color=discord.Color.red()
            )
            log_embed.set_footer(text=f"User ID: {ctx.author.id}")
            await log_channel.send(embed=log_embed)
            await ctx.message.delete()

    # Invisible status (changes actual presence status)
    elif mode.lower() == "invisible":
        activity = discord.Game(name=content)
        await bot.change_presence(status=discord.Status.invisible, activity=activity)
        await ctx.send(f"✅ Status updated to: Invisible - {content}")

        # Log to admin channel
        if log_channel:
            log_embed = discord.Embed(
                title="🔧 Status Changed to Invisible",
                description=f"**By:** {ctx.author.mention}\n**New Status:** Invisible - {content}",
                color=discord.Color.dark_gray()
            )
            log_embed.set_footer(text=f"User ID: {ctx.author.id}")
            await log_channel.send(embed=log_embed)
            await ctx.message.delete()

    else:
        await ctx.send("❌ Invalid status mode! Use `?setstatushelp` for a list of available modes.",delete_after=5)

    await ctx.message.delete()


@bot.command()
@commands.has_permissions(administrator=True)
async def clearstatus(ctx):
    await bot.change_presence(activity=None, status=discord.Status.online)
    
    embed = discord.Embed(
        title="✅ Status Cleared",
        description="The bot's status has been reset to default.",
        color=discord.Color.red()
    )
    await ctx.send(embed=embed,delete_after=3)
    await ctx.message.delete()


    # Log to admin channel
    log_channel = bot.get_channel(ADMIN_LOG_CHANNEL_ID)
    if log_channel:
        log_embed = discord.Embed(
            title="🔻 Bot Status Cleared",
            description=f"**By:** {ctx.author.mention}",
            color=discord.Color.red()
        )
        log_embed.set_footer(text=f"User ID: {ctx.author.id}")
        await log_channel.send(embed=log_embed)


#Resets the exp of the user
@bot.command(name="reset")
@commands.has_permissions(administrator=True)
async def reset(ctx, member: discord.Member):
    """Resets XP and Level of a specific user"""
    xp_data = load_xp_data()

    if member.id in xp_data:
        xp_data[member.id] = {"xp": 0, "level": 0}
        save_xp_data(xp_data)
        log_channel = ctx.guild.get_channel(ADMIN_LOG_CHANNEL_ID)
        if log_channel:
            embed = discord.Embed(
                title="🗑️ Reset XP",
                description=f"**User:** {ctx.author.mention}\n**Target:** {member.mention}\n**Action:** Reset XP & Level",
                color=discord.Color.red()
            )
            embed.set_footer(text=f"Executed by: {ctx.author.display_name}")
            await log_channel.send(embed=embed)

        await ctx.send(f"✅ {member.mention}'s XP and level have been reset!")
    else:
        await ctx.send(f"⚠️ {member.mention} has no XP data yet!")

#Rest the exp of all the member of server
@bot.command(name="reset_all")
@commands.has_permissions(administrator=True)
async def reset_all(ctx):
    """Resets XP and Levels of all users in the server"""
    xp_data = load_xp_data()

    for user_id in xp_data.keys():
        xp_data[user_id] = {"xp": 0, "level": 0}

    save_xp_data(xp_data)
    log_channel = ctx.guild.get_channel(ADMIN_LOG_CHANNEL_ID)
    if log_channel:
        embed = discord.Embed(
            title="🗑️ Reset All XP",
            description=f"**User:** {ctx.author.mention}\n**Action:** Reset XP & Levels for all members",
            color=discord.Color.red()
        )
        embed.set_footer(text=f"Executed by: {ctx.author.display_name}")
        await log_channel.send(embed=embed)

    await ctx.send("✅ All users' XP and levels have been reset!")

#Adds exp to a member
@bot.command(name="addexp")
@commands.has_permissions(administrator=True)
async def addxp(ctx, member: discord.Member, amount: int):
    """Adds XP to a specific user"""
    if amount <= 0:
        await ctx.send("⚠️ Please enter a positive amount of XP.")
        return

    xp_data = load_xp_data()
    user_stats = xp_data.get(member.id, {"xp": 0, "level": 0})

    user_stats["xp"] += amount

    # Check for level-up
    while user_stats["xp"] >= xp_needed(user_stats["level"] + 1):
        user_stats["level"] += 1
        user_stats["xp"] -= xp_needed(user_stats["level"])

    xp_data[member.id] = user_stats
    save_xp_data(xp_data)
    log_channel = ctx.guild.get_channel(ADMIN_LOG_CHANNEL_ID)
    if log_channel:
        embed = discord.Embed(
            title="➕ Added XP",
            description=f"**User:** {ctx.author.mention}\n**Target:** {member.mention}\n**XP Added:** {amount}",
            color=discord.Color.green()
        )
        embed.set_footer(text=f"Executed by: {ctx.author.display_name}")
        await log_channel.send(embed=embed)
    

    await ctx.send(f"✅ Added {amount} XP to {member.mention}. They are now Level {user_stats['level']} with {user_stats['xp']} XP.")


#About owner (You have to fill this data manually zzzzzzz)
@commands.has_permissions(administrator=True)
@bot.command()
async def aboutowner(ctx):
    birthdate = datetime.date(2008, 2, 20)  # Your birthdate  #Update this on your own :)
    today = datetime.date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

    embed = discord.Embed(
        title=" <a:rocket_animated:1296099979961696329> **ABOUT DEFENDER XD**",
        description=(
            "\n\u200B"  # Adds spacing
            "**<a:JumpingStar:1296099466159456380> ️ PERSONAL DETAILS**\n\n"
            f"**•ㅤName:** Swastik Kaushal\n"
            f"**•ㅤAge:** {age}\n"
            f"**•ㅤFrom:** New Delhi, India\n"
            "\n\u200B"

            "**<a:JumpingStar:1296099466159456380> ️ SOCIAL MEDIA LINKS**\n\n"
            f"**•  **<a:Instagram:1351462316322983976> **Instagram:**ㅤ[defenderxd](https://www.instagram.com/defenderxd/)\n"
            f"**•  **<a:YOUTUBE:1351462319791673388> **YouTube:**ㅤ[DefenderXD](https://www.youtube.com/@DefenderXD)\n"
            f"**•         **<a:Twitch_Logo_Animated:1351462324501876788> **Twitch:**ㅤ[defendersxd](https://www.twitch.tv/defendersxd)\n"
            "\n\u200B"

            "**<a:JumpingStar:1296099466159456380> ️ PC SPECIFICATIONS**\n\n"
            "**•ㅤMotherboard:** Gigabyte H310S2H 2.0\n"
            "**•ㅤRAM:** 8GB\n"
            "**•ㅤStorage:** 500GB HDD, 480GB SSD\n"
            "**•ㅤGPU:** GT 710\n"
            "**•ㅤCPU:** i3 9th Gen\n"
            "**•ㅤMouse:** Razer DeathAdder Essential\n"
            "**•ㅤMonitor:** Acer 60Hz 720p\n"
            "**•ㅤKeyboard:** Zebronics\n"
            "**•ㅤPSU:** 450W\n"
        ),
        color=discord.Color.from_rgb(255, 255, 255)  # White Embed Color
    )

    embed.set_image(url="https://i.postimg.cc/sDbFLb0x/ABOUT.jpg")  # Replace with your image URL , any thumbnail or use mine for now

    await ctx.send(embed=embed)

#Delets multiple Messages at once
@bot.command()
@commands.has_permissions(administrator=True)  
async def purge(ctx, amount: int):
    if amount <= 100:  
        deleted = await ctx.channel.purge(limit=amount + 1)  
        await ctx.send(f"✅ Deleted {len(deleted)} messages!", delete_after=3)
        
        log_channel = ctx.guild.get_channel(ADMIN_LOG_CHANNEL_ID)
        if log_channel:
            embed = discord.Embed(
                title="🗑️ Purge Command Used",
                description=(
                    f"**User:** {ctx.author.mention}\n"
                    f"**Messages Deleted:** {len(deleted)}\n"
                    f"**Channel:** {ctx.channel.mention}"
                ),
                color=discord.Color.orange()
            )
            embed.set_footer(text=f"Executed by: {ctx.author.display_name}")
            await log_channel.send(embed=embed)

    else:
        await ctx.send("❌ Cannot delete more than 100 messages at a time!", delete_after=3)

        
# Rules Command (Properly spaced and formatted)
#(You  only have to change the server name )
@bot.command()
@commands.has_permissions(administrator=True)
async def rules(ctx):
    embed = discord.Embed(
        title="<a:minecraftenchant:1351439263916625920> **SERVER RULES OF DEFENDER XD **",
        description=(
            "\n\u200B"  # Adds spacing to widen the embed
            "<a:readbook:1351439257314525245> **WELCOME TO THE SERVER**\n"
            "Welcome to the **Defender xD Community!** 🎉\n"
            "Please follow the rules to keep the server safe & fun for everyone.\n"
            "\n\u200B"

            "<a:JumpingStar:1296099466159456380> **DISCORD COMMUNITY GUIDELINES**\n"
            "This server follows **Discord’s official guidelines.** Please review them:\n"
            "<a:Discord:1351440168803893343> **[Discord Community Guidelines](https://discord.com/guidelines)**\n"
            "<a:Discord:1351440168803893343> **[Discord Terms of Service](https://discord.com/terms)**\n"
            "\n\u200B"

            "<a:JumpingStar:1296099466159456380> **SERVER RULES**\n\n"
            "<a:Arrow_right:1351456353037586475> Be Respectful  –  No harassment, hate speech, or discrimination.\n\n"
            "<a:Arrow_right:1351456353037586475> No Spamming  –  Avoid excessive messages, emojis, or mentions.\n\n"
            "<a:Arrow_right:1351456353037586475> Stay on Topic  –  Use the correct channels for discussions.\n\n"
            "<a:Arrow_right:1351456353037586475> No Self-Promotion  –  Don't advertise without permission.\n\n"
            "<a:Arrow_right:1351456353037586475> Keep it Safe  –  No NSFW, illegal, or offensive content.\n\n"
            "<a:Arrow_right:1351456353037586475> Follow Staff Instructions  –  Moderators have the final say.\n"
            "\n\u200B"

            "<a:JumpingStar:1296099466159456380> **TEXT CHANNEL RULES**\n\n"
            "<a:Arrow_right:1351456353037586475> No spamming or flooding the chat. Do not type in ALL CAPS & limit to 4 emojis per line.\n\n"
            "<a:Arrow_right:1351456353037586475> No advertising other sites/Discord servers (unless permitted by staff).\n\n"
            "<a:Arrow_right:1351456353037586475> No offensive usernames.\n\n"
            "<a:Arrow_right:1351456353037586475> No nuisance behavior. Repeated complaints may lead to administrative action.\n\n"
            "<a:Arrow_right:1351456353037586475> No controversial discussions. Avoid topics that can cause serious issues.\n\n"
            "<a:Arrow_right:1351456353037586475> No inappropriate profile pictures.\n\n"
            "<a:Arrow_right:1351456353037586475> No personal bots or exploiting Discord glitches.\n\n"
            "<a:Arrow_right:1351456353037586475> No doxing. Don't share personal/private information.\n\n"
            "<a:Arrow_right:1351456353037586475> No discussions on Sexism, Racism, Religion, Politics, or Sexual content.\n\n"
            "<a:Arrow_right:1351456353037586475> Only English or Hinglish is allowed in text chats.\n\n"
            "<a:Arrow_right:1351456353037586475> No DM promotions.\n\n"
            "<a:Arrow_right:1351456353037586475> Don't tag admins unnecessarily.\n\n"
            "<a:Arrow_right:1351456353037586475> Do not ask for roles.\n\n"
            "<a:Arrow_right:1351456353037586475> No NSFW content (gore, pornography, rule34, etc.). Any violation will lead to a ban.\n"
            "\n\u200B"

            "<a:JumpingStar:1296099466159456380> VOICE CHANNEL RULES\n\n"
            "<a:Arrow_right:1351456353037586475> No NSFW noises, earrape, or disturbing others. Instant mute will be applied.\n\n"
            "<a:Arrow_right:1351456353037586475> No bullying or abusive language.\n\n"
            "<a:Arrow_right:1351456353037586475> Notify before recording.** Get approval before recording voice conversations.\n\n"
            "<a:Arrow_right:1351456353037586475> No voice changers or text-to-speech software.\n\n"
            "<a:Arrow_right:1351456353037586475> Do not argue with staff in voice channels.\n\n"
            
        ),
        color=discord.Color.from_rgb(255, 255, 255)  # White Embed Color
    )
    embed3 = discord.Embed(
        title=" <a:JumpingStar:1296099466159456380> **Additional Information**",
        description=(
            "<a:Arrow_right:1351456353037586475> **Breaking rules will result in consequences:**\n"
            "• 1st Offense → Warning ⚠️\n"
            "• 2nd Offense → Temporary Mute ⏳\n"
            "• 3rd Offense → Kick 🚪\n"
            "• Repeated Violations → Permanent Ban 🔨\n\n"
            
            "<a:Arrow_right:1351456353037586475> **Moderators and Admins have authority to enforce rules.**\n"
            "• Some rules may not apply to staff members when executing their duties.\n"
            "• If you feel a mod is being unfair, **report it to higher management**.\n\n"
            
            "<a:Arrow_right:1351456353037586475> **Report Rule Breakers** \n"
            "• If you see someone breaking rules, report them to a mod instead of arguing.\n\n"
            
            "<a:Arrow_right:1351456353037586475> **Appealing Bans/Penalties**\n"
            "• If you were unfairly punished, you can appeal to staff in DMs.\n"
        ),
        color=discord.Color.from_rgb(255, 255, 255)
        
    )
    embed3.set_image(url="https://i.postimg.cc/zBLKxdtC/RULES.jpg") #Change the image from here

    await ctx.send(embed=embed)
    await ctx.send(embed=embed3)
    await ctx.message.delete()  


@bot.command()
@commands.has_permissions(administrator=True)
async def selfrole(ctx):
    # First Embed - Image Only
    embed1 = discord.Embed(title="", color=discord.Color.from_rgb(255, 255, 255))
    embed1.set_image(url="https://i.postimg.cc/VvhLkkCQ/self-roles.jpg")
    await ctx.send(embed=embed1)

    # Second Embed - Game Roles
    embed2 = discord.Embed(
        title="<a:JumpingStar:1296099466159456380> **Choose Your Game Roles!**",
        description=(
            "<:bgmi:1354174612383994148> **BGMI** – `PUBG Mobile India`\n"
            "<:valorant:1354174622236676359> **Valorant** – `Tactical FPS Game`\n"
            "<:minecraft:1354174618923044956> **Minecraft** – `Sandbox Building Game`\n"
            "<:cod:1354174616142090410> **Call of Duty** – `COD Mobile / Warzone`\n"
        ),
        color=discord.Color.from_rgb(255, 255, 255)
    )
    embed2.set_footer(text="React to get your preferred game role!")
    msg2 = await ctx.send(embed=embed2)
    for emoji in ["<:bgmi:1354174612383994148>", "<:valorant:1354174622236676359>", "<:minecraft:1354174618923044956>", "<:cod:1354174616142090410>"]:
        await msg2.add_reaction(emoji)

    # Third Embed - Software Roles
    embed3 = discord.Embed(
        title="<a:JumpingStar:1296099466159456380> **Choose Your Software Roles!**",
        description=(
            "<:ps:1354174641861824572> **Photoshop** – `Photo Editing & Design`\n"
            "<:AE:1354174629538697337> **After Effects** – `Video Editing & VFX`\n"
            "<:blender:1354174632810385529> **Blender** – `3D Modeling & Animation`\n"
        ),
        color=discord.Color.from_rgb(255, 255, 255)
    )
    embed3.set_footer(text="React to select the software you use!")
    msg3 = await ctx.send(embed=embed3)
    for emoji in ["<:ps:1354174641861824572>", "<:AE:1354174629538697337>", "<:blender:1354174632810385529>"]:
        await msg3.add_reaction(emoji)

    # Fourth Embed - Gender Roles
    embed4 = discord.Embed(
        title="<a:JumpingStar:1296099466159456380> **Choose Your Gender!**",
        description=(
            "<:male:1354174639349432361> **Male**\n"
            "<:female:1354174636178280569> **Female**\n"
        ),
        color=discord.Color.from_rgb(255, 255, 255)
    )
    embed4.set_footer(text="React to identify yourself!")
    msg4 = await ctx.send(embed=embed4)
    for emoji in ["<:male:1354174639349432361>", "<:female:1354174636178280569>"]:
        await msg4.add_reaction(emoji)

    await ctx.message.delete()


@bot.event
async def on_raw_reaction_add(payload):
    # Check if the reaction is in the correct channel
    if payload.channel_id != REACTION_CHANNEL_ID:
        return

    emoji_str = str(payload.emoji)
    role_id = emoji_role_map.get(emoji_str)
    if role_id is None:
        return

    # Get the guild and member who reacted
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    if member is None or member.bot:
        return

    # Get the role to be assigned
    role = guild.get_role(role_id)
    if role:
        await member.add_roles(role)
        
        # Log the role assignment in the log channel
        log_channel = guild.get_channel(ADMIN_LOG_CHANNEL_ID)
        if log_channel:
            embed = discord.Embed(
                title="Role Assigned",
                description=f"**User:** {member.mention}\n**Role:** {role.name}",
                color=discord.Color.green()
            )
            embed.set_footer(text=f"Assigned by: {member.display_name}")
            await log_channel.send(embed=embed)


@bot.event
async def on_raw_reaction_remove(payload):
    # Check if the reaction is in the correct channel
    if payload.channel_id != REACTION_CHANNEL_ID:
        return

    emoji_str = str(payload.emoji)
    role_id = emoji_role_map.get(emoji_str)
    if role_id is None:
        return

    # Get the guild and member who removed the reaction
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    if member is None or member.bot:
        return

    # Get the role to be removed
    role = guild.get_role(role_id)
    if role and role in member.roles:
        await member.remove_roles(role)

        # Log the role removal in the log channel
        log_channel = guild.get_channel(ADMIN_LOG_CHANNEL_ID)
        if log_channel:
            embed = discord.Embed(
                title="Role Removed",
                description=f"**User:** {member.mention}\n**Role:** {role.name}",
                color=discord.Color.red()
            )
            embed.set_footer(text=f"Removed by: {member.display_name}")
            await log_channel.send(embed=embed)



#If the bot by chances restart then the buttons wont work for then its there (only for appeal ticket)
@bot.command(name="unbanappeal")
@commands.has_permissions(administrator=True)
async def unban_appeal(ctx):
    if not ctx.channel.name.startswith("appeal-"):
        return await ctx.send("❌ This command can only be used in appeal channels.", delete_after=5)

    if not ctx.author.guild_permissions.administrator:
        return await ctx.send("❌ You don't have permission to do this.", delete_after=5)

    appeal_server = bot.get_guild(APPEAL_SERVER_ID)
    main_guild = ctx.guild

    try:
        user_id = int(ctx.channel.name.replace("appeal-", ""))
    except ValueError:
        return await ctx.send("❌ Invalid user ID format in channel name.", delete_after=5)

    try:
        user = await bot.fetch_user(user_id)
    except Exception as e:
        return await ctx.send(f"❌ Error fetching user: {e}", delete_after=5)

    try:
        await main_guild.unban(discord.Object(id=user_id))
        try:
            await user.send(f"✅ You have been unbanned from {main_guild.name}. You can rejoin using this link: {MAINSERVER}")
        except discord.Forbidden:
            await ctx.send("⚠️ Unable to send DM. The user may have DMs disabled.", delete_after=5)
    except discord.NotFound:
        return await ctx.send("❌ User is not banned.", delete_after=5)
    except discord.Forbidden:
        return await ctx.send("❌ I don't have permission to unban this user.", delete_after=5)
    except Exception as e:
        return await ctx.send(f"❌ Unexpected error unbanning user: {e}", delete_after=5)

    member = appeal_server.get_member(user_id)
    if not member:
        member = await appeal_server.fetch_member(user_id)  # Try fetching if not in cache

    if member:
        try:
            await member.kick(reason="Appeal Accepted")
        except discord.Forbidden:
            return await ctx.send("❌ I don't have permission to kick this user from the appeal server.", delete_after=5)
        except Exception as e:
            return await ctx.send(f"❌ Error kicking user from appeal server: {e}", delete_after=5)
    else:
        await ctx.send("⚠️ User is not in the appeal server or already left.", delete_after=5)


    await ctx.send(view=CloseTicketOptionsmanual(ctx.channel))


#If the bot by chances restart then the buttons wont work for then its there   (only for appeal ticket)
@bot.command(name="adduser")
@commands.has_permissions(administrator=True)
async def add_user(ctx, user: discord.Member):
    if not ctx.channel.name.startswith("appeal-"):
        return await ctx.send("❌ This command can only be used in appeal channels.", delete_after=5)

    if not ctx.author.guild_permissions.administrator:
        return await ctx.send("❌ You don't have permission to do this.", delete_after=5)

    try:
        await ctx.channel.set_permissions(user, read_messages=True, send_messages=True)
        await ctx.send(f"✅ {user.mention} has been added to the ticket!")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

class CloseTicketOptionsmanual(discord.ui.View):
    def __init__(self, main_ticket):
        super().__init__(timeout=None)
        self.main_ticket = main_ticket

    @discord.ui.button(label="📜 Transcript Ticket", style=discord.ButtonStyle.primary)
    async def transcript_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ You don't have permission to do this.", ephemeral=True)
            return

        messages = []
        async for msg in self.main_ticket.history(limit=1000):
            messages.append(f"[{msg.created_at}] {msg.author}: {msg.content}")

        transcript_text = "\n".join(reversed(messages))
        transcript_file = discord.File(io.StringIO(transcript_text), filename="transcript.txt")

        log_channel = interaction.guild.get_channel(TRANSCRIPT_CHANNEL_ID)
        if log_channel:
            await log_channel.send("📜 Transcript of closed ticket:", file=transcript_file)

        await interaction.response.send_message("✅ Transcript has been sent to the appeal log.", ephemeral=True)
        
    @discord.ui.button(label="🗑️ Delete Chat", style=discord.ButtonStyle.danger)
    async def delete_chat(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ You don't have permission to do this.", ephemeral=True)
            return

        if self.main_ticket:
            await self.main_ticket.delete()
            await interaction.response.send_message("🗑️ Ticket chat has been deleted.", ephemeral=True)

#If the bot by chances restart then the buttons wont work for then its there   (only for appeal ticket)
@bot.command(name="closeappeal")
@commands.has_permissions(administrator=True)
async def close_appeal(ctx):
    if not ctx.channel.name.startswith("appeal-"):
        return await ctx.send("❌ This command can only be used in appeal channels.", delete_after=5)

    if not ctx.author.guild_permissions.administrator:
        return await ctx.send("❌ You don't have permission to do this.", delete_after=5)

    appeal_server = bot.get_guild(APPEAL_SERVER_ID)

    user_id_str = ctx.channel.name.replace("appeal-", "")
    try:
        user_id = int(user_id_str)
    except ValueError:
        return await ctx.send("❌ Invalid user ID format in channel name.", delete_after=5)

    member = appeal_server.get_member(user_id)
    if not member:
        try:
            member = await appeal_server.fetch_member(user_id) 
        except discord.NotFound:
            print(f"[ERROR] Member with ID {user_id} not found in appeal server.")
            return await ctx.send("❌ User not found in the appeal server.", delete_after=5)
        except discord.Forbidden:
            print(f"[ERROR] Missing permissions to fetch member.")
            return await ctx.send("❌ I don't have permission to fetch members.", delete_after=5)


    role = appeal_server.get_role(Appeal_role)  

    if role and role in member.roles:
        try:
            await member.remove_roles(role)
        except discord.Forbidden:
            return await ctx.send("❌ I don't have permission to remove roles.", delete_after=5)
    else:
        print(f"[DEBUG] Member does not have the '{role.name}' role.")

    try:
        user = await bot.fetch_user(user_id)
        await user.send("❌ Your appeal request has been closed. Feel free to retry after 2 weeks.")
    except discord.Forbidden:
        print("error")
        

    await ctx.send(view=CloseTicketOptionsmanual(ctx.channel))

    appeal_channel = discord.utils.get(appeal_server.text_channels, name=ctx.channel.name)
    if appeal_channel:
        try:
            await appeal_channel.delete()
        except Exception as e:
            print(f"[ERROR] Failed to delete appeal ticket: {e}")
    else:
        print(f"[DEBUG] No matching channel found in appeal server for {ctx.channel.name}")

#If the bot by chances restart then the buttons wont work for then its there   (only for appeal ticket)
@bot.command(name="banappeal")
@commands.has_permissions(administrator=True)
async def ban_appeal(ctx):
    if not ctx.channel.name.startswith("appeal-"):
        return await ctx.send("❌ This command can only be used in appeal channels.", delete_after=5)

    appeal_server = bot.get_guild(APPEAL_SERVER_ID)
    if not appeal_server:
        return await ctx.send("❌ Appeal server not found.", delete_after=5)

    user_id_str = ctx.channel.name.replace("appeal-", "")

    try:
        user_id = int(user_id_str)
    except ValueError:
        return await ctx.send("❌ Invalid user ID format in channel name.", delete_after=5)

    member = appeal_server.get_member(user_id)
    
    if not member:
        try:
            member = await appeal_server.fetch_member(user_id)  # Try fetching if not in cache
        except discord.NotFound:
            return await ctx.send("❌ User not found in the appeal server.", delete_after=5)
        except discord.Forbidden:
            return await ctx.send("❌ I don't have permission to fetch members.", delete_after=5)

    try:
        await member.send("❌ Your appeal has been rejected. You have been permanently banned from the server.")
    except discord.Forbidden:
        print(f"[WARNING] Could not send DM to {member} (DMs disabled).")

    try:
        await appeal_server.ban(member, reason="Appeal rejected - Permanent ban")
        await ctx.send(f"✅ {member} has been banned from the appeal server.", delete_after=5)
    except discord.Forbidden:
        return await ctx.send("❌ I don't have permission to ban this user. Check my role position and permissions.", delete_after=5)
    except Exception as e:
        return await ctx.send(f"❌ Error banning user: {e}", delete_after=5)

    await ctx.send(view=CloseTicketOptionsmanual(ctx.channel))

    appeal_channel = discord.utils.get(appeal_server.text_channels, name=ctx.channel.name)
    if appeal_channel:
        try:
            await appeal_channel.delete()
        except Exception as e:
            print(f"[ERROR] Failed to delete appeal ticket: {e}")
    else:
        print(f"[DEBUG] No matching channel found in appeal server for {ctx.channel.name}")
        



@bot.command()
@commands.check(lambda ctx: ctx.author.guild_permissions.administrator or any(role.id in SUPPORT_ROLES for role in ctx.author.roles))
async def close_ticketsupp(ctx):
    ticket_channel = ctx.channel  # Get the ticket channel

    # Check if the channel is a valid ticket channel (e.g., starts with "ticket-")
    if not ticket_channel.name.startswith("ticket-"):
        await ctx.send("❌ This is not a valid ticket channel.")
        return

    # Ensure that the user has permission to manage channels (staff/owners)
    if not ctx.author.guild_permissions.manage_channels:
        await ctx.send("❌ You do not have permission to close this ticket.", ephemeral=True)
        return

    # Lock the ticket: remove view/send access from everyone except staff
    overwrites = ticket_channel.overwrites

    # Revoke permission for everyone except staff and the bot
    for target in overwrites:
        if isinstance(target, discord.Member) or isinstance(target, discord.User):
            # Revoke for individual users (e.g., ticket opener)
            overwrites[target].read_messages = False
            overwrites[target].send_messages = False

    # Re-apply updated overwrites
    await ticket_channel.edit(overwrites=overwrites)

    # Send staff controls
    embed = discord.Embed(
        title="Support team ticket controls",
        description="The ticket is now closed. Use the buttons below to manage it.",
        color=discord.Color.dark_gray()
    )
    await ticket_channel.send(embed=embed, view=TicketControlView())


# Define the command to add a user to the ticket
@bot.command()
@commands.check(lambda ctx: ctx.author.guild_permissions.administrator or any(role.id in SUPPORT_ROLES for role in ctx.author.roles))
async def add_usersupp(ctx, user_id: int):
    ticket_channel = ctx.channel  # Get the ticket channel

    # Check if the channel is a valid ticket channel (e.g., starts with "ticket-")
    if not ticket_channel.name.startswith("ticket-"):
        await ctx.send("❌ This is not a valid ticket channel.")
        return

    # Ensure that the user has permission to manage channels (staff/owners)
    if not ctx.author.guild_permissions.manage_channels:
        await ctx.send("❌ You do not have permission to add a user.", ephemeral=True)
        return

    try:
        # Fetch the user by ID and grant them access to the ticket channel
        user = await bot.fetch_user(user_id)
        await ticket_channel.set_permissions(user, read_messages=True, send_messages=True)
        await ticket_channel.send(f"👋 Welcome {user.mention}, you've been added to this ticket.")
    except discord.NotFound:
        await ctx.send("❌ User not found. Please check the ID.")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

# ========================== AUTOMATED SECTION ==========================
# ⚠️ Do not modify this section — it's handled internally by the bot and requires no changes from your side.


class TicketControls(View):
    def __init__(self, member, appeal_ticket, main_ticket, bot):
        super().__init__(timeout=None)
        self.member = member
        self.appeal_ticket = appeal_ticket
        self.main_ticket = main_ticket
        self.bot = bot

    @discord.ui.button(label="✅ Unban User", style=discord.ButtonStyle.green)
    async def unban(self, interaction: discord.Interaction, button: Button):
        
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ You don't have permission to do this.", ephemeral=True)
            return

        guild = interaction.guild
        try:
            await guild.unban(discord.Object(id=self.member.id))
            await self.member.send(f"✅ You have been unbanned from {guild.name}. You can rejoin using this link: {MAINSERVER}")
            await interaction.response.send_message("✅ User has been unbanned.", ephemeral=True)
            appeal_guild = self.bot.get_guild(APPEAL_SERVER_ID)
            member = appeal_guild.get_member(self.member.id)

            try:
                await appeal_guild.kick(member, reason="Appeal Accepted")
            except discord.Forbidden:
                await interaction.response.send_message("❌ I don't have permission to kick this user. Check my role position and permissions.", ephemeral=True)
            except Exception as e:
                await interaction.response.send_message(f"❌ Error kicking user: {e}", ephemeral=True)
                
        except Exception as e:
            await interaction.response.send_message(f"❌ Error unbanning: {e}", ephemeral=True)
        for member in self.main_ticket.members:
            if not member.guild_permissions.administrator:
                await self.main_ticket.set_permissions(member, overwrite=discord.PermissionOverwrite(read_messages=False, send_messages=False))
                
        
        await interaction.followup.send("✅ Ticket closed in appeal server. Only admins can see it in the main server.", ephemeral=True)

        await self.main_ticket.send(view=CloseTicketOptions(self.main_ticket))


    @discord.ui.button(label="➕ Add User", style=discord.ButtonStyle.blurple)
    async def add_user(self, interaction: discord.Interaction, button: Button):
        """ Opens a modal form to add a user to the ticket in the Main Server. """
        class AddUserModal(Modal, title="Add User to Ticket"):
            def __init__(self, main_ticket):
                super().__init__()
                self.main_ticket = main_ticket
                self.user_id = TextInput(label="Enter User ID", placeholder="123456789012345678", required=True)
                self.add_item(self.user_id)

            async def on_submit(self, modal_interaction: discord.Interaction):
                user_id = self.user_id.value.strip()
                try:
                    user = modal_interaction.guild.get_member(int(user_id))
                    if user:
                        await self.main_ticket.set_permissions(user, read_messages=True, send_messages=True)
                        await modal_interaction.response.send_message(f"✅ {user.mention} has been added to the ticket!", ephemeral=True)
                    else:
                        await modal_interaction.response.send_message("❌ User not found in this server.", ephemeral=True)
                except Exception as e:
                    await modal_interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

        await interaction.response.send_modal(AddUserModal(self.main_ticket))

    @discord.ui.button(label="❌ Close Ticket", style=discord.ButtonStyle.red)
    async def close_ticket(self, interaction: discord.Interaction, button: Button):
        appeal_server = bot.get_guild(APPEAL_SERVER_ID)
        user_id_str = interaction.channel.name.replace("appeal-", "")
        user = appeal_server.get_member(int(user_id_str)) 
        role = appeal_server.get_role(Appeal_role)  # Role to give in appeal server
        await user.remove_roles(role)

        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ You don't have permission to do this.", ephemeral=True)
            return

        try:
            await self.member.send("❌ Your appeal request has been closed. Feel free to re try after 2 weeks.")
        except discord.Forbidden:
            pass  
        try:
            await self.appeal_ticket.delete()
        except Exception as e:
            await interaction.response.send_message(f"❌ Error deleting appeal ticket: {e}", ephemeral=True)
            return

        try:
            for member in self.main_ticket.members:
                if not member.guild_permissions.administrator:
                    await self.main_ticket.set_permissions(member, overwrite=discord.PermissionOverwrite(read_messages=False, send_messages=False))

            await interaction.response.send_message("✅ Ticket closed in appeal server. Only admins can see it in the main server.", ephemeral=True)

            await self.main_ticket.send(view=CloseTicketOptions(self.main_ticket))

        except Exception as e:
            await interaction.response.send_message(f"❌ Error closing main ticket: {e}", ephemeral=True)
    @discord.ui.button(label="🚫 Ban User", style=discord.ButtonStyle.danger)
    async def ban_user(self, interaction: discord.Interaction, button: Button):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ You don't have permission to do this.", ephemeral=True)
            return

        appeal_guild = self.bot.get_guild(APPEAL_SERVER_ID)
        if not appeal_guild:
            await interaction.response.send_message("❌ Appeal server not found.", ephemeral=True)
            return

        member = appeal_guild.get_member(self.member.id)
        if not member:
            await interaction.response.send_message("❌ User is not in the appeal server.", ephemeral=True)
            return

        try:
            await interaction.response.send_message(f"✅ {member} has been banned from the appeal server.", ephemeral=True)
            await appeal_guild.ban(member, reason="Appeal rejected")
        except discord.Forbidden:
            await interaction.response.send_message("❌ I don't have permission to ban this user. Check my role position and permissions.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error banning user: {e}", ephemeral=True)

        for member in self.main_ticket.members:
            if not member.guild_permissions.administrator:
                await self.main_ticket.set_permissions(member, overwrite=discord.PermissionOverwrite(read_messages=False, send_messages=False))

        await interaction.followup.send("✅ Ticket closed in appeal server. Only admins can see it in the main server.", ephemeral=True)

            # 5️⃣ Send Admin Options (Transcript & Delete Chat)
        await self.main_ticket.send(view=CloseTicketOptions(self.main_ticket))

class CloseTicketOptions(View):
    def __init__(self, main_ticket):
        super().__init__(timeout=None)
        self.main_ticket = main_ticket

    @discord.ui.button(label="📜 Transcript Ticket", style=discord.ButtonStyle.primary)
    async def transcript_ticket(self, interaction: discord.Interaction, button: Button):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ You don't have permission to do this.", ephemeral=True)
            return

        messages = []
        async for msg in self.main_ticket.history(limit=1000):
            messages.append(f"[{msg.created_at}] {msg.author}: {msg.content}")

        transcript_text = "\n".join(reversed(messages))
        transcript_file = discord.File(io.StringIO(transcript_text), filename="transcript.txt")

        log_channel = interaction.guild.get_channel(TRANSCRIPT_CHANNEL_ID)
        if log_channel:
            await log_channel.send("📜 Transcript of closed ticket:", file=transcript_file)

        await interaction.response.send_message("✅ Transcript has been sent to the appeal log.", ephemeral=True)

    @discord.ui.button(label="🗑️ Delete Chat", style=discord.ButtonStyle.danger)
    async def delete_chat(self, interaction: discord.Interaction, button: Button):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ You don't have permission to do this.", ephemeral=True)
            return

        if self.main_ticket:
            await self.main_ticket.delete()
            await interaction.response.send_message("🗑️ Ticket chat has been deleted.", ephemeral=True)



class AppealButton(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="📩 Create Appeal", style=discord.ButtonStyle.green)
    async def create_ticket(self, interaction: discord.Interaction, button: Button):
        appeal_guild = bot.get_guild(APPEAL_SERVER_ID)
        main_guild = bot.get_guild(GUILD_ID)
        
        if not appeal_guild or not main_guild:
            await interaction.response.send_message("❌ Could not fetch servers.", ephemeral=True)
            return
        user = interaction.user
        banned_role = appeal_guild.get_role(Banned_role)  # Banned role

        appeal_role = appeal_guild.get_role(Appeal_role)  # Appeal is open role

        # Check if user already has an open appeal
        if appeal_role in user.roles:
            await interaction.response.send_message("❌ You already have an open appeal. Please wait for a response before opening another one.", ephemeral=True)
            return


        if banned_role not in user.roles:
            await interaction.response.send_message("❌ You do not have the required role to create an appeal.", ephemeral=True)
            return

        
        category = appeal_guild.get_channel(APPEAL_CATEGORY_ID)
        main_category = main_guild.get_channel(MAIN_TICKET_CATEGORY_ID)
        
        overwrites = {
            appeal_guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        }
        main_overwrites = {
            main_guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        }
        
        appeal_ticket = await appeal_guild.create_text_channel(name=f"appeal-{interaction.user.id}", category=category, overwrites=overwrites)
        main_ticket = await main_guild.create_text_channel(name=f"appeal-{interaction.user.id}", category=main_category, overwrites=main_overwrites)
        
        ticket_mappings[interaction.user.id] = (appeal_ticket.id, main_ticket.id)
        
        controls = TicketControls(interaction.user, appeal_ticket, main_ticket, bot)
        await appeal_ticket.send("Please wait for an Admin To Connect, If this ticket stops working please open another ticket or dm any admin")
        await main_ticket.send("Admin, an appeal ticket has been created, The Ban Details Are Below")

        embed = await get_ban_embed(interaction.user)
        if embed:
            await main_ticket.send(embed=embed,view=controls)  # Send the found embed
        else:
            await main_ticket.send(f"No ban record found for {user.mention}.")
        user=interaction.user
        role = appeal_guild.get_role(Appeal_role)  # Role to give in appeal server
        await user.add_roles(role)
        await interaction.response.send_message(f"✅ Appeal tickets created: {appeal_ticket.mention} (Appeal Server), {main_ticket.mention} (Main Server)", ephemeral=True)


@bot.event
async def on_ready():
    await bot.tree.sync() 
    print(f"✅ Synced Slash Commands! Logged in as {bot.user}")
    await send_appeal_message()
    await send_ticket_embed()  # 👈 We just call it here
    for guild in bot.guilds:
        await notify_ticket_channels_on_restart(guild)
    if setup_channel_id:
        setup_channel = bot.get_channel(setup_channel_id)
        if setup_channel:
            async for message in setup_channel.history(limit=100):
                await message.delete()
            embed = discord.Embed(title="Ban Appeal", description="Click the button below to create a ban appeal ticket.", color=discord.Color.red())
            view = AppealButton()
            await setup_channel.send(embed=embed, view=view)
            await setup_channel.send("⚠️ **IF DISCORD BOT IS OFFLINE, PLEASE WAIT OR DM THE ADMIN**")

async def mute_purge(channel, member, mute_time=120, reason="Spamming messages (Auto Moderation)"):
    """Mutes a user and deletes their messages from the last 30 seconds."""
    try:

        duration = discord.utils.utcnow() + timedelta(minutes=mute_time)
        await member.edit(timed_out_until=duration)

        # Notify user via DM
        try:
            await member.send(f":mute: You have been muted in **{member.guild.name}** for {mute_time} minutes.\n**Reason:** {reason}")
        except discord.Forbidden:
            print(f"[WARNING] ⚠️ {member} has DMs closed. Skipping notification.")
            pass  # Ignore if DMs are closed


        await channel.send(f":mute: {member.mention} has been muted for {mute_time} minutes. Reason: {reason}", delete_after=5)

        # Delete messages from the last 30 seconds
        def check(msg):
            return (
                msg.author.id == member.id
                and (discord.utils.utcnow() - msg.created_at).total_seconds() <= 30  # Using discord.utils.utcnow()
            )

        deleted = await channel.purge(limit=100, check=check)

        await channel.send(f":broom: Deleted {len(deleted)} messages from {member.mention} (last 30s).", delete_after=5)

        # Logging the mute action
        log_channel = channel.guild.get_channel(ADMIN_LOG_CHANNEL_ID)
        if log_channel:
            embed = discord.Embed(
                title=":rotating_light: Auto Moderation",
                description=(
                    f"**:bust_in_silhouette: User:** {member.mention}\n"
                    f"**:hourglass_flowing_sand: Duration:** {mute_time} minutes\n"
                    f"**:pushpin: Reason:** {reason}\n"
                    f"**:link: Channel:** {channel.mention}\n"
                    f"**:wastebasket: Messages Deleted:** {len(deleted)}"
                ),
                color=discord.Color.orange()
            )
            embed.set_footer(text=f"Muted by: {channel.guild.me.display_name}")

            await log_channel.send(embed=embed)

    except Exception as e:
        await channel.send(f":x: Error: {e}", delete_after=5)



@bot.event
async def on_member_join(member):
    print(f"{member} joined {member.guild.name}")

    main_server = bot.get_guild(GUILD_ID)  # Main server where bans are checked
    appeal_server = bot.get_guild(member.guild.id)  # Appeal server

    if not main_server or not appeal_server:
        print("Servers not found.")
        return

    try:
        ban_entry = await main_server.fetch_ban(member)        
        role = appeal_server.get_role(Banned_role)  # Role to give in appeal server
        await member.add_roles(role)
    
    except discord.NotFound as e:
        print(f"Error fetching ban: {e}")  
    except discord.Forbidden as e:
        print(f"Bot lacks permission: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    



async def get_ban_embed(user: discord.User):
    main_server = bot.get_guild(GUILD_ID)  # Main server
    if not main_server:
        return None

    channel = main_server.get_channel(ADMIN_LOG_CHANNEL_ID)  # Ban log channel
    if not channel:
        return None

    async for message in channel.history(limit=100, oldest_first=False):  # Search from latest messages
        if message.embeds:
            embed = message.embeds[0]  # Get the first embed
            
            # Check if the embed contains the username or ID
            if user.name in embed.description or str(user.id) in embed.description:
                return embed  # Return the embed instead of sending it

    return None  # Return None if no ban log is found

@bot.event
async def on_member_update(before, after):
    # Check if the user boosted the server (i.e., the premium_since field changed)
    if before.premium_since is None and after.premium_since is not None:
        # Get the correct channel by ID (BOOST_CHANNEL_ID)
        channel = bot.get_channel(BOOST_CHANNEL_ID)
        
        if channel:
            # Mention the user in a spoiler in a separate message
            await channel.send(f"||{after.mention}||")
            
            # Create the embed with the thank-you message
            embed = discord.Embed(
                title="<a:rocket_animated:1296099979961696329> Thanks for Boosting!",
                description=f"<a:celeb:1356564690670456932> {after.mention} just boosted the server! Thanks for your support! <a:scribble:1356564695678455940>\n\nNow we have {after.guild.premium_subscription_count} boosts! <a:celeb:1356564690670456932>",
                color=discord.Color.from_rgb(174, 0, 255)  # Use your specified color
            )
            embed.set_footer(text="You're amazing! <a:scribble:1356564695678455940>")

            # Send the embed to the correct channel
            await channel.send(embed=embed)
        
        # Optionally assign a booster role to the user
        booster_role = after.guild.get_role(BOOSTER_ROLE_ID)
        if booster_role:
            await after.add_roles(booster_role)

async def send_appeal_message():
    guild = bot.guilds[0]  # Assumes the bot is in only one guild; modify as needed
    category = discord.utils.get(guild.categories, id=MAIN_TICKET_CATEGORY_ID)
    
    if not category:
        print("Category not found!")
        return
    
    sent = False
    for channel in category.text_channels:
        if channel.name.startswith("appeal-"):
            await channel.send("**Admins, the bot has restarted. Please use the manual commands for now, buttons won't work.**\n"
                   "**Manual Commands:** `?closeappeal`, `?banappeal`, `?unbanappeal`, `?adduser`")
            sent = True

    if not sent:
        print("No appeal channels found in the category.")
def get_next_level_xp(level):
    """Calculate the XP required to reach the next level."""
    return 5 * (level ** 2) + 50 * level + 100

def update_xp(user_id):
    """Updates user XP, handles level-up, and saves to CSV."""

    file_path = "xp_data.csv"

    # Create CSV if it doesn't exist
    if not os.path.exists(file_path):
        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["UserID", "XP", "Level"])  # Column headers

    # Load current data
    users = {}
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip header
        for row in reader:
            users[row[0]] = {"xp": int(row[1]), "level": int(row[2])}

    # Get current stats
    user = users.get(user_id, {"xp": 0, "level": 1})
    user["xp"] += XP_PER_MESSAGE

    # Check for level-up
    next_xp = get_next_level_xp(user["level"])
    if user["xp"] >= next_xp:
        user["level"] += 1  # Increase level
        user["xp"] = 0  # Reset XP
        next_xp = get_next_level_xp(user["level"])  # Update next XP requirement

    # Save updated data
    users[user_id] = user
    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["UserID", "XP", "Level"])  # Re-write header
        for uid, data in users.items():
            writer.writerow([uid, data["xp"], data["level"]])

    return user["xp"], user["level"], next_xp

def xp_needed(level):
    """Mee6-style XP formula"""
    return 5 * (level ** 2) + 50 * level + 100


def load_xp_data():
    """Load XP data from CSV (or create if missing)."""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["UserID", "XP", "Level"])
    with open(CSV_FILE, "r") as f:
        reader = csv.DictReader(f)
        return {int(row["UserID"]): {"xp": int(row["XP"]), "level": int(row["Level"])} for row in reader}


def save_xp_data(data):
    """Save XP data back to CSV."""
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["UserID", "XP", "Level"])
        for user_id, stats in data.items():
            writer.writerow([user_id, stats["xp"], stats["level"]])



def generate_rank_card(username, avatar_url, level, rank, xp, xp_needed):
    # Image size
    img_width, img_height = 934, 282
    img = Image.new("RGB", (img_width, img_height), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)

    # Load fonts
    font_dir = "fonts"
    font_large = ImageFont.truetype(os.path.join(font_dir, "arial.ttf"), 40)
    font_small = ImageFont.truetype(os.path.join(font_dir, "arial.ttf"), 25)
    font_bold = ImageFont.truetype(os.path.join(font_dir, "arialbd.ttf"), 45)
    font_xp_bold = ImageFont.truetype(os.path.join(font_dir, "arialbd.ttf"), 25)

    # Download and process avatar
    response = requests.get(avatar_url)
    avatar = Image.open(BytesIO(response.content)).resize((120, 120))
    mask = Image.new("L", (120, 120), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, 120, 120), fill=255)

    avatar = avatar.convert("RGBA")
    circular_avatar = Image.new("RGBA", (120, 120), (0, 0, 0, 0))
    circular_avatar.paste(avatar, (0, 0), mask=mask)

    # Paste avatar
    img.paste(circular_avatar, (30, 80), circular_avatar)

    # RANK and LEVEL (properly inside image)
    rank_x, rank_y = 620, 60
    level_x = rank_x + 150

    draw.text((rank_x + 80, rank_y - 5), f"#{rank}", font=font_bold, fill="white")  # Rank number
    draw.text((rank_x + 80, rank_y + 35), "RANK", font=font_small, fill="gray")  # 'RANK' below

    draw.text((level_x + 70, rank_y - 5), f"{level}", font=font_bold, fill="red")  # Level number
    draw.text((level_x + 70, rank_y + 35), "LEVEL", font=font_small, fill="red")  # 'LEVEL' below

    # Username closer to XP bar
    username_x, username_y = 180, 140
    draw.text((username_x, username_y), username, font=font_large, fill="white")

    # XP Bar
    bar_x, bar_y, bar_width, bar_height = 180, 190, 600, 35  # Moved bar up a little
    xp_progress = int((xp / xp_needed) * bar_width)

    # Draw XP bar with rounded edges
    draw.rounded_rectangle((bar_x, bar_y, bar_x + bar_width, bar_y + bar_height), fill="gray", radius=18)
    draw.rounded_rectangle((bar_x, bar_y, bar_x + xp_progress, bar_y + bar_height), fill="red", radius=18)

    # XP Progress inside the bar (rounded edges)
    progress_bar = Image.new("RGBA", (xp_progress, bar_height), (255, 0, 0, 255))
    progress_mask = Image.new("L", (xp_progress, bar_height), 0)
    progress_draw = ImageDraw.Draw(progress_mask)
    progress_draw.rounded_rectangle((0, 0, xp_progress, bar_height), fill=255, radius=18)

    img.paste(progress_bar, (bar_x, bar_y), progress_mask)

    # XP Text (moved slightly higher)
    xp_text_bold = f"{xp}"  # Bold part
    xp_text_normal = f" / {xp_needed} XP"  # Normal part
    xp_bold_width = draw.textbbox((0, 0), xp_text_bold, font=font_xp_bold)[2]  # Get width of bold text

    xp_text_x = bar_x + bar_width - 160  # Adjusted for better positioning
    xp_text_y = bar_y - 30  # **Moved slightly higher above XP bar**

    draw.text((xp_text_x, xp_text_y), xp_text_bold, font=font_xp_bold, fill="white")  # Current XP in bold
    draw.text((xp_text_x + xp_bold_width, xp_text_y), xp_text_normal, font=font_small, fill="gray")  # Total XP normal

    # Save image
    img_path = "rank_card.png"
    img.save(img_path)
    return img_path



class TicketView(discord.ui.View):
    @discord.ui.button(label="🎫 Create Ticket", style=discord.ButtonStyle.green, custom_id="create_ticket")
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        user = interaction.user
        category = discord.utils.get(guild.categories, id=TICKET_CATEGORY_ID)

        # Check if ticket already exists
        existing_channel = discord.utils.get(guild.channels, name=f"ticket-{user.id}")
        if existing_channel:
            await interaction.response.send_message("❗ You already have an open ticket.", ephemeral=True)
            return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True)
        }

        for role_id in SUPPORT_ROLES:
            role = guild.get_role(role_id)
            if role:
                overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

        # Create ticket channel in the specified category with the user ID as part of the name
        ticket_channel = await guild.create_text_channel(
            name=f"ticket-{user.id}",
            overwrites=overwrites,
            category=category,
            reason="Support ticket created"
        )

        await interaction.response.send_message(f"✅ Your ticket has been created: {ticket_channel.mention}", ephemeral=True)

        # Send the Staff View to the ticket channel after creation
        view = TicketStaffView(ticket_channel)


        # Create the embed for the ticket management
        embed = discord.Embed(
            description="Support will be with you shortly.\nAdmins can control the ticket using the buttons below.",
            color=discord.Color.green(),
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text="Support Team • Defender_XD")

        # Send the embed along with the view for buttons
        await ticket_channel.send(f"Welcome! <@{user.id}>",embed=embed, view=view)


class TicketStaffView(discord.ui.View):
    def __init__(self, ticket_channel: discord.TextChannel):
        super().__init__()
        self.ticket_channel = ticket_channel

    @discord.ui.button(label="❌ Close Ticket", style=discord.ButtonStyle.red, custom_id="close_ticket")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.user.guild_permissions.manage_channels:
            await interaction.response.send_message("❌ You do not have permission to close this ticket.", ephemeral=True)
            return

        # Lock the ticket: remove view/send access from everyone except staff and bot
        overwrites = self.ticket_channel.overwrites

        # Revoke permission for individual users (ticket creator, etc.)
        for target in list(overwrites.keys()):
            if isinstance(target, discord.Member) or isinstance(target, discord.User):
                overwrites[target].read_messages = False
                overwrites[target].send_messages = False

        # Keep support roles and bot access
        for role_id in SUPPORT_ROLES:
            role = self.ticket_channel.guild.get_role(role_id)
            if role:
                overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

        # Ensure bot always has access
        overwrites[self.ticket_channel.guild.me] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

        # Apply the updated overwrites
        await self.ticket_channel.edit(overwrites=overwrites)


        # Send staff controls
        embed = discord.Embed(
            title="Support team ticket controls",
            description="The ticket is now closed. Use the buttons below to manage it.",
            color=discord.Color.dark_gray()
        )
        await self.ticket_channel.send(embed=embed, view=TicketControlView())

        await interaction.response.send_message("✅ The ticket has been locked. Only staff can view it now.", ephemeral=True)

    @discord.ui.button(label="➕ Add User", style=discord.ButtonStyle.blurple, custom_id="add_user")
    async def add_user(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.user.guild_permissions.manage_channels:
            await interaction.response.send_message("❌ You do not have permission to add a user.", ephemeral=True)
            return

        # Modal Class (defined inside the method for context)
        class AddUserModal(discord.ui.Modal, title="Add User to Ticket"):
            def __init__(modal_self, ticket_channel):
                super().__init__()
                modal_self.ticket_channel = ticket_channel
                modal_self.user_id = discord.ui.TextInput(
                    label="Enter User ID",
                    placeholder="123456789012345678",
                    required=True
                )
                modal_self.add_item(modal_self.user_id)

            async def on_submit(modal_self, modal_interaction: discord.Interaction):
                user_id = modal_self.user_id.value.strip()
                try:
                    user = await bot.fetch_user(int(user_id))
                    await modal_self.ticket_channel.set_permissions(user, read_messages=True, send_messages=True)
                    await modal_self.ticket_channel.send(f"👋 Welcome {user.mention}, you've been added to this ticket.")
                    await modal_interaction.response.send_message(f"✅ {user.mention} added successfully!")
                except discord.NotFound:
                    await modal_interaction.response.send_message("❌ User not found. Please check the ID.", ephemeral=True)
                except Exception as e:
                    await modal_interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

        # Show modal to the staff member
        await interaction.response.send_modal(AddUserModal(self.ticket_channel))





async def create_transcript(channel: discord.TextChannel) -> str:
    # Use an async generator to collect all messages
    messages = []
    async for msg in channel.history(limit=None, oldest_first=True):
        messages.append(msg)

    filename = f"transcript-{channel.name}.txt"
    filepath = f"./{filename}"

    # Create a text file and write all messages to it
    async with aiofiles.open(filepath, mode='w', encoding='utf-8') as f:
        for msg in messages:
            time = msg.created_at.strftime("%Y-%m-%d %H:%M:%S")
            await f.write(f"{msg.author} [{time}]: {msg.content}\n")

    return filepath, len(messages)


async def send_transcript_log(channel: discord.TextChannel, moderator: discord.Member, ticket_owner: discord.Member):
    # Generate the transcript file and count messages
    transcript_path, msg_count = await create_transcript(channel)
    file = discord.File(transcript_path, filename=os.path.basename(transcript_path))

    # Create the embed to be sent first
    embed = discord.Embed(
        title="🎟️ Ticket Closed",
        color=discord.Color.dark_gray(),
        timestamp=datetime.utcnow()
    )
    embed.set_author(name=moderator.display_name, icon_url=moderator.display_avatar.url)
    embed.add_field(name="Ticket Owner", value=f"{ticket_owner.mention}", inline=True)
    embed.add_field(name="Ticket Name", value=channel.name, inline=True)
    embed.add_field(name="Panel Name", value="Support Tickets", inline=True)
    embed.add_field(name="Direct Transcript", value="Use Button", inline=True)
    embed.add_field(name="Users in transcript", value=f"{msg_count} – {bot.user.mention} - {bot.user}", inline=False)
    embed.set_footer(text=f"Channel ID: {channel.id} | Server: {channel.guild.name}")

    # Send the embed first
    log_channel = bot.get_channel(TRANSCRIPT_LOG_CHANNEL_ID)
    await log_channel.send(embed=embed)

    # Send the .txt file after the embed
    await log_channel.send(file=file)

    # Optional cleanup of the .txt file after sending it
    os.remove(transcript_path)




class TicketControlView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # Disable timeout so it stays

    @discord.ui.button(label="Transcript", style=discord.ButtonStyle.gray, emoji="📄", custom_id="transcript_btn")
    async def transcript(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Get the current channel (the ticket channel)
        channel = interaction.channel

        # Ensure the channel name follows the 'ticket-<user_id>' format
        if channel.name.startswith("ticket-"):
            # Extract the user ID from the channel name
            user_id_str = channel.name.split('-')[1]  # e.g., "ticket-123456789012345678"
            try:
                ticket_owner_id = int(user_id_str)
            except ValueError:
                await interaction.response.send_message("Invalid ticket owner ID format.", ephemeral=True)
                return
            
            # Try to get the ticket owner (user) from the cache
            ticket_owner = channel.guild.get_member(ticket_owner_id)

            if not ticket_owner:
                # If the member isn't cached, attempt to fetch them
                try:
                    ticket_owner = await channel.guild.fetch_member(ticket_owner_id)
                except discord.NotFound:
                    await interaction.response.send_message("Ticket owner not found.", ephemeral=True)
                    return

            moderator = interaction.user  # The user interacting with the button

            # Send transcript log to the desired channel (e.g., ticket log channel)
            await send_transcript_log(channel, moderator, ticket_owner)

            # Send a response to the user
            await interaction.response.send_message("Transcript has been sent to the log channel!", ephemeral=True)


    @discord.ui.button(label="Open", style=discord.ButtonStyle.blurple, emoji="🔓", custom_id="open_btn")
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        ticket_channel = interaction.channel  # Get the ticket channel
        
        # Check if the ticket channel exists and follows naming convention (if necessary)
        if ticket_channel.name.startswith("ticket-"):  # Adjust this as per your ticket channel naming convention
            # Get the ticket owner from the channel name (assuming it's based on the user ID)
            ticket_owner = None
            user_id_str = ticket_channel.name.split('-')[1]  # Assuming the name format is ticket-<user_id>
            try:
                ticket_owner = await ticket_channel.guild.fetch_member(int(user_id_str))
            except discord.NotFound:
                ticket_owner = None
            
            # Prepare permission overwrites for the channel (open it)
            overwrites = {
                ticket_channel.guild.default_role: discord.PermissionOverwrite(read_messages=False),  # Default role cannot read
                ticket_owner: discord.PermissionOverwrite(read_messages=True),  # Allow the ticket owner to see the ticket
            }



            # Update the channel permissions
            await ticket_channel.edit(overwrites=overwrites)

            # Send confirmation message
            await interaction.response.send_message(f"The ticket `{ticket_channel.name}` has been opened!", ephemeral=True)


            await ticket_channel.send(f"Your ticket has been opened. You can now interact with it. {ticket_owner.mention}")            
            # Remove both the embed and the buttons from the message by editing it with a plain message
            await interaction.message.edit(content="The ticket is now open and accessible.", embed=None, view=None)

        else:
            # If it's not a valid ticket channel
            await interaction.response.send_message("This is not a valid ticket channel to open.", ephemeral=True)


    @discord.ui.button(label="Delete", style=discord.ButtonStyle.red, emoji="⛔", custom_id="delete_btn")
    async def delete_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Get the channel where the ticket exists (interaction.channel)
        ticket_channel = interaction.channel
        
        # Check if the channel is indeed a ticket channel (you could use naming convention or some other way to check)
        if ticket_channel.name.startswith("ticket-"):  # Adjust this condition as needed
            # Send a message with Yes/No buttons for confirmation
            confirm_view = discord.ui.View()

            # Yes button for confirming deletion
            yes_button = discord.ui.Button(label="Yes", style=discord.ButtonStyle.green, custom_id="confirm_delete")
            # No button for canceling deletion
            no_button = discord.ui.Button(label="No", style=discord.ButtonStyle.red, custom_id="cancel_delete")

            confirm_view.add_item(yes_button)
            confirm_view.add_item(no_button)

            # Send the confirmation message with buttons
            await interaction.response.send_message(
                f"Are you sure you want to delete the ticket `{ticket_channel.name}`? This action cannot be undone.",
                view=confirm_view,
                ephemeral=True
            )

            # Define the callback for the 'Yes' button
            async def confirm_delete(interaction: discord.Interaction):
                await ticket_channel.delete()
                await interaction.response.send_message(f"The ticket `{ticket_channel.name}` has been deleted.", ephemeral=True)
            
            # Define the callback for the 'No' button
            async def cancel_delete(interaction: discord.Interaction):
                await interaction.response.send_message("Ticket deletion canceled.", ephemeral=True)

            # Attach the callbacks to the buttons
            yes_button.callback = confirm_delete
            no_button.callback = cancel_delete

        else:
            # If it's not a ticket channel, just notify the user
            await interaction.response.send_message("This is not a valid ticket channel for deletion.", ephemeral=True)



async def notify_ticket_channels_on_restart(guild: discord.Guild):
    # Get the ticket category
    category = discord.utils.get(guild.categories, id=TICKET_CATEGORY_ID)
    if not category:
        print("Ticket category not found.")
        return

    # Loop through channels in this category
    for channel in category.text_channels:
        if channel.name.startswith("ticket-"):
            try:
                # Create the embed message
                embed = discord.Embed(
                    title="🔁 Bot Restart Detected",
                    description=(
                        "Sorry admins! The bot has been restarted.\n\n"
                        "**Please use the manual commands below to manage this ticket:**\n"
                        "🔸 `?close_ticketsupp`\n"
                        "🔸 `?add_usersupp`"
                    ),
                    color=discord.Color.orange()
                )
                embed.set_footer(text="Support Team • Defender_XD")

                # Send the message
                await channel.send(embed=embed)

            except Exception as e:
                print(f"Failed to notify {channel.name}: {e}")




async def send_ticket_embed():
    channel = bot.get_channel(TICKET_CHANNEL_ID)
    guild = bot.get_guild(1286631860197392396)  # Replace with your actual server ID

    if channel and guild:
        await channel.purge(limit=100)  # Clear previous embeds/messages

        embed = discord.Embed(
            title="📩 Need Support?",
            description=(
                "**If you're experiencing issues or have questions, click the button below to open a private support ticket.**\n\n"
                "Our team will assist you shortly. Please be respectful and provide as much detail as possible. 🤝\n\n"
            ),
            color=discord.Color.teal()
        )
        embed.set_footer(text="Support Team • Defender_XD")
        embed.set_thumbnail(url=guild.icon.url if guild.icon else discord.Embed.Empty)

        await channel.send(embed=embed, view=TicketView())
    else:
        print("❌ Could not find the ticket channel or guild.")





# ========================== MODERATOR SECTION ==========================
# 🛡️ Commands and settings available to server moderators


@bot.command()
@commands.check(lambda ctx: ctx.author.guild_permissions.administrator or any(role.id in MODERATOR_ROLES for role in ctx.author.roles))
async def ban(ctx, member: discord.Member, *, reason_with_proof="No reason provided"):
    # Split reason and optional proof message ID
    parts = reason_with_proof.split('|', 1)
    reason = parts[0].strip()
    proof_message_id = parts[1].strip() if len(parts) > 1 else None


    # Attempt to DM the banned user
    try:
        await member.send(f"❌ You have been permanently banned from {ctx.guild.name} for: {reason}\nYou can appeal here: {APPEAL_SERVER_INVITE}")
    except:
        pass

    # Fetch the log channel
    log_channel = bot.get_channel(ADMIN_LOG_CHANNEL_ID)
    if log_channel:
        proof_message_content = "*No proof message provided*"

        # Fetch proof message if an ID was provided
        if proof_message_id:
            try:
                proof_message = await ctx.channel.fetch_message(int(proof_message_id))
                proof_message_content = proof_message.content if proof_message.content else "*[Message had no text content]*"
            except discord.NotFound:
                proof_message_content = "*[Message not found]*"
            except discord.Forbidden:
                proof_message_content = "*[Missing permissions to fetch message]*"
            except discord.HTTPException:
                proof_message_content = "*[Failed to retrieve message]*"

        # Create embed with proof
        embed = discord.Embed(
            title="🚨 User Banned",
            description=(
                f"**👤 User:** {member.mention}\n\n"
                f"**📄 Reason:** {reason}\n\n"
                f"**🛠️ Moderator:** {ctx.author.mention}\n\n"
                f"**🧾 Proof (User Message):**\n{proof_message_content}"
            ),
            color=discord.Color.red()
        )

        await log_channel.send(embed=embed)
        # Ban the user
    await member.ban(reason=reason)
    await ctx.send(f"✅ {member.mention} has been permanently banned for: {reason}",delete_after=5)
    await ctx.message.delete()



@bot.command()
@commands.check(lambda ctx: ctx.author.guild_permissions.administrator or any(role.id in MODERATOR_ROLES for role in ctx.author.roles))
async def unban(ctx, user_id: int):
    guild = ctx.guild

    try:
        user = await bot.fetch_user(user_id)  # Fetch user object
        await guild.unban(user)
        await ctx.send(f"✅ {user.mention} has been unbanned.",delete_after=3)
        await ctx.message.delete()
        
        # Log the unban action
        log_channel = bot.get_channel(ADMIN_LOG_CHANNEL_ID)
        if log_channel:
            embed = discord.Embed(
                title="🚨 User Unbanned",
                description=f"**👤 User:** {user.mention} (`{user.id}`)\n\n**🛠️ Unbanned by:** {ctx.author.mention}",
                color=discord.Color.green()
            )
            await log_channel.send(embed=embed)

    except discord.NotFound:
        await ctx.send("⚠️ No banned user found with that ID.")
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to unban users.")
    except Exception as e:
        await ctx.send(f"⚠️ Unexpected error: `{e}`")


@bot.command()
@commands.check(lambda ctx: ctx.author.guild_permissions.administrator or any(role.id in MODERATOR_ROLES for role in ctx.author.roles))
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    # Notify the user via DM
    try:
        await member.send(f"⚠️ You have been kicked from {ctx.guild.name} by {ctx.author.mention} for: {reason}")
    except:
        pass  # Ignore if DMs are closed

    # Kick the user
    await member.kick(reason=reason)
    await ctx.send(f"✅ {member.mention} has been kicked by {ctx.author.mention} for: {reason}",delete_after=5)

    # Log the action in the admin log channel
    log_channel = bot.get_channel(ADMIN_LOG_CHANNEL_ID)
    if log_channel:
        embed = discord.Embed(
            title="🚨 User Kicked",
            description=f"**👤 User:** {member.mention} (`{member.id}`)\n\n"
                        f"**📄 Reason:** {reason}\n\n"
                        f"**🛠️ Kicked by:** {ctx.author.mention} (`{ctx.author.id}`)",
            color=discord.Color.orange()
        )
        await log_channel.send(embed=embed)

    # Delete the command message
    await ctx.message.delete()


@bot.command()
@commands.check(lambda ctx: ctx.author.guild_permissions.administrator or any(role.id in MODERATOR_ROLES for role in ctx.author.roles))
async def lock(ctx, *, reason="Channel Locked"):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send(f"**🔒 {reason.upper()} 🔒**")
    await ctx.message.delete()

@bot.command()
@commands.check(lambda ctx: ctx.author.guild_permissions.administrator or any(role.id in MODERATOR_ROLES for role in ctx.author.roles))
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)

    async for message in ctx.channel.history(limit=50):  # Checks the last 50 messages
        if message.author == bot.user and "🔒" in message.content:
            await message.delete()
            break  

    await ctx.message.delete()  # Deletes the unlock command message



@bot.command()
@commands.check(lambda ctx: ctx.author.guild_permissions.administrator or any(role.id in MODERATOR_ROLES for role in ctx.author.roles))
async def mute(ctx, member: discord.Member, time: int, *, reason="No reason provided"):
    try:
        duration = discord.utils.utcnow() + timedelta(minutes=time)
        await member.edit(timed_out_until=duration)

        # Send DM to the user
        try:
            await member.send(f"🔇 You have been muted in **{ctx.guild.name}** for {time} minutes.\n**Reason:** {reason}")
        except discord.Forbidden:
            pass  # Ignore if DMs are closed

        await ctx.send(f"🔇 {member.mention} has been muted for {time} minutes. Reason: {reason}")

        # Delete the command message
        try:
            await ctx.message.delete()
        except discord.NotFound:
            pass  

        # Log mute
        log_channel = ctx.guild.get_channel(ADMIN_LOG_CHANNEL_ID)
        if log_channel:
            embed = discord.Embed(
                title="🔇 User Muted",
                description=(
                    f"**👤 User:** {member.mention} (`{member.id}`)\n"
                    f"**📄 Reason:** {reason}\n"
                    f"**⏳ Duration:** {time} minutes\n"
                    f"**🛠️ Muted by:** {ctx.author.mention}"
                ),
                color=discord.Color.red(),
            )
            await log_channel.send(embed=embed)

    except Exception as e:
        await ctx.send(f"❌ Error: {e}", ephemeral=True)  # Error message only visible to the user



@bot.command()
@commands.check(lambda ctx: ctx.author.guild_permissions.administrator or any(role.id in MODERATOR_ROLES for role in ctx.author.roles))
async def unmute(ctx, member: discord.Member):
    try:
        await member.edit(timed_out_until=None)  # Remove timeout

        # Send DM to the user
        try:
            await member.send(f"🔊 You have been unmuted in **{ctx.guild.name}**.")
        except discord.Forbidden:
            pass  # Ignore if DMs are closed

        await ctx.send(f"✅ {member.mention} has been unmuted.",delete_after=3)

        # Delete the command message
        try:
            await ctx.message.delete()
        except discord.NotFound:
            pass  

        # Log unmute
        log_channel = ctx.guild.get_channel(ADMIN_LOG_CHANNEL_ID)
        if log_channel:
            embed = discord.Embed(
                title="🔊 User Unmuted",
                description=f"**👤 User:** {member.mention} (`{member.id}`)\n**🛠️ Unmuted by:** {ctx.author.mention}",
                color=discord.Color.green(),
            )
            await log_channel.send(embed=embed)

    except Exception as e:
        await ctx.send(f"❌ Error: {e}", ephemeral=True)  # Error message only visible to the user

def load_warnings():
    try:
        with open(WARN_FILE, "r") as file:
            reader = csv.reader(file)
            return {rows[0]: int(rows[1]) for rows in reader}
    except FileNotFoundError:
        return {}

def save_warning(user_id, count):
    warnings = load_warnings()
    warnings[user_id] = count
    with open(WARN_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        for uid, warns in warnings.items():
            writer.writerow([uid, warns])

def remove_warning(user_id):
    warnings = load_warnings()
    if user_id in warnings:
        del warnings[user_id]
    with open(WARN_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        for uid, warns in warnings.items():
            writer.writerow([uid, warns])

        

async def log_warning(ctx, user, reason, warns):
    log_channel = bot.get_channel(ADMIN_LOG_CHANNEL_ID)
    punishment = "None"

    if warns == 2:
        punishment = "Muted for 2 hours"
        mute_until = discord.utils.utcnow() + datetime.timedelta(hours=2)
        await user.edit(timed_out_until=mute_until)

    elif warns == 3:
        punishment = "Muted for 24 hours, Don’t do it again or you will be BANNED!"
        mute_until = discord.utils.utcnow() + datetime.timedelta(hours=24)
        await user.edit(timed_out_until=mute_until)

    elif warns >= 4:
        punishment = "Banned"
        try:
            await user.send(f"❌ You have been permanently banned from {ctx.guild.name} for: {reason}\nYou can appeal here: {APPEAL_SERVER_INVITE}")
        except:
            pass
        await user.ban(reason="Reached 4 warnings")

    # 🔹 Set the moderator to "Auto Moderation" if the warning is automatic
    moderator = "Auto Moderation" if isinstance(ctx, discord.Message) else ctx.author.mention

    embed = discord.Embed(
        title="⚠️ User Warned",
        description=(
            f"**User:** {user.mention}\n"
            f"**Reason:** {reason}\n"
            f"**Total Warnings:** {warns}\n"
            f"**Punishment:** {punishment}\n"
            f"**Moderator:** {moderator}\n"
        ),
        color=discord.Color.orange()
    )

    if log_channel:
        await log_channel.send(embed=embed)

    try:
        next_punishment = "No action"
        if warns == 1:
            next_punishment = "Mute for 2 hours (on 2nd warn)"
        elif warns == 2:
            next_punishment = "Mute for 24 hours (on 3rd warn)"
        elif warns == 3:
            next_punishment = "Permanent Ban (on 4th warn)"

        await user.send(
            f"\n**BEAWARE ABOUT YOUR WARNING**\n"
            f"Total Warnings: {warns}\n"
            f"Next Action: {next_punishment}"
        )
    except:
        pass



@bot.command()
@commands.check(lambda ctx: ctx.author.guild_permissions.administrator or any(role.id in MODERATOR_ROLES for role in ctx.author.roles))
async def warn(ctx, user: discord.Member, *, reason="No reason provided"):
    warns = load_warnings()
    user_id = str(user.id)
    warns[user_id] = warns.get(user_id, 0) + 1
    save_warning(user_id, warns[user_id])

    warning_count = warns[user_id]

    punishment = None
    if warning_count == 2:
        duration = discord.utils.utcnow() + timedelta(hours=2)
        await user.edit(timed_out_until=duration)
        punishment = "Muted for 2 hours"
    elif warning_count == 3:
        duration = discord.utils.utcnow() + timedelta(hours=24)
        await user.edit(timed_out_until=duration)
        punishment = "Muted for 24 hours"
    elif warning_count >= 4:
        await user.send(f"❌ You have been permanently banned from {ctx.guild.name} for: excessive warnings \nYou can appeal here: {APPEAL_SERVER_INVITE}")
        await user.ban(reason=f"Excessive warnings ({warning_count} warnings). Reason: {reason}")
        punishment = "Banned from the server"

    try:
        await user.send(f"⚠️ You have been warned in **{ctx.guild.name}**.\n**Reason:** {reason}\n**Total Warnings:** {warning_count}\n**🚨 Punishment:** {punishment if punishment else 'None'}")
    except discord.Forbidden:
        pass  

    try:
        await ctx.send(f"⚠️ {user.mention} has been warned. Reason: {reason}\nTotal Warnings: {warning_count}\nPunishment: {punishment if punishment else 'None'}",delete_after=3)
    except:
        print("")
    await log_warning(ctx, user, reason, warning_count)

    try:
        await ctx.message.delete()
    except discord.NotFound:
        pass
    
@bot.command()
@commands.check(lambda ctx: ctx.author.guild_permissions.administrator or any(role.id in MODERATOR_ROLES for role in ctx.author.roles))
async def warns(ctx, user: discord.Member):
    warns = load_warnings()
    user_id = str(user.id)
    count = warns.get(user_id, 0)
    await ctx.send(f"{user.mention} has {count} warnings.",delete_after=3)
    await ctx.message.delete()


@bot.command()
@commands.check(lambda ctx: ctx.author.guild_permissions.administrator or any(role.id in MODERATOR_ROLES for role in ctx.author.roles))
async def clearwarn(ctx, user: discord.Member):
    remove_warning(str(user.id))
    await ctx.send(f"Cleared warnings for {user.mention}",delete_after=3)
    log_channel = bot.get_channel(ADMIN_LOG_CHANNEL_ID)
    embed = discord.Embed(
        title="⚠️ User Warnning Cleared",
        description=(
            f"**User:** {user.mention}\n"
            f"**Moderator:** {ctx.author.mention}"
        ),
        color=discord.Color.orange()
    )
    await log_channel.send(embed=embed)

    await ctx.message.delete()

@bot.command()
@commands.check(lambda ctx: ctx.author.guild_permissions.administrator or any(role.id in MODERATOR_ROLES for role in ctx.author.roles))
async def insta_noti(ctx, link: str):
    """Command to send an Instagram notification (Only for Moderators)"""
    
    # Validate the Instagram link
    if not link.startswith("https://www.instagram.com/"):
        await ctx.send("❌ Please provide a valid Instagram link.")
        return

    # Send the notification in the designated channel
    channel = bot.get_channel(INSTA_NOTI_CHANNEL_ID)
    if channel:
        await channel.send(f"  @everyone \n <a:Announce:1296099996902494259>  **New Instagram Post!** \n  Check it out here: {link}")

        
    log_channel = bot.get_channel(ADMIN_LOG_CHANNEL_ID)
    embed = discord.Embed(
        title="Instagram Notification command used ",
        description=(
            f"**Link:**{link}\n"
            f"**Moderator:** {ctx.author.mention}"
        ),
        color=discord.Color.orange()
    )
    await log_channel.send(embed=embed)




@bot.command(name='helpmod')
@commands.check(lambda ctx: ctx.author.guild_permissions.administrator or any(role.id in MODERATOR_ROLES for role in ctx.author.roles))
async def custom_help(ctx):
    embed = discord.Embed(
        title="Help - Available Commands",
        description="Here are the commands you can use:",
        color=discord.Color.from_rgb(255, 255, 255)
    )
    
    embed.add_field(
        name="?ban <@user> reason | proof ",
        value="Ban a user from the server.",
        inline=False
    )
    embed.add_field(
        name="?unban <@user>  ",
        value="UnBan a user from the server.",
        inline=False
    )
    embed.add_field(
        name="?kick <@user> reason ",
        value="Kicks a user from the server .",
        inline=False
    )
    embed.add_field(
        name="?mute <@user> time reason (time is in minutes)",
        value="Mutes a user  .",
        inline=False
    )
    embed.add_field(
        name="?unmute <@user> ",
        value="Unmutes a User  .",
        inline=False
    )
    embed.add_field(
        name="?warn <@user> reason ",
        value="Warns a user  .",
        inline=False
    )
    embed.add_field(
        name="?warns <@user> ",
        value="See how many warns he has   .",
        inline=False
    )
    embed.add_field(
        name="?clearwarn <@user> ",
        value="Clears his warn  .",
        inline=False
    )
    embed.add_field(
        name="?insta_noti <link> ",
        value=f"Sends Instagram Notification **https://discord.com/channels/1286631860197392396/1287082090587754588**  .",
        inline=False
    )

    
    embed.timestamp = ctx.message.created_at
    await ctx.send(embed=embed)
    await ctx.message.delete()

# ========================== MEMBER SECTION ==========================
# 👥 Commands accessible to all regular server members

@bot.tree.command(name="rank")
async def rank(interaction: discord.Interaction, member: discord.Member = None):
    """Shows user's XP, level, and rank as an image."""
    if member is None:
        member = interaction.user  # Default to the command user

    xp_data = load_xp_data()
    
    # Sort users by XP (highest to lowest) to determine rank
    sorted_users = sorted(xp_data.items(), key=lambda x: x[1]["xp"], reverse=True)
    rank = next((i + 1 for i, (user_id, stats) in enumerate(sorted_users) if user_id == member.id), None)

    user_stats = xp_data.get(member.id, {"xp": 0, "level": 0})
    xp = user_stats["xp"]
    level = user_stats["level"]
    next_xp = xp_needed(level + 1)

    # Generate rank card with global rank
    img_path = generate_rank_card(member.name, member.display_avatar.url, level, rank, xp, next_xp)


    # Send image in response to interaction
    await interaction.response.send_message(file=discord.File(img_path))

@bot.tree.command(name="lb")
async def leaderboard(interaction: discord.Interaction):
    """Shows the top 10 users with the highest XP."""
    xp_data = load_xp_data()

    # Sort users by XP (highest first)
    sorted_users = sorted(xp_data.items(), key=lambda x: x[1]["xp"], reverse=True)

    # Create an embed for the leaderboard
    embed = discord.Embed(title="🏆 Leaderboard", color=discord.Color.gold())
    embed.set_footer(text="Top 10 XP Holders")

    # Add up to 10 users to the embed
    for rank, (user_id, stats) in enumerate(sorted_users[:10], start=1):
        member = interaction.guild.get_member(user_id)  # Get the user object
        name = member.name if member else f"User ID {user_id}"  # Handle missing users
        embed.add_field(name=f"#{rank} {name}", value=f"Level {stats['level']} ", inline=False)

    # Send leaderboard as a response
    await interaction.response.send_message(embed=embed)

    
# ========================== BOT CORE ==========================
# ❤️ The heart of the Discord bot — do not touch this section!

@bot.event
async def on_message(message):
    if message.author.bot:
        return
        # Ignore XP gain for users with the specified role
    if NO_XP_ROLE_ID in [role.id for role in message.author.roles]:
        return await bot.process_commands(message)  # Still allow commands

    xp_data = load_xp_data()
    user_id = message.author.id

    # Get user stats or initialize
    user_stats = xp_data.get(user_id, {"xp": 0, "level": 1})

    # Add a fixed XP amount per message
    user_stats["xp"] += XP_PER_MESSAGE  # Example: XP_PER_MESSAGE = 15

    # Check if user leveled up
    next_xp = xp_needed(user_stats["level"])
    if user_stats["xp"] >= next_xp:
        user_stats["level"] += 1
        user_stats["xp"] = 0  # Reset XP
        botchannel = message.guild.get_channel(BOT_COMMAND_ID)
        await botchannel.send(f"🎉 {message.author.mention} leveled up to **Level {user_stats['level']}!**")

    # Save updated XP and level
    xp_data[user_id] = user_stats
    save_xp_data(xp_data)

    #1) Relay system
    for user_id, (appeal_ticket_id, main_ticket_id) in ticket_mappings.items():
        if message.channel.id == appeal_ticket_id:
            main_ticket = bot.get_channel(main_ticket_id)
            if main_ticket:
                await main_ticket.send(f" ({message.author.mention}): {message.content}")
        elif message.channel.id == main_ticket_id:
            appeal_ticket = bot.get_channel(appeal_ticket_id)
            if appeal_ticket:
                await appeal_ticket.send(f"Admin : {message.content}")
    user_roles = {role.id for role in message.author.roles}

    # Ignore users with specific roles
    user_roles = {role.id for role in message.author.roles}

    # Ignore users with specific roles
    if user_roles & IGNORED_ROLES:
        await bot.process_commands(message)
        return

    #2 Detect links using regex
    if re.search(LINK_REGEX, message.content, re.IGNORECASE):

        if message.channel.id in BLOCKED_LINK_CHANNELS:
            print("❌ Link posted in a restricted channel. Deleting...")

            await message.delete()
            await message.channel.send(f"{message.author.mention}, links are not allowed in this channel!", delete_after=3)

            # Call warn function without using ctx
            print(f"⚠️ Warning user: {message.author}")
            await warn(message, message.author, reason="Posting links in a restricted channel")

    #3 Detect bad words using regex
    if any(word in message.content.lower() for word in BAD_WORDS) or BAD_WORDS_REGEX.search(message.content):
        print("🚨 Bad word detected! Deleting message...")
        await message.delete()
        await message.channel.send(f"{message.author.mention}, watch your language!", delete_after=3)

        # Call warn function
        print(f"⚠️ Warning user: {message.author} for bad language")
        await warn(message, message.author, reason="Using inappropriate language")
        return

    # 5️⃣ Spam Protection System
    user_id = message.author.id
    current_time = time.time()

    if user_id not in user_message_timestamps:
        user_message_timestamps[user_id] = []
        user_messages[user_id] = []  # Store user messages for tracking

    user_message_timestamps[user_id].append(current_time)
    user_messages[user_id].append(message)

    user_message_timestamps[user_id] = [t for t in user_message_timestamps[user_id] if current_time - t < SPAM_TIMEFRAME]
    user_messages[user_id] = [msg for msg in user_messages[user_id] if current_time - msg.created_at.timestamp() < SPAM_TIMEFRAME]

    warning_cooldown = 10  
    last_warning_time = spam_warnings.get(user_id, 0)

    # 6️⃣ Detect too many messages in a short time
    if len(user_message_timestamps[user_id]) > SPAM_MESSAGE_LIMIT:
        if current_time - last_warning_time > warning_cooldown:
            spam_warnings[user_id] = current_time  # Update last warning time
            
            # Call mute_purge() instead of deleting messages here
            print(f"[DEBUG] 🚨 Spam detected for {message.author}! Calling mute_purge()...")  # Debugging log
            await mute_purge(message.channel, message.author, mute_time=120, reason="Spamming messages (Auto)")
        
        return         
        return  
    # 7️⃣ Detect repeated messages (e.g., "hello" multiple times)
    last_messages = [msg.content for msg in user_messages[user_id][-3:]]
    if len(last_messages) >= 3 and all(msg == message.content for msg in last_messages):
        if current_time - last_warning_time > warning_cooldown:
            spam_warnings[user_id] = current_time  
            for msg in user_messages[user_id]:
                if msg.content == message.content:
                    try:
                        await msg.delete()
                    except discord.NotFound:
                        pass  

            await message.channel.send(f"{message.author.mention}, stop repeating the same message!", delete_after=3)
            await mute_purge(message.channel, message.author, mute_time=120, reason="Spamming messages (Auto)")
        
        return  

    await bot.process_commands(message)


bot.run(TOKEN)

