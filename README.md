# Discord AI Assistant Bot

*English | [简体中文](README.zh-CN.md)*

A Discord bot that integrates with x.ai's API to provide an interactive AI assistant with multiple conversation modes, user-specific conversation history, and channel auto-response capabilities.

## Features

- **Multiple AI Modes**: Switch between different personalities and use cases like general chatting, learning assistant, coding helper, etc.
- **Conversation History**: Maintains separate conversation histories for each user across different chats
- **Channel Auto-Response**: Configure specific channels where the bot will respond to all messages without needing to be pinged
- **Simple Command System**: Easy-to-use slash commands for all interactions
- **User-Friendly Interface**: Clean embeds and interactive components for a polished user experience

## Setup Instructions

### Prerequisites

- Python 3.12 (Discord.py v2.3.2 does not support Python 3.13)
- A Discord bot token (create one at [Discord Developer Portal](https://discord.com/developers/applications))
- An x.ai API key (sign up at [x.ai](https://x.ai))

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/Jinomee/jBot.git
   cd jBot
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure your environment variables in the `.env` file:
   ```
   # Discord Bot Token
   DISCORD_TOKEN=your_discord_bot_token_here

   # AI API Configuration
   AI_API_URL=https://api.x.ai/v1
   XAI_API_KEY=your_xai_api_key_here

   # AI Model Selection
   AI_MODEL=grok-3-mini-beta
   ```

4. Run the bot:
   ```
   python bot.py
   ```

### Adding the Bot to Your Server

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Select your application and go to the "OAuth2" → "URL Generator" tab
3. Select the following scopes:
   - `bot`
   - `applications.commands`
4. Select the following bot permissions:
   - `Send Messages`
   - `Send Messages in Threads`
   - `Embed Links`
   - `Attach Files`
   - `Read Message History`
   - `Use Slash Commands`
   - `Use Embedded Activities`
5. Copy and open the generated URL to add the bot to your server

## Usage

### Interacting with the Bot

The bot responds to:
- Direct messages
- Mentions (@BotName)
- Messages in enabled auto-reply channels

### Slash Commands

- `/help` - Displays all available commands
- `/mode` - View and change the AI assistant mode
- `/newchat` - Start a new conversation with the AI
- `/chathistory` - View and select from your previous conversations
- `/settings` - Configure the AI assistant settings
- `/clear` - Clear your current conversation history
- `/autoreply` - Toggle auto-responses in a specific channel (requires Manage Channels permission)

### Setting Up Auto-Reply Channels

1. Use the command: `/autoreply channel:#channel-name`
2. The bot will now respond to all messages in that channel without needing to be pinged
3. To disable auto-replies in a channel: `/autoreply channel:#channel-name enable:False`

## AI Modes

The bot comes with several pre-configured AI modes:

- **General Chatting** - Casual conversation with the AI assistant
- **Learning Assistant** - Help with studying and learning new concepts
- **Coding Helper** - Assistance with programming and coding tasks
- **Creative Writing** - Help with creative writing and content creation
- **Language Tutor** - Practice and learn new languages
- **Personal Coach** - Get motivation and guidance for personal growth

You can easily add more modes by editing the `DEFAULT_AI_MODES` dictionary in the `config.py` file.

## Customization

### Adding New AI Modes

Edit the `config.py` file to add new modes:

```python
"your_mode_id": {
    "name": "Your Mode Name",
    "description": "Description of what this mode does",
    "system_prompt": "System prompt that defines the AI's behavior in this mode"
}
```

### Changing Bot Settings

Various bot settings can be configured in the `config.py` file:

```python
BOT_SETTINGS = {
    "default_mode": "general_chatting",
    "max_tokens": 500,
    "user_data_file": "user_data.json",
    "command_cooldown": 3  # seconds
}
```

## Troubleshooting

- **Slash Commands Not Appearing**: Try inviting the bot to your server again using the URL with both `bot` and `applications.commands` scopes.
- **Bot Not Responding**: Check that your Discord token is correct in the `.env` file.
- **API Errors**: Verify your x.ai API key and make sure you have sufficient API credits.
- **Permission Issues**: Ensure the bot has proper permissions in your Discord server.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Uses [x.ai](https://x.ai)'s API for AI capabilities
- Built with [discord.py](https://discordpy.readthedocs.io/) library
