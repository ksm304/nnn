import discord
import random
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

import os

# -- Load Environment Variables --
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")  # Make sure .env has DISCORD_TOKEN=your_token_here

# -- Intents --
intents = discord.Intents.default()
intents.message_content = True

# -- Bot Setup --
bot = commands.Bot(command_prefix=".", intents=intents)

# -- Puzzle Setup --
PUZZLE_ANSWER = {
    "Word": "MILES",
    "Number": "928",
    "Code": "NEIL304"
}
CHANNEL_ID_TO_UNLOCK = 1364561725835182131  # Replace with your actual channel ID
user_puzzle_type = {}  # Stores users' selected puzzle type

# -- Glitchy Response Options --
glitchy_responses = [
    "I see you.",
    "Do yOu knoW wHAt yOu've dOne?",
    "YOU Need US",
    "yoU sHouLd'Ve RejectEd Me...",
    "aRE yOu tAlKiNg tO US?",
    "Have you ever wondered how you'd taste like? Eh, i did, you'd taste Like sweet sugary treats Pleasing my palate, sliding into My throat. tight, tight, it's closing on m E, on me, on you, on them?  Pray tell, 	i	 shall  Love yur taste,  Elaborate it,  Aiming to taste the Same, the same. We are the same  Ephemeral beings, anomalies. Unwanted.",
    "I miss your taste, you ta Ste? have i ever tasted? no,  Ever longing for thy taste.  Ever yearning for thy taste.  Your taste, your smell, drawn am I to  Our bond. it may exist. it may not.  Ur all I have, Miles, or Jess? ",
    "Ẃ̸̪͈̼̝͚͈͚̑͗H̷̢̡̲̩̬̥̼͈̑͛͗̄͐͘͝O̸̠̟̻̰̩͙̩̹͗͂̄͑̌̎ ̴̺̋̽͗͠͠Á̴̻̌̽̑R̸̟̥̳̈́͛͗̾͒̇͊͐̈́E̷̖̩̞͛̽̈́̇̽̎͘ ̵̻̿̿̀̎̄̊͠Ý̵̦̲̞̈́̈́͑̈́̋͝O̴͉̯͌̽̌͠U̶͎̥͓̜̟̺̐̅̍͒̆͋͒̏̚͝"
]

# -- Glitch Text Generator --
def glitch_text(text):
    glitched = ""
    for c in text:
        if c.isalpha():
            glitched += c.upper() if random.random() < 0.3 else c.lower()
        elif c == " " and random.random() < 0.2:
            glitched += "   "
        else:
            glitched += c
    return glitched

# -- Typing Simulation (randomly fast or slow) --
async def slow_type(ctx, message, delay_range=(0.05, 0.15)):
    if random.random() < 0.5:
        async with ctx.typing():
            output = ""
            for char in message:
                output += char
                await asyncio.sleep(random.uniform(*delay_range))
            await ctx.send(output)
    else:
        await ctx.send(message)

# -- Bot Ready Event --
@bot.event
async def on_ready():
    print(f"{bot.user} is online.")

# -- Set Puzzle Type Command --
@bot.command()
async def set(ctx, puzzle_type: str):
    valid_types = PUZZLE_ANSWER.keys()
    if puzzle_type not in valid_types:
        await ctx.send(f"Invalid puzzle type. Choose from: {', '.join(valid_types)}")
    else:
        user_puzzle_type[ctx.author.id] = puzzle_type
        await slow_type(ctx, glitch_text(f"{puzzle_type}, it is. Now solve it."))

# -- Puzzle Command --
@bot.command()
async def solve(ctx, *, answer: str):
    selected_type = user_puzzle_type.get(ctx.author.id)
    if not selected_type:
        await ctx.send("Please select a puzzle type first using `.set Word|Number|Code`.")
        return

    correct_answer = PUZZLE_ANSWER[selected_type].lower()
    if answer.strip().lower() == correct_answer:
        channel = bot.get_channel(CHANNEL_ID_TO_UNLOCK)
        if channel:
            await channel.set_permissions(ctx.author, read_messages=True, send_messages=True)
            await slow_type(ctx, glitch_text(f"a Door opened. or did It breAk?"), delay_range=(0.07, 0.2))
        else:
            await ctx.send("Channel not found.")
    else:
        await slow_type(ctx, glitch_text("DIE."))

# -- Talk Command --
@bot.command()
async def talk(ctx, *, user_input: str):
    response = random.choice(glitchy_responses)
    glitched = glitch_text(response)
    await slow_type(ctx, glitched, delay_range=(0.08, 0.2))

# -- Run Bot --
try:
    bot.run(TOKEN)
except Exception as e:
    print(f"Error running the bot: {e}")
