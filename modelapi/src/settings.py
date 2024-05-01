import os 
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('../.env')
load_dotenv(dotenv_path=dotenv_path)

DB_USER_NAME = os.getenv('MONGO_MODELDB_USER_USERNAME') 
DB_USER_PWD = os.getenv('MONGO_MODELDB_USER_PASSWORD')
DB_NAME = os.getenv('MONGO_MODELDB_NAME')
TABLE_NAME = os.getenv('MONGO_TABLE_NAME')

if __name__ == "__main__":
    print(DB_USER_NAME, DB_USER_PWD, DB_NAME, TABLE_NAME)