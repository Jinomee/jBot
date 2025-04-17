# Discord AI 助手机器人 - jBot

*[English](README.md) | 简体中文*

一个与 x.ai API 集成的 Discord 机器人，提供多种对话模式、用户特定的对话历史记录以及频道自动回复功能。

## 功能特点

- **多种 AI 模式**：在不同的个性和用例之间切换，如一般聊天、学习助手、编程帮手等
- **对话历史**：在不同聊天中为每个用户维护单独的对话历史记录
- **频道自动回复**：配置特定频道，机器人将回复所有消息，无需被提及
- **简单命令系统**：所有交互都有易于使用的斜杠命令
- **用户友好界面**：整洁的嵌入式消息和交互组件，提供精致的用户体验

## 设置说明

### 前提条件

- Python 3.12（Discord.py v2.3.2 不支持 Python 3.13）
- Discord 机器人令牌（在 [Discord 开发者门户](https://discord.com/developers/applications) 创建）
- x.ai API 密钥（在 [x.ai](https://x.ai) 注册）

### 安装

1. 克隆此仓库：
   ```
   git clone https://github.com/Jinomee/jBot.git
   cd jBot
   ```

2. 安装所需依赖：
   ```
   pip install -r requirements.txt
   ```

### 手动安装

1. 从[发布页面](https://github.com/Jinomee/jBot/releases)下载最新版本。
2. 将ZIP文件解压到您想要的位置。
3. 打开终端或命令提示符并导航到解压目录：
   ```
   cd path/to/extracted/jBot
   ```
4. 安装所需依赖：
   ```
   pip install -r requirements.txt
   ```

3. 在 `.env` 文件中配置环境变量：
   ```
   # Discord 机器人令牌
   DISCORD_TOKEN=your_discord_bot_token_here

   # AI API 配置
   AI_API_URL=https://api.x.ai/v1
   XAI_API_KEY=your_xai_api_key_here

   # AI 模型选择
   AI_MODEL=grok-3-mini-beta
   ```

4. 运行机器人：
   ```
   python bot.py
   ```

### 将机器人添加到您的服务器

1. 前往 [Discord 开发者门户](https://discord.com/developers/applications)
2. 选择您的应用程序并前往 "OAuth2" → "URL Generator" 选项卡
3. 选择以下范围：
   - `bot`
   - `applications.commands`
4. 选择以下机器人权限：
   - `Send Messages`
   - `Send Messages in Threads`
   - `Embed Links`
   - `Attach Files`
   - `Read Message History`
   - `Use Slash Commands`
   - `Use Embedded Activities`
5. 复制并打开生成的 URL，将机器人添加到您的服务器

## 使用方法

### 与机器人互动

机器人响应：
- 直接消息
- 提及（@机器人名称）
- 已启用自动回复频道中的消息

### 斜杠命令

- `/help` - 显示所有可用命令
- `/mode` - 查看并更改 AI 助手模式
- `/newchat` - 与 AI 开始新对话
- `/chathistory` - 查看并选择您之前的对话
- `/settings` - 配置 AI 助手设置
- `/clear` - 清除您当前的对话历史
- `/autoreply` - 在特定频道中切换自动回复（需要管理频道权限）

### 设置自动回复频道

1. 使用命令：`/autoreply channel:#channel-name`
2. 机器人现在将回复该频道中的所有消息，无需被提及
3. 要在频道中禁用自动回复：`/autoreply channel:#channel-name enable:False`

## AI 模式

机器人预配置了几种 AI 模式：

- **一般聊天** - 与 AI 助手进行休闲对话
- **学习助手** - 帮助学习和理解新概念
- **编程帮手** - 提供编程和代码任务的帮助
- **创意写作** - 帮助创意写作和内容创作
- **语言导师** - 练习并学习新语言
- **个人教练** - 获取个人成长的动力和指导

您可以通过编辑 `config.py` 文件中的 `DEFAULT_AI_MODES` 字典轻松添加更多模式。

## 自定义

### 添加新的 AI 模式

编辑 `config.py` 文件添加新模式：

```python
"your_mode_id": {
    "name": "您的模式名称",
    "description": "此模式功能的描述",
    "system_prompt": "定义 AI 在此模式下行为的系统提示"
}
```

### 更改机器人设置

可以在 `config.py` 文件中配置各种机器人设置：

```python
BOT_SETTINGS = {
    "default_mode": "general_chatting",
    "max_tokens": 500,
    "user_data_file": "user_data.json",
    "command_cooldown": 3  # 秒
}
```

## 故障排除

- **斜杠命令未出现**：尝试使用同时包含 `bot` 和 `applications.commands` 范围的 URL 再次邀请机器人到您的服务器。
- **机器人不响应**：检查 `.env` 文件中的 Discord 令牌是否正确。
- **API 错误**：验证您的 x.ai API 密钥，并确保您有足够的 API 额度。
- **权限问题**：确保机器人在您的 Discord 服务器中具有适当的权限。

## 许可证

此项目根据 MIT 许可证授权 - 有关详细信息，请参阅 LICENSE 文件。

## 致谢

- 使用 [x.ai](https://x.ai) 的 API 实现 AI 功能
- 使用 [discord.py](https://discordpy.readthedocs.io/) 库构建 