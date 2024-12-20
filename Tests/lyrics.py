import lyrical
import asyncio
import json
lyrics = asyncio.run(lyrical.Lyrics.get_lyrics("Hello World"))
artist = asyncio.run(lyrical.Lyrics.get_artists("https://genius.com/Louie-zong-hello-world-lyrics"))
title = asyncio.run(lyrical.Lyrics.get_title("https://genius.com/Louie-zong-hello-world-lyrics"))
print(f'Lyrics: {lyrics}\nArtists: {artist}\nTitle: {title}')

overall = lyrical.Lyrics.lyrics("Hello World")
print(json.loads(overall))