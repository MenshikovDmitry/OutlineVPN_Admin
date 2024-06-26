import os

API_URL = os.getenv('API_URL', 'https://192.168.1.2:5858/api')
API_TOKEN = os.getenv('API_TOKEN')

assert API_TOKEN is not None, 'API_TOKEN enviromental variable must be provided'

HOSTNAME = os.getenv('HOSTNAME', 'localhost')
PORT = os.getenv('PORT', "")

WEBSITE_API_URL = f"{HOSTNAME}"
if PORT != "":
    WEBSITE_API_URL += f":{PORT}"
WEBSITE_API_URL += "/"