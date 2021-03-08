import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

ALBUMS_INSERT="INSERT INTO albums(album_id, album_name, release_date, artists) VALUES (%s, %s, %s, %s)"
TRACKS_INSERT="INSERT INTO tracks(track_id, track_name, album_id, artists) VALUES (%s, %s, %s, %s)"
ARTISTS_INSERT="INSERT INTO artists(artist_id, artist_name, popularity) VALUES (%s, %s, %s)"

class SpotifyDB:

    def __init__(self):
        """ create tables in the PostgreSQL database"""
        commands = (
            """
            CREATE TABLE albums (
                album_id TEXT PRIMARY KEY,
                album_name VARCHAR(255) NOT NULL,
                release_date TEXT NOT NULL,
                artists TEXT []
            )
            """,
            """ CREATE TABLE tracks (
                    track_id TEXT PRIMARY KEY,
                    track_name VARCHAR(255) NOT NULL,
                    album_id TEXT,
                    artists TEXT [],
                    CONSTRAINT fk_track_album
                        FOREIGN KEY(album_id) 
                            REFERENCES albums(album_id)
                            ON DELETE CASCADE
                    )
            """,
            """
            CREATE TABLE artists (
                    artist_id TEXT PRIMARY KEY,
                    artist_name VARCHAR(100) NOT NULL,
                    popularity INT NOT NULL
            )
            """)
        conn = None
        try:
            # connect to the PostgreSQL server     
            conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="postgres-db", port="5432" )
            cur = conn.cursor()
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # create spotify DB
            cur.execute("DROP DATABASE IF EXISTS spotify")
            cur.execute("CREATE DATABASE spotify")
            # conect to new DB
            conn = psycopg2.connect(database="spotify", user="postgres", password="postgres", host="postgres-db", port="5432" )
            cur = conn.cursor()
            # create tables one by one
            for command in commands:
                cur.execute(command)
            # close communication with the PostgreSQL database server
            cur.close()
            # commit the changes
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def insert_data(self, data, table_name):
        """
            This function iterates over the list of load queries that load the data from
            files in s3 bucket to the stage tables (stg_events, stg_songs) using COPY command.
            INPUTS:
            1. data list of objects of the entity to load (Album, Track, or Artist) 
            2. table_name postgres table name
        """
        conn = None

        try:
            # conect to spotify DB
            conn = psycopg2.connect(database="spotify", user="postgres", password="postgres", host="postgres-db", port="5432" )
            cur = conn.cursor()
            # execute insert stmt
            for d in data:
                if table_name == 'albums':
                    cur.execute(ALBUMS_INSERT, (d.id, d.name, d.release_date, d.artists))
                elif table_name == 'tracks':
                    cur.execute(TRACKS_INSERT, (d.id, d.name, d.album_id, d.artists))
                elif table_name == 'artists':
                    cur.execute(ARTISTS_INSERT, (d.id, d.name, d.popularity))
            # close communication with the PostgreSQL database server
            cur.close()
            # commit the changes
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
