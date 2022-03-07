import os

from dotenv import load_dotenv


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_file_path = os.path.join(BASE_DIR, '.env')
load_dotenv(env_file_path)

SERVER_HOST = os.getenv('SERVER_HOST', 'localhost')
SERVER_PORT = int(os.getenv('SERVER_PORT', 8002))

MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')
MONGO_PORT = os.getenv('MONGO_PORT', '27017')
MONGO_URL = f"mongodb://{MONGO_HOST}:{MONGO_PORT}"

database_name = 'files'
files_collection = 'files_metadata'

