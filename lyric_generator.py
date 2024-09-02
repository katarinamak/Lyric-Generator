from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
import lyricsgenius as lg
import os

claude_api_key = os.environ["CLAUDE_API_KEY"]
anthropic = Anthropic(api_key=claude_api_key)

# lyrics genius: 

lg_api_key = os.environ["LG_API_KEY"]


def get_lyrics(artist_name, album_name):
    genius = lg.Genius(lg_api_key, skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"], remove_section_headers=True)
    album = genius.search_album(name=album_name, artist=artist_name)
    
    if album is not None:
        tracks = album.tracks

    lyrics = ""
    for track in tracks:
        lyrics += track.to_text()

    print(lyrics)
    return lyrics

def main():
    artist = input("Name an artist: \n")
    album = input("Name their best album: \n")
    print(artist, album)
    context = get_lyrics(artist, album)

    completion = anthropic.completions.create(
        model="claude-2",
        max_tokens_to_sample=100000,
        prompt=f"Human: {context}Assistant:",
    )
    print(completion.completion)

    completion = anthropic.completions.create(
        model="claude-2",
        max_tokens_to_sample=100000,
        prompt=f"""Human: These are the lyrics from all the songs on the album {album}.You are {artist} and you need to write the lyrics for a new song in the same style as the lyrics already on the album {album}. It should be believable that this song really exists on the album. Also generate a song title that sounds fitting. The song should be a length similar to the other songs in the album. Only output the title and the lyrics of the new song, don't print any additional comments. Assistant:""",
    )

    print(completion.completion)

   
    
if __name__ == "__main__":
    main()
