#!/usr/bin/env python
"""
Discord AI Bot Launcher
This script provides a simple way to run the Discord AI bot.
"""

import os
import sys
import subprocess

def check_dependencies():
    """Check if all dependencies are installed"""
    try:
        import discord
        import dotenv
        import aiohttp
        print("✅ All dependencies are installed.")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {str(e)}")
        print("Installing dependencies...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ Dependencies installed successfully.")
            return True
        except Exception as e:
            print(f"❌ Failed to install dependencies: {str(e)}")
            return False

def check_env_file():
    """Check if .env file exists and has required variables"""
    if not os.path.exists(".env"):
        print("❌ .env file not found.")
        create_env_file()
        return False
    
    with open(".env", "r") as f:
        env_content = f.read()
    
    required_vars = ["DISCORD_TOKEN", "AI_API_URL", "AI_API_TOKEN"]
    missing_vars = []
    
    for var in required_vars:
        if f"{var}=" not in env_content or f"{var}=your_{var.lower()}_here" in env_content:
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please update your .env file with the required variables.")
        return False
    
    print("✅ Environment file is configured.")
    return True

def create_env_file():
    """Create a template .env file"""
    with open(".env", "w") as f:
        f.write("""# Discord Bot Token
DISCORD_TOKEN=your_discord_token_here

# AI API Configuration
AI_API_URL=your_ai_api_url_here
AI_API_TOKEN=your_ai_api_token_here
""")
    print("📝 Created template .env file. Please update it with your actual values.")

def run_bot():
    """Run the Discord bot"""
    try:
        import bot
        print("🤖 Starting Discord AI bot...")
        bot.bot.run(bot.DISCORD_TOKEN)
    except Exception as e:
        print(f"❌ Failed to run bot: {str(e)}")

def main():
    """Main function"""
    print("=== Discord AI Bot Launcher ===")
    
    if not check_dependencies():
        print("❌ Please install the required dependencies and try again.")
        return
    
    if not check_env_file():
        print("❌ Please configure your .env file and try again.")
        return
    
    run_bot()

if __name__ == "__main__":
    main()
