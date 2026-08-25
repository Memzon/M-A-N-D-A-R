import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN", "")
GUILD_ID = int(os.getenv("GUILD_ID", "0") or 0)

CHEST_CHANNEL_ID = int(os.getenv("CHEST_CHANNEL_ID", "0") or 0)
SPEED_CHANNEL_ID = int(os.getenv("SPEED_CHANNEL_ID", "0") or 0)

CURRENCY_NAME = os.getenv("CURRENCY_NAME", "Coin")
CURRENCY_EMOJI = os.getenv("CURRENCY_EMOJI", "🪙")

# Dakika cinsinden - etkinliklerin ne sıklıkla (rastgele aralıkta) tetikleneceği
CHEST_MIN_INTERVAL = int(os.getenv("CHEST_MIN_INTERVAL_MIN", "30"))
CHEST_MAX_INTERVAL = int(os.getenv("CHEST_MAX_INTERVAL_MIN", "120"))
SPEED_MIN_INTERVAL = int(os.getenv("SPEED_MIN_INTERVAL_MIN", "20"))
SPEED_MAX_INTERVAL = int(os.getenv("SPEED_MAX_INTERVAL_MIN", "90"))

CHEST_MIN_REWARD = int(os.getenv("CHEST_MIN_REWARD", "50"))
CHEST_MAX_REWARD = int(os.getenv("CHEST_MAX_REWARD", "500"))
SPEED_MIN_REWARD = int(os.getenv("SPEED_MIN_REWARD", "100"))
SPEED_MAX_REWARD = int(os.getenv("SPEED_MAX_REWARD", "750"))

SPEED_TIMEOUT = int(os.getenv("SPEED_TIMEOUT_SEC", "30"))
SPEED_CODE_LENGTH = int(os.getenv("SPEED_CODE_LENGTH", "6"))
