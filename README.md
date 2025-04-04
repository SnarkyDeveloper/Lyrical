# Lyrical

A Python package to fetch song lyrics from Genius.

## Installation

```bash
pip install lyrical
```

## Info

- **Author:** SnarkyDev
- **Version:** 1.1.2
- **LICENSE:** MIT
- **USE:** Scrapes Genius for lyrics, in an async way

## Usage

```python
from lyrical import Lyrics
import asyncio
import json

lyrical = Lyrics()
async def main():
    song = "Hello world"
    url = await lyrical.search(song)
    lyrics = await lyrical.get_lyrics(url)
    artist = await lyrical.get_artists(url)
    title = await lyrical.get_title(url)
    print(f'Lyrics:\n{lyrics}\nArtists: {artist}\nTitle: {title}')

    overall = await lyrical.lyrics(song)
    print(json.loads(overall))

if __name__ == "__main__":
    asyncio.run(main())
```

### API

```python
import lyrical
import asyncio
lyrics = asyncio.run(lyrical.Lyrics.start_api())
```
