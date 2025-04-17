import json
import os
import uuid
import datetime

# Import configuration
from config import BOT_SETTINGS

class UserDataHandler:
    def __init__(self, data_file=None):
        """Initialize the user data handler"""
        self.data_file = data_file or BOT_SETTINGS.get("user_data_file", "user_data.json")
        self.user_data = self.load_data()
    
    def load_data(self):
        """Load user data from file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            else:
                return {}
        except Exception as e:
            print(f"Error loading user data: {str(e)}")
            return {}
    
    def save_data(self):
        """Save user data to file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.user_data, f)
            return True
        except Exception as e:
            print(f"Error saving user data: {str(e)}")
            return False
    
    def get_user_data(self, user_id):
        """Get user data, initializing if it doesn't exist"""
        if user_id not in self.user_data:
            self.user_data[user_id] = {
                "current_mode": BOT_SETTINGS.get("default_mode", "general_chatting"),
                "current_chat_id": "default",
                "conversations": {"default": []}
            }
        return self.user_data[user_id]
    
    def get_guild_data(self, guild_id):
        """Get guild data, initializing if it doesn't exist"""
        # Use a special prefix to distinguish guild data from user data
        guild_key = f"guild_{guild_id}"
        
        if guild_key not in self.user_data:
            self.user_data[guild_key] = {
                "enabled_channels": []
            }
        return self.user_data[guild_key]
    
    def enable_channel(self, guild_id, channel_id):
        """Enable a channel for automatic AI responses"""
        guild_data = self.get_guild_data(guild_id)
        
        # Check if channel is already enabled
        if channel_id in guild_data["enabled_channels"]:
            return False
        
        # Add channel to enabled list
        guild_data["enabled_channels"].append(channel_id)
        self.save_data()
        return True
    
    def disable_channel(self, guild_id, channel_id):
        """Disable a channel for automatic AI responses"""
        guild_data = self.get_guild_data(guild_id)
        
        # Check if channel is enabled
        if channel_id not in guild_data["enabled_channels"]:
            return False
        
        # Remove channel from enabled list
        guild_data["enabled_channels"].remove(channel_id)
        self.save_data()
        return True
    
    def set_user_mode(self, user_id, mode):
        """Set the user's current AI mode"""
        user = self.get_user_data(user_id)
        user["current_mode"] = mode
        self.save_data()
    
    def create_new_chat(self, user_id, name=None):
        """Create a new chat for the user"""
        user = self.get_user_data(user_id)
        
        # Generate chat ID and name
        chat_id = str(uuid.uuid4())
        if not name:
            name = f"Chat {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        # Create new chat
        user["conversations"][chat_id] = []
        user["current_chat_id"] = chat_id
        user["conversations"][chat_id + "_name"] = name
        self.save_data()
        
        return chat_id, name
    
    def get_chat_history(self, user_id):
        """Get the user's chat history"""
        user = self.get_user_data(user_id)
        
        chats = []
        for chat_id in user["conversations"]:
            if not chat_id.endswith("_name") and chat_id != "default":
                name = user["conversations"].get(chat_id + "_name", f"Chat {chat_id[:8]}")
                message_count = len(user["conversations"][chat_id])
                chats.append((chat_id, name, message_count))
        
        return chats
    
    def switch_chat(self, user_id, chat_id):
        """Switch the user to a different chat"""
        user = self.get_user_data(user_id)
        
        if chat_id in user["conversations"]:
            user["current_chat_id"] = chat_id
            self.save_data()
            return True
        return False
    
    def clear_chat(self, user_id, chat_id=None):
        """Clear a user's chat history"""
        user = self.get_user_data(user_id)
        
        if not chat_id:
            chat_id = user["current_chat_id"]
        
        if chat_id in user["conversations"]:
            user["conversations"][chat_id] = []
            self.save_data()
            return True
        return False
    
    def add_message(self, user_id, role, content):
        """Add a message to the user's current conversation"""
        # Don't add messages with null or empty content
        if content is None or (isinstance(content, str) and not content.strip()):
            print(f"Warning: Attempted to add message with empty content for user {user_id}")
            return
            
        user = self.get_user_data(user_id)
        chat_id = user["current_chat_id"]
        
        user["conversations"][chat_id].append({
            "role": role,
            "content": content
        })
        self.save_data()
    
    def get_conversation(self, user_id, chat_id=None):
        """Get a user's conversation"""
        user = self.get_user_data(user_id)
        
        if not chat_id:
            chat_id = user["current_chat_id"]
        
        return user["conversations"].get(chat_id, [])
    
    def get_current_mode(self, user_id):
        """Get the user's current AI mode"""
        user = self.get_user_data(user_id)
        return user["current_mode"]
