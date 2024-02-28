import os
import discord
import interactions
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('GUILD_ID')
API = os.getenv('API_KEY')

genai.configure(api_key=API)
intents = discord.Intents.default()
client = discord.Client(intents=intents)
bot = interactions.Client(token=TOKEN)

generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

convo = model.start_chat(history=[
    
])
chat = convo.send_message

async def generate_response(message):
    if message:
        response = chat(message)
        if response and response.text:
            message_text = response.text.strip()
            return message_text
    return "No response available."




async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        print("Message sent!")
        return

    # Pass the user's message as the prompt to the AI model
    response = await generate_response(message.content)
    chunks = [response[i:i + 2000] for i in range(0, len(response), 2000)]

    for chunk in chunks:
        await message.channel.send(content=chunk, ephemeral=False)

@bot.command(
    name="chat",
    description="Chat with the AI!",
    options=[
        interactions.Option(
            name="message",
            description="Message to send to the AI",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def chat_command(ctx, message: str):
    await ctx.defer()

    # Use the message string to send to the AI model
    response = await generate_response(message)

    chunks = [response[i:i + 2000] for i in range(0, len(response), 2000)]
    for chunk in chunks:
        await ctx.send(content=chunk, ephemeral=False)
bot.start()
