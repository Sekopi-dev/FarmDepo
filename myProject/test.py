from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Access environment variables
db_user = os.getenv('DB_USER')
print(db_user)
