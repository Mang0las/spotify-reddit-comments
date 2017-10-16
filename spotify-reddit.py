from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import praw


# Authentication stuff for Spotify
client_credentials_manager = SpotifyClientCredentials(
    client_id='INSERT CLIENT ID',
    client_secret='INSERT CLIENT SECRET')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Authentication stuff for Reddit
reddit = praw.Reddit(
    user_agent='Comment Extraction',
    client_id='INSERT CLIENT ID', client_secret='INSERT CLIENT SECRET')


uri = 'spotify:user:mang0las:playlist:7BuuFjN1FaWAOFaCnblgb1'  # Insert the URI of a playlist
username = uri.split(':')[2]                                   # (My placeholder playlist)
playlist_id = uri.split(':')[4]
artists_list = []

submission = reddit.submission(id='1jpy7e') # Insert ID of a submission
submission.comments.replace_more(limit=0)  # Stores all the comments
comments = submission.comments.list()


def show_tracks(tracks):
    # Adds all the artists from one page to a list
    for item in tracks['items']:
        track = item['track']['artists'][0]['name']
        if track not in artists_list:
            artists_list.append(track)


def display_artists():
    # Cycles through every page in a playlist
    results = sp.user_playlist(username, playlist_id, fields="tracks,next")
    tracks = results['tracks']
    show_tracks(tracks)
    while tracks['next']:
        tracks = sp.next(tracks)
        show_tracks(tracks)


display_artists()
artists_list.sort(key=lambda s: s.lower()) # sorts the list alphabetically ignoring case
artists_list = list(filter(None, artists_list)) # filters empty entries

# Very basic list of matches, could do with better formatting
f = open('matches.html', 'w')
for comment in comments:
    for artist in artists_list:
        if artist.lower() in comment.body.lower():
            f.write('<a href="https://reddit.com' + comment.permalink() + '">' + artist + '</a>' + '<br>')


f.close()
