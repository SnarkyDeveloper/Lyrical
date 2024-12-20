import lyrical
import asyncio
import json
url = asyncio.run(lyrical.Lyrics.search("Hello World"))
lyrics = asyncio.run(lyrical.Lyrics.get_lyrics(url))
artist = asyncio.run(lyrical.Lyrics.get_artists(url))
title = asyncio.run(lyrical.Lyrics.get_title(url))
print(f'Lyrics: {lyrics}\nArtists: {artist}\nTitle: {title}')

overall = asyncio.run(lyrical.Lyrics.lyrics("Hello World"))
print(json.loads(overall))