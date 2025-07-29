import discord
from discord.ext import commands
import random
from discord import app_commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

bad_words = ["fuck", "shit", "bitch", "ass"]
harm = ["loser",":L","pathetic", "idiot", "stupid"]
weird = ["heck","hell"]
afk = ["AFK","afk"]

bad_word_responses = [
    "{name}, did you say that fucking swear word? shut up!",
    "Hey {name}, that's a spicy word! Wash your mouth with soap!",
    "Yikes, {name}! Swearing detected! 🚨"
    "Woah {name} Watch your tone lil kid,I'll kick your ass out if you kept yapping!"
]

harm_responses = [
    "{name}, who did you call a {word}? Pathetic.",
    "Not cool, {name}! Calling someone '{word}'? you suck",
    "Oof, {name}, that's harsh! But you too!",
    "Hey {name}, words can hurt! '{word}' isn't very nice. But I FUCKING LOVE THE WORD!"
]

weird_responses = [
    "{name}, what the {word} did you just say?",
    "Umm, {name}? Did you just say '{word}'? That's weird.",
    "Heckin' strange, {name}! Mind your words.",
    "Well, {name}, that's a heck of a thing to say!"
]
afk_Res = [
    "what u only knew is 'afk'"
]

COLOR_ROLES = {
    "green": discord.Color.green(),
    "blue": discord.Color.blue(),
    "purple": discord.Color.purple(),
    "red": discord.Color.red(),
    "pink": discord.Color.magenta()
}


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    msg_content = message.content.lower()

    if msg_content == "dude":
        for _ in range(10):
            await message.channel.send("nah i'm not ur dude idiot")
        await bot.process_commands(message)
        return
    elif "anyone know" in msg_content:
        await message.channel.send("no idk")
    elif "gf" in msg_content:
        await message.channel.send("gf? how cute?")

    if any(bad_word in msg_content for bad_word in bad_words):
        response = random.choice(bad_word_responses).format(name=message.author.display_name)
        await message.channel.send(response)
    elif any(h in msg_content for h in harm):
        matched = next((h for h in harm if h in msg_content), "someone")
        response = random.choice(harm_responses).format(name=message.author.display_name, word=matched)
        await message.channel.send(response)
    elif any(w in msg_content for w in weird):
        matched = next((w for w in weird if w in msg_content), "that")
        response = random.choice(weird_responses).format(name=message.author.display_name, word=matched)
        await message.channel.send(response)
    elif any(w in msg_content for w in afk):
        matched = next((w for w in afk if w in msg_content), "that")
        response = random.choice(afk_Res).format(name=message.author.display_name, word=matched)
        await message.channel.send(response)

    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="welcome")
    if channel and channel.permissions_for(member.guild.me).send_messages:
        await channel.send(f"Yo What's up {member.display_name}, you can use /namecolor to change your role color! But remember only once,or when you are '@everyone' role (only if I'm online,also I'm not 24/7 online.)")
        await channel.send("uh,also,there's only Green/Blue/Purple/Red/Pink")
@bot.tree.command(name="namecolor", description="Change your name color! (green/blue/purple/red/pink)")
@app_commands.describe(color="The color you want: green, blue, purple, red, or pink")
async def namecolor(interaction: discord.Interaction, color: str):
    await interaction.response.defer(ephemeral=True)


# /say command: bot says 'userdisplayname: message'
@bot.tree.command(name="say", description="Make the bot say something as you!")
@app_commands.describe(message="The message you want the bot to say.")
async def say(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(f"{interaction.user.display_name}: {message}")

    color = color.lower()
    if color not in COLOR_ROLES:
        await interaction.followup.send(
            "Invalid color! Choose from: green, blue, purple, red, pink.", ephemeral=True
        )
        return

    guild = interaction.guild
    member = interaction.user

    for role in member.roles:
        if role.name.startswith("Color: "):
            await member.remove_roles(role)

    role_name = f"Color: {color.capitalize()}"
    role = discord.utils.get(guild.roles, name=role_name)
    if not role:
        role = await guild.create_role(
            name=role_name,
            color=COLOR_ROLES[color],
            reason="Color role for /namecolor command"
        )
        await role.edit(position=guild.me.top_role.position - 1)

    await member.add_roles(role)
    await interaction.followup.send(
        f"Your name color has been changed to {color}!", ephemeral=True
    )
@app_commands.describe(color="The color you want: green, blue, purple, red, pink, or normal to reset")
async def adminnamecolor(interaction: discord.Interaction, color: str):
    await interaction.response.defer(ephemeral=True)

    color = color.lower()

    member = interaction.user
    guild = interaction.guild

    admin_role = discord.utils.get(guild.roles, name="Admin")

    # Check if user has Admin or an AdminColor role
    has_admin = False
    if admin_role and admin_role in member.roles:
        has_admin = True
    else:
        for role in member.roles:
            if role.name.startswith("AdminColor: "):
                has_admin = True
                break

    if not has_admin:
        await interaction.followup.send(
            "You must have the Admin role or a colored admin role to use this command.", ephemeral=True
        )
        return

    # Remove all AdminColor roles
    roles_to_remove = [role for role in member.roles if role.name.startswith("AdminColor: ")]
    await member.remove_roles(*roles_to_remove, reason="Switching admin color role")

    if color == "normal" or color == "clear" or color == "c":
        # Just add the normal Admin role back if user lost it
        if admin_role and admin_role not in member.roles:
            await member.add_roles(admin_role, reason="Reset to normal Admin role")
        await interaction.followup.send(
            "Your admin name color has been reset to normal Admin.", ephemeral=True
        )
        return

    if color not in COLOR_ROLES:
        await interaction.followup.send(
            "Invalid color! Choose from: green, blue, purple, red, pink, or normal.", ephemeral=True
        )
        return

    # Remove the normal Admin role before adding the color role (if user has it)
    if admin_role and admin_role in member.roles:
        await member.remove_roles(admin_role, reason="Switching to colored admin role")

    role_name = f"AdminColor: {color.capitalize()}"
    role = discord.utils.get(guild.roles, name=role_name)

    if not role:
        try:
            role = await guild.create_role(
                name=role_name,
                color=COLOR_ROLES[color],
                reason="Admin color role for /adminnamecolor command"
            )
            bot_top_role = guild.me.top_role
            await role.edit(position=bot_top_role.position - 1)
        except Exception as e:
            await interaction.followup.send(f"Failed to create role: {e}", ephemeral=True)
            return

    await member.add_roles(role)
    await interaction.followup.send(
        f"Your admin name color has been changed to {color}! You still have full admin access.", ephemeral=True
    )

bot.run('MTM5NTI0MDMyNzYzNTUzMzkwNQ.GTsVTE.3jiqceM4aaxUm4-7j-sRj4FBHQJ_r2GFwkyrjc')
