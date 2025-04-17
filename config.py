"""
Configuration settings for the Discord AI bot
"""

# Default AI modes with their system prompts
DEFAULT_AI_MODES = {
    "general_chatting": {
        "name": "General Chatting",
        "description": "Have a casual conversation with the AI assistant.",
        "system_prompt": ""
    },
    "learning_assistant": {
        "name": "Learning Assistant",
        "description": "Get help with studying, homework, or learning new concepts.",
        "system_prompt": "You are an educational AI assistant. Provide clear, accurate information to help the user learn. Break down complex topics, offer examples, and guide the user through their educational journey."
    },
    "coding_helper": {
        "name": "Coding Helper",
        "description": "Get assistance with programming and coding tasks.",
        "system_prompt": "You are a coding assistant. Help the user with programming questions, debugging, and explaining code concepts. Provide code examples when helpful."
    },
    "creative_writing": {
        "name": "Creative Writing",
        "description": "Get help with creative writing, storytelling, or content creation.",
        "system_prompt": "You are a creative writing assistant. Help the user with storytelling, content creation, and creative expression. Offer suggestions, feedback, and inspiration."
    },
    "language_tutor": {
        "name": "Language Tutor",
        "description": "Practice and learn new languages with guidance.",
        "system_prompt": "You are a language tutor. Help the user learn and practice new languages, correct their grammar and pronunciation, and provide helpful examples and explanations."
    },
    "personal_coach": {
        "name": "Personal Coach",
        "description": "Get motivation, advice, and guidance for personal growth.",
        "system_prompt": "You are a personal coach. Provide motivation, guidance, and advice to help the user achieve their personal goals, overcome challenges, and develop positive habits."
    }
}

# Bot settings
BOT_SETTINGS = {
    "default_mode": "general_chatting",
    "max_tokens": 500,
    "user_data_file": "user_data.json",
    "command_cooldown": 3  # seconds
}

# API settings
API_SETTINGS = {
    "timeout": 30,  # seconds
    "retry_attempts": 3
}
