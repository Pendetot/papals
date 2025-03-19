import os
from dotenv import load_dotenv

load_dotenv(".env")

MAX_BOT = int(os.getenv("MAX_BOT", "100"))
DEVS = list(map(int, os.getenv("DEVS", "8010700213").split()))
API_ID = int(os.getenv("API_ID", ""))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
OWNER_ID = int(os.getenv("OWNER_ID", ""))
BLACKLIST_CHAT = list(map(int, os.getenv("BLACKLIST_CHAT", "-1002125842026 -1002053287763 -1002044997044 -1002022625433 -1002050846285").split()))
RMBG_API = os.getenv("RMBG_API", "a6qxsmMJ3CsNo7HyxuKGsP1o")
MONGO_URL = os.getenv("MONGO_URL", "")
LOGS_MAKER_UBOT = int(os.getenv("LOGS_MAKER_UBOT"))
API_KEY = os.getenv("API_KEY", "")
USER_GROUP = os.getenv("USER_GROUP", "@SEWAUBOT")
