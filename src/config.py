from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")
    MONGODB_URI: str = os.getenv("MONGO_URI")
    DB_NAME: str = os.getenv("DB_NAME")
    
settings = Settings()  

#Check Error
if not settings.BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in environment variables")
if not settings.MONGODB_URI:
    raise ValueError("MONGO_URI is not set in environment variables")
if not settings.DB_NAME:
    raise ValueError("DB_NAME is not set in environment variables")