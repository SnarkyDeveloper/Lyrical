from lyrical import Lyrics
import asyncio
asyncio.run(Lyrics.start_api(port=8000, host="0.0.0.0"))

# Test api
import requests

response = requests.get("http://0.0.0.0:8000/lyrics?q=Hello World")