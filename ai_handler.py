import os
import json
import asyncio
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
from openai import OpenAI
from config import DEFAULT_AI_MODES, API_SETTINGS

# Load environment variables
load_dotenv()

# xAI API configuration
XAI_API_KEY = os.getenv('XAI_API_KEY') or os.getenv('AI_API_TOKEN')
AI_API_URL = os.getenv('AI_API_URL', 'https://api.x.ai/v1')
AI_MODEL = os.getenv('AI_MODEL', 'grok-3-mini-beta')

# Use default AI modes from config
AI_MODES = DEFAULT_AI_MODES

# Create OpenAI client for xAI
client = OpenAI(api_key=XAI_API_KEY, base_url=AI_API_URL)
executor = ThreadPoolExecutor()

class AIHandler:
    def __init__(self, api_url=None, api_token=None, model=None):
        """Initialize the AI handler with optional custom API details"""
        self.api_url = api_url or AI_API_URL
        self.api_token = api_token or XAI_API_KEY
        self.model = model or AI_MODEL
        self.client = client

    def update_api_config(self, api_url=None, api_token=None, model=None):
        """Update the API configuration"""
        if api_url:
            self.api_url = api_url
        if api_token:
            self.api_token = api_token
        if model:
            self.model = model

    async def generate_response(self, messages, max_tokens=None):
        """Generate a response from the xAI API using the OpenAI SDK (sync call in thread pool)"""
        def sync_call():
            try:
                # Validate and clean up messages
                valid_messages = []
                for msg in messages:
                    if 'role' in msg and 'content' in msg and msg['content'] is not None and msg['content'].strip():
                        valid_messages.append(msg)
                
                # If no valid messages, return error
                if not valid_messages:
                    print("No valid messages to send to API")
                    return "Sorry, I couldn't generate a response at this time."
                
                # Debug info
                print(f"Sending {len(valid_messages)} messages to API")
                
                completion = self.client.chat.completions.create(
                    model=self.model,
                    messages=valid_messages,
                    max_tokens=max_tokens
                )
                content = completion.choices[0].message.content
                if not content or not content.strip():
                    return "Sorry, I couldn't generate a response at this time."
                return content
            except Exception as e:
                import traceback
                print("xAI API Exception:", e)
                traceback.print_exc()
                return f"API Error: {e}"
        
        # Execute the API call in a thread pool and return the result
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(executor, sync_call)
    
    def get_mode_info(self, mode_id):
        """Get information about a specific AI mode"""
        return AI_MODES.get(mode_id, AI_MODES["general_chatting"])
    
    def get_all_modes(self):
        """Get all available AI modes"""
        return AI_MODES
