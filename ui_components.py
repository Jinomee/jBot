import discord
from discord import ui

class ModeSelectView(ui.View):
    """View for selecting AI modes"""
    
    def __init__(self, modes, user_handler, ai_handler, timeout=60):
        super().__init__(timeout=timeout)
        self.user_handler = user_handler
        self.ai_handler = ai_handler
        
        # Add buttons for each mode
        for mode_id, mode_info in modes.items():
            self.add_mode_button(mode_id, mode_info["name"])
    
    def add_mode_button(self, mode_id, mode_name):
        """Add a button for a mode"""
        button = ui.Button(
            label=mode_name,
            custom_id=f"mode_{mode_id}",
            style=discord.ButtonStyle.primary
        )
        
        async def button_callback(interaction):
            user_id = str(interaction.user.id)
            self.user_handler.set_user_mode(user_id, mode_id)
            mode_info = self.ai_handler.get_mode_info(mode_id)
            await interaction.response.send_message(
                f"Mode changed to **{mode_info['name']}**!", 
                ephemeral=True
            )
        
        button.callback = button_callback
        self.add_item(button)


class ChatHistoryView(ui.View):
    """View for selecting from chat history"""
    
    def __init__(self, chats, user_handler, timeout=60):
        super().__init__(timeout=timeout)
        self.user_handler = user_handler
        
        # Add buttons for each chat
        for chat_id, name, _ in chats:
            self.add_chat_button(chat_id, name)
    
    def add_chat_button(self, chat_id, chat_name):
        """Add a button for a chat"""
        button = ui.Button(
            label=chat_name,
            custom_id=f"chat_{chat_id}",
            style=discord.ButtonStyle.secondary
        )
        
        async def button_callback(interaction):
            user_id = str(interaction.user.id)
            self.user_handler.switch_chat(user_id, chat_id)
            await interaction.response.send_message(
                f"Switched to chat: **{chat_name}**", 
                ephemeral=True
            )
        
        button.callback = button_callback
        self.add_item(button)


class ClearConfirmView(ui.View):
    """View for confirming chat clearing"""
    
    def __init__(self, user_handler, user_id, timeout=30):
        super().__init__(timeout=timeout)
        self.user_handler = user_handler
        self.user_id = user_id
        
        # Add confirm button
        confirm_button = ui.Button(
            label="Confirm",
            custom_id="clear_confirm",
            style=discord.ButtonStyle.danger
        )
        
        async def confirm_callback(interaction):
            self.user_handler.clear_chat(self.user_id)
            await interaction.response.send_message(
                "Conversation cleared! The AI will no longer remember your previous messages in this chat.",
                ephemeral=True
            )
        
        confirm_button.callback = confirm_callback
        self.add_item(confirm_button)
        
        # Add cancel button
        cancel_button = ui.Button(
            label="Cancel",
            custom_id="clear_cancel",
            style=discord.ButtonStyle.secondary
        )
        
        async def cancel_callback(interaction):
            await interaction.response.send_message("Operation cancelled.", ephemeral=True)
        
        cancel_button.callback = cancel_callback
        self.add_item(cancel_button)
