import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

# Import custom modules
from ai_handler import AIHandler
from user_data_handler import UserDataHandler
from ui_components import ModeSelectView, ChatHistoryView, ClearConfirmView
from config import BOT_SETTINGS

# Load environment variables
load_dotenv()

# Bot configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Bot setup - Use an empty prefix so no prefix commands work
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="", intents=intents)

# Initialize handlers
ai_handler = AIHandler()
user_handler = UserDataHandler()

async def generate_ai_response(user_id, message_content):
    """Generate a response from the AI model"""
    # Get user data
    mode = user_handler.get_current_mode(user_id)
    conversation = user_handler.get_conversation(user_id)
    
    # Add user message to conversation
    user_handler.add_message(user_id, "user", message_content)
    
    # Get updated conversation
    conversation = user_handler.get_conversation(user_id)
    
    # Prepare messages for API
    mode_info = ai_handler.get_mode_info(mode)
    messages = [{"role": "system", "content": mode_info["system_prompt"]}]
    messages.extend(conversation)
    
    # Call AI API
    ai_response = await ai_handler.generate_response(messages)
    
    # Add AI response to conversation
    user_handler.add_message(user_id, "assistant", ai_response)
    
    return ai_response

# Bot events
@bot.event
async def on_ready():
    """Called when the bot is ready"""
    print(f'{bot.user} has connected to Discord!')
    
    # Register commands on startup
    print("Registering application (/) commands...")
    
    try:
        # Clear existing commands to avoid issues
        if bot.application_id:
            # This is a direct approach that always works
            await bot.http.bulk_upsert_global_commands(bot.application_id, [])
            print("Cleared existing commands.")
        
        # Now register the commands to Discord
        # This approach directly registers the commands with Discord API
        synced = await bot.tree.sync()
        
        # Show the registered commands
        command_names = [cmd.name for cmd in synced]
        print(f"Successfully registered {len(synced)} commands: {', '.join(command_names)}")
        
        # Show invite link in case the bot needs to be reinvited
        if hasattr(bot, 'application_id') and bot.application_id:
            print(f"If commands don't appear, use this invite link:")
            print(f"https://discord.com/api/oauth2/authorize?client_id={bot.application_id}&permissions=274878024704&scope=bot%20applications.commands")
    except Exception as e:
        print(f"Error registering commands: {e}")

@bot.event
async def on_message(message):
    """Handle incoming messages"""
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return
    
    # Only respond to direct messages, mentions, or in enabled channels
    is_dm = isinstance(message.channel, discord.DMChannel)
    is_mentioned = bot.user in message.mentions
    
    # Check if this is an enabled channel for this guild
    is_enabled_channel = False
    if message.guild:
        guild_id = str(message.guild.id)
        channel_id = str(message.channel.id)
        guild_data = user_handler.get_guild_data(guild_id)
        is_enabled_channel = channel_id in guild_data.get("enabled_channels", [])
    
    if is_dm or is_mentioned or is_enabled_channel:
        # Remove mention from message content if present
        content = message.content
        if is_mentioned:
            content = content.replace(f'<@{bot.user.id}>', '').strip()
        
        # Only proceed if there's content
        if content:
            # Show typing indicator
            async with message.channel.typing():
                # Generate AI response
                response = await generate_ai_response(str(message.author.id), content)
            
            # Send response
            if not response or not response.strip():
                response = "Sorry, I couldn't generate a response at this time."
            await message.reply(response)

# Bot slash commands
@bot.tree.command(name="help", description="Display all available commands")
async def help_command(interaction: discord.Interaction):
    """Display all available commands"""
    embed = discord.Embed(
        title="AI Assistant Bot Commands",
        description="Here are all the available commands:",
        color=discord.Color.blue()
    )
    
    embed.add_field(name="/help", value="Display this help message", inline=False)
    embed.add_field(name="/mode", value="View and change the AI assistant mode", inline=False)
    embed.add_field(name="/newchat", value="Start a new conversation with the AI", inline=False)
    embed.add_field(name="/chathistory", value="View and select from your previous conversations", inline=False)
    embed.add_field(name="/settings", value="Configure the AI assistant settings", inline=False)
    embed.add_field(name="/clear", value="Clear your current conversation history", inline=False)
    embed.add_field(name="/autoreply", value="Toggle AI auto-responses in a specific channel", inline=False)
    
    # Add usage information
    embed.add_field(
        name="Channel Auto-Response Feature",
        value="You can set up specific channels where the bot will respond to all messages without needing to ping it:\n"
              "1. Use `/autoreply channel:#channel-name` to enable auto-responses in a channel\n"
              "2. The bot will then respond to all messages in that channel\n"
              "3. Use `/autoreply channel:#channel-name enable:False` to turn this feature off\n"
              "Note: You need 'Manage Channels' permission to use this command",
        inline=False
    )
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="mode", description="View and change the AI assistant mode")
async def mode_command(interaction: discord.Interaction):
    """Display available AI modes and allow selection"""
    user_id = str(interaction.user.id)
    current_mode = user_handler.get_current_mode(user_id)
    all_modes = ai_handler.get_all_modes()
    mode_info = ai_handler.get_mode_info(current_mode)
    
    # Create embed
    embed = discord.Embed(
        title="AI Assistant Modes",
        description=f"Current mode: **{mode_info['name']}**\n\nSelect a mode below:",
        color=discord.Color.green()
    )
    
    # Add fields for each mode
    for mode_id, mode_info in all_modes.items():
        embed.add_field(
            name=mode_info["name"], 
            value=mode_info["description"], 
            inline=False
        )
    
    # Create mode selection view
    view = ModeSelectView(all_modes, user_handler, ai_handler)
    
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

@bot.tree.command(name="newchat", description="Start a new conversation with the AI")
async def newchat_command(interaction: discord.Interaction, name: str = None):
    """Create a new chat session"""
    user_id = str(interaction.user.id)
    
    # Create new chat
    chat_id, chat_name = user_handler.create_new_chat(user_id, name)
    
    await interaction.response.send_message(
        f"Started a new chat: **{chat_name}**\nYou can now continue your conversation with a fresh memory.",
        ephemeral=True
    )

@bot.tree.command(name="chathistory", description="View and select from your previous conversations")
async def chathistory_command(interaction: discord.Interaction):
    """Display chat history and allow selection"""
    user_id = str(interaction.user.id)
    
    # Get chat history
    chats = user_handler.get_chat_history(user_id)
    
    # Create embed
    embed = discord.Embed(
        title="Your Chat History",
        description="Select a chat to continue the conversation:",
        color=discord.Color.gold()
    )
    
    if not chats:
        embed.description = "You don't have any previous chats. Use /newchat to start one!"
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    # Get current chat ID
    user_data = user_handler.get_user_data(user_id)
    current_chat_id = user_data["current_chat_id"]
    
    # Add fields for each chat
    for chat_id, name, message_count in chats:
        is_current = chat_id == current_chat_id
        embed.add_field(
            name=f"{name} {'(Current)' if is_current else ''}",
            value=f"{message_count} messages",
            inline=False
        )
    
    # Create chat selection view
    view = ChatHistoryView(chats, user_handler)
    
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

@bot.tree.command(name="clear", description="Clear your current conversation history")
async def clear_command(interaction: discord.Interaction):
    """Clear the current conversation"""
    user_id = str(interaction.user.id)
    
    # Create confirmation view
    view = ClearConfirmView(user_handler, user_id)
    
    await interaction.response.send_message(
        "Are you sure you want to clear your current conversation history? This cannot be undone.",
        view=view,
        ephemeral=True
    )

@bot.tree.command(name="settings", description="Configure the AI assistant settings")
async def settings_command(interaction: discord.Interaction):
    """Configure AI settings"""
    embed = discord.Embed(
        title="AI Assistant Settings",
        description="Configure your AI assistant settings below:",
        color=discord.Color.purple()
    )
    
    embed.add_field(
        name="API Configuration",
        value="The AI API is currently configured with the following settings:\n"
              f"- API URL: `{ai_handler.api_url if ai_handler.api_url else 'Not configured'}`\n"
              f"- API Token: `{'Configured' if ai_handler.api_token else 'Not configured'}`\n\n"
              "To change these settings, update your .env file and restart the bot.",
        inline=False
    )
    
    embed.add_field(
        name="Bot Settings",
        value=f"- Default Mode: `{ai_handler.get_mode_info(BOT_SETTINGS.get('default_mode', 'general_chatting'))['name']}`\n"
              f"- Max Response Tokens: `{BOT_SETTINGS.get('max_tokens', 500)}`",
        inline=False
    )
    
    # Add guild-specific settings if in a guild
    if interaction.guild:
        guild_id = str(interaction.guild.id)
        guild_data = user_handler.get_guild_data(guild_id)
        enabled_channels = guild_data.get("enabled_channels", [])
        
        if enabled_channels:
            channel_mentions = []
            for channel_id in enabled_channels:
                channel = interaction.guild.get_channel(int(channel_id))
                if channel:
                    channel_mentions.append(channel.mention)
            
            if channel_mentions:
                embed.add_field(
                    name="Auto-Reply Channels",
                    value="The bot will automatically respond to all messages in these channels:\n• " + 
                          "\n• ".join(channel_mentions) + 
                          f"\n\nUse `/autoreply` to manage auto-reply channels.",
                    inline=False
                )
        else:
            embed.add_field(
                name="Auto-Reply Channels",
                value="No channels are currently set up for auto-replies.\n" +
                      "Use `/autoreply channel:#channel-name` to enable auto-replies in a channel.",
                inline=False
            )
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="autoreply", description="Toggle AI auto-responses in a specific channel")
@app_commands.guild_only()
@app_commands.checks.has_permissions(manage_channels=True)
@app_commands.describe(channel="The channel to enable/disable auto-responses in", enable="Enable or disable auto-responses (default: toggle)")
async def autoreply_command(interaction: discord.Interaction, channel: discord.TextChannel, enable: bool = None):
    """Toggle automatic AI responses in a specific channel"""
    # Guild-only check is handled by the decorator
    guild_id = str(interaction.guild.id)
    channel_id = str(channel.id)
    
    # Get current channel status
    guild_data = user_handler.get_guild_data(guild_id)
    is_enabled = channel_id in guild_data.get("enabled_channels", [])
    
    # Determine whether to enable or disable
    if enable is None:
        # Toggle if not specified
        enable = not is_enabled
    
    # Enable or disable the channel
    if enable:
        # Enable the channel if not already enabled
        if not is_enabled:
            user_handler.enable_channel(guild_id, channel_id)
            status = "enabled"
        else:
            status = "already enabled"
    else:
        # Disable the channel if currently enabled
        if is_enabled:
            user_handler.disable_channel(guild_id, channel_id)
            status = "disabled"
        else:
            status = "already disabled"
    
    # Create the response embed
    embed = discord.Embed(
        title="Auto-Reply Channel Settings",
        description=f"Auto-reply has been {status} for {channel.mention}",
        color=discord.Color.green() if enable else discord.Color.red()
    )
    
    # Add additional information
    if enable:
        embed.add_field(
            name="What this means",
            value="The bot will now respond to all messages in this channel without being mentioned.",
            inline=False
        )
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

# Run the bot
if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
