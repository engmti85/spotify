from flask import Flask, request
import psycopg2
from Spotify import Spotify

app = Flask(__name__)


def get_top10_popular_artists():
    """
        This function gets the top10 artists according to popularity from the artists table in postgres db
        OUTPUT:
            results list of tuples with artist name and popularity
    """
    results=[]
    try:
        conn = psycopg2.connect(database="spotify", user="postgres", password="postgres", host="postgres-db", port="5432" )
        # conect to spotify DB
        cur = conn.cursor()
        # create table one by one
        cur.execute("select artist_name, popularity from artists order by popularity desc limit 10")
        results = cur.fetchall()
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    return results

def get_tracks_by_artist(artist_name):
    """
        This function gets all tracks for an artist from tracks and artists tables in postgres db
        OUTPUT:
            results list of tuples with track name and artist name
    """
    results=[]
    try:
        conn = psycopg2.connect(database="spotify", user="postgres", password="postgres", host="postgres-db", port="5432" )
        # conect to spotify DB
        cur = conn.cursor()
        # create table one by one
        cur.execute(""" SELECT 
                            track_name, 
                            artist_name 
                        from 
                            artists a,
                            tracks t, 	
                            unnest(t.artists) ar 
                        where 
                            a.artist_id = ar 
                        and artist_name = '{}'
                    """.format(artist_name))
        results = cur.fetchall()
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        self.conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    return results

@app.route('/top10', methods=['GET'])
def top10():
    """
        Routing to get top10 funtion
    """
    artists = get_top10_popular_artists()
    results=''
    for i in range(len(artists)):
        results+=str(artists[i])+"\n\r"
    return f'{results}\n'

@app.route('/load', methods=['GET'])
def load():
    """
        initiate Spotify class object to create the spotify postgres db and load spotify data to it
    """
    country = request.args.get('country', 'US')
    try:
        spotify = Spotify(country)
    except Exception as e:
        print(e)
    
    return f'New releases for {country} loaded!\n'

@app.route('/')
def hello():
    return f'Spotify-App!\n'

@app.route('/tracks', methods=['GET'])
def tracks():
    """
        Routing to get tracks funtion
    """
    artist = request.args.get('artist', 'Drake')
    tracks = get_tracks_by_artist(artist)
    results=''
    for i in range(len(tracks)):
        results+=str(tracks[i])+"\n\r"
    return f'{results}\n'

if __name__ == '__main__':
    # Used to run locally only.
    app.run(debug=True, host='0.0.0.0')