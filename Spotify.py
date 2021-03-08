import requests, json, base64, pandas as pd
from SpotifyEntity import Album, Artist, Track
from SpotifyDB import SpotifyDB

CLIENT_ID = '495855bc7ad34791a164c58be84885d2'
CLIENT_SECRET = '4e02f23a19664f1785a1629cb726642b'

AUTH_URL = 'https://accounts.spotify.com/api/token'
BROWSE_URL="https://api.spotify.com/v1/browse/new-releases"
ALBUMS_URL="https://api.spotify.com/v1/albums"
ARTISTS_URL="https://api.spotify.com/v1/artists"
COUNTRY='US'
MAX_ALBUMS=20
MAX_ARTISTS=50

class Spotify:

    def get_tracks(self, albums_ids, headers):
        """
            This function gets tracks info. using the tracks API
            INPUTS:
                1. albums_ids ids to send to the API as params 
                2. headers used for auth
            OUTPUT:
                tracks_list a list of Track objects
        """
        params={}
        params['ids'] = albums_ids
        # call the API
        album_response = requests.get(ALBUMS_URL, headers=headers, params=params)

        ar = album_response.json()
        albums=ar['albums']
        artists_ids=[]
        tracks_list=[]
        # loop on albums to extract the data
        for i in range(len(albums)):
            album_id = albums[i]['id']
            tracks = albums[i]['tracks']['items']
            # loop on tracks within the album
            for i in range(len(tracks)):
                track_id = tracks[i]['id']
                track_name = tracks[i]['name']
                artists = tracks[i]['artists']
                # loop on artists within the track
                for i in range(len(artists)):
                    artists_ids.append(artists[i]["id"])
                tracks_list.append(Track(track_id, track_name, album_id, artists_ids))
                artists_ids=[]
        
        return tracks_list

    def get_artist(self, ids, headers):
        """
            This function gets artists info. using the artists API
            INPUTS:
                1. ids artists ids to send to the API as params 
                2. headers used for auth
            OUTPUT:
                artists_list a list of Artist objects
        """
        params={}
        params['ids'] = ids
        artists_response = requests.get(ARTISTS_URL, headers=headers, params=params)

        ar = artists_response.json()
        artists = ar['artists']
        artists_list=[]
        for artist in artists:
            # create list of Artist objects
            artists_list.append(Artist(artist['id'], artist['name'], artist['popularity']))
        
        return artists_list


    def get_albums(self, res):
        """
            This function gets new releases for a given country   
            INPUTS:
                1. res API response json object for albums new releases
            OUTPUT:
                albums_list a list of Album objects
        """
        albums = res['albums']['items']
        albums_list=[]
        artists_ids=[]
        for album in albums:
            for i in range(len(album['artists'])):
                artists_ids.append(album['artists'][i]["id"])
            albums_list.append(Album(album['id'], album['name'], album['release_date'], artists_ids))
            artists_ids=[]

        return albums_list

    def get_auth_header(self):
        """
            This function creates headers for authentication
            OUTPUT:
                headers object to use for auth
        """
        # POST
        auth_response = requests.post(AUTH_URL, {
            'grant_type': 'client_credentials',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        })

        # convert the response to JSON
        auth_response_data = auth_response.json()

        # save the access token
        access_token = auth_response_data['access_token']

        headers = {
            'Authorization': 'Bearer {token}'.format(token=access_token)
        }

        return headers

    def load_albums(self, country, headers):
        """
            This function gets new releases for a given country   
            INPUTS:
                1. country code to get new releases for
                2. headers used for uthentication
            OUTPUT:
                albums list of Album objects
        """
        params={}
        params['country'] = country
        # POST
        search_response = requests.get(BROWSE_URL, headers=headers, params=params)

        r = search_response.json()
        next=r['albums']['next']
        albums = self.get_albums(r)

        while next:
            next_response = requests.get(next, headers=headers)
            nr = next_response.json()
            next=nr['albums']['next']
            albums.extend(self.get_albums(nr))

        return albums

    def load_tracks(self, albums, headers):
        """
            This function gets tracks list for all given albums  
            INPUTS:
                1. albums list of album objects
                2. headers used for uthentication
            OUTPUT:
                tracks list of Track objects
        """
        no_of_albums=0
        albums_id=""
        tracks=[]
        for i in range(len(albums)):
            if albums_id=="":
                albums_id += albums[i].id
            else:
                albums_id += "," + albums[i].id
            no_of_albums+=1
            if no_of_albums == MAX_ALBUMS or no_of_albums == len(albums):
                # call the tracks API for a number of tracks based on the max allowed ids
                tracks.extend(self.get_tracks(albums_id, headers))
                no_of_albums=0
                albums_id=""
        
        return tracks


    def load_artists(self, tracks, headers):
        """
            This function gets artists list for all given tracks  
            INPUTS:
                1. tracks list of tracks objects
                2. headers used for uthentication
            OUTPUT:
                artists list of Artist objects
        """
        no_of_artists=0
        artist_id=""
        artists_id=[]
        artists=[]
        for i in range(len(tracks)):
            artists_id.extend(tracks[i].artists)
        
        # remove duplicate artists ids
        artists_id = list( dict.fromkeys(artists_id) )

        for i in range(len(artists_id)):
            if artist_id=="":
                artist_id += artists_id[i]
            else:
                artist_id += "," + artists_id[i]
            no_of_artists+=1
            if no_of_artists == MAX_ARTISTS or no_of_artists == len(artists):
                # call the artists API for a number of artists based on the max allowed ids
                artists.extend(self.get_artist(artist_id, headers))
                no_of_artists=0
                artist_id=""
        
        return artists

    def __init__(self, country):
        """
            This func is the Spotify class entry point
            INPUTS:
                1. country the country code to get albums for
        """
        # authenticate
        headers = self.get_auth_header()
        # get new releases for the input country
        albums = self.load_albums(country, headers)
        print(albums[0].id)
        # get tracks in each album
        tracks = self.load_tracks(albums, headers)
        print(tracks[0].id)
        # get artists from all tracks
        artists = self.load_artists(tracks, headers)
        print(artists[0].id)
        # load data into postgres DB
        spotify_db = SpotifyDB()
        spotify_db.insert_data(albums, "albums")
        spotify_db.insert_data(tracks, "tracks")
        spotify_db.insert_data(artists, "artists")
