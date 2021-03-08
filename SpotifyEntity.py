class Album:
    # Album object
    def __init__(self, id, name, release_date, artists):
        self.id = id
        self.name = name
        self.release_date = release_date
        self.artists = artists

class Track:
    # Track object
    def __init__(self, id, name, album_id, artists):
        self.id = id
        self.name = name
        self.album_id = album_id
        self.artists = artists

class Artist:
    # Artist object
    def __init__(self, id, name, popularity):
        self.id = id
        self.name = name
        self.popularity = popularity