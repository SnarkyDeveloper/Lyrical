from lyrical import Lyrics
import asyncio
import json
asyncio.run(Lyrics.start_api(port=8000, host="127.0.0.1"))

import requests

response = requests.get("http://localhost:8000/lyrics?q=Hello World")
print(json.loads(response.text))