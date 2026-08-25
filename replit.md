# Replit setup

This project is a Python Discord bot located in `econobot/`. Its persistent
economy data is stored in `econobot/data/economy.db` using SQLite.

## Run command

```bash
cd econobot && python main.py
```

## Required environment variables

Configure these in Replit Secrets/environment variables before starting the
bot:

- `DISCORD_TOKEN` — the bot token from the Discord Developer Portal
- `GUILD_ID` — the Discord server ID where slash commands should sync
- `CHEST_CHANNEL_ID` — channel ID for chest events
- `SPEED_CHANNEL_ID` — channel ID for speed events

Optional tuning variables and their defaults are documented in
`econobot/.env.example`.

The Discord bot must have the Message Content and Server Members intents
enabled, and the invited bot needs permission to send messages, embed links,
attach files, read message history, and use slash commands.