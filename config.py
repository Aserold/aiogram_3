from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.environ.get('TOKEN')
DB_LITE = os.environ.get('DB_LITE')