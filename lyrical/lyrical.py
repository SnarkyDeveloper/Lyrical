import httpx
from bs4 import BeautifulSoup
import sys
import asyncio
from urllib.parse import quote_plus
import json
import fastapi
import uvicorn
app = fastapi.FastAPI()
sys.stdout.reconfigure(encoding='utf-8')
class Lyrics:
    async def search(query):
        try:
            search_url = f"https://genius.com/api/search/song?q={quote_plus(query)}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = httpx.get(search_url, headers=headers)
            json_data = response.json()
            
            if 'response' in json_data and json_data['response']['sections'][0]['hits']:
                hit = json_data['response']['sections'][0]['hits'][0]
                return hit['result']['url']
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    async def get_lyrics(url):
        try:
            response = httpx.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            lyrics_containers = soup.find_all('div', attrs={'data-lyrics-container': 'true'})
        
            if lyrics_containers:
                full_lyrics = []
                for container in lyrics_containers:
                    for br in container.find_all('br'):
                        br.replace_with('\n')
                    full_lyrics.append(container.get_text())
                return '\n'.join(full_lyrics)
            else:
                print("No lyrics container found.")
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None    
    async def get_artists(url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            script = soup.find('script', string=lambda text: text and '_sf_async_config.authors' in text)
            if script:
                authors_line = [line for line in script.string.split('\n') if 'authors' in line][0]
                artists = authors_line.split('=')[1].strip().strip("';")
                return artists
            
        return ""
    async def get_title(url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            title_meta = soup.find('meta', property='og:title')
            if title_meta:
                return title_meta['content']
                
            return ""    
    @classmethod
    async def lyrics(cls, query: str):
        url = await cls.search(query)
        if not url:
            return None
        lyrics = await cls.get_lyrics(url)
        artists = await cls.get_artists(url)
        title = await cls.get_title(url)
        data = {
            'title': title,
            'artists': artists,
            'lyrics': lyrics,
            'gennius_url': url
        }
        return json.dumps(data, indent=4)
    def start_api(port: int = 8000, host: str = "127.0.0.1"):
        @app.get("/")
        async def index():
            return {"error": "No query provided, enter a query in format /lyrics?q="}
        @app.get("/lyrics")
        async def lyrics(q: str):
            try:
                if not q:
                    return {"error": "No query provided, enter a query in format /lyrics?q="}
                result = await Lyrics.lyrics(q)
                return fastapi.responses.JSONResponse(content=json.loads(result))
            except:
                return {"error": "Error retrieving lyrics"}
        uvicorn.run(app, host=host, port=port)