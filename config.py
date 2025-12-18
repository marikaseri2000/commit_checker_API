import os
from dotenv import load_dotenv

#il TOKEN non deve essere pushato

load_dotenv()

base_url = os.getenv("BASE_URL")
URL = os.getenv("URL")
github_token = os.getenv("GITHUB_TOKEN")