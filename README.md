# Spotify API with Postgres

## Introduction

This is a task for using Spotify API to retrieve new releases (albums) for a given country, extract all tracks in those albums,
and get all artists in those tracks. Then, store all this data in a postgres DB.
This app is packaged and deployed using Docker.

## Getting Started

### Prerequisites

Prerequisites for running the project:
1. Have docker installed

## Project structure
Here is a list of the project files:

1. README.md this file, provides an overview of the task.
2. SpotifyEntity.py class file containing objects Spotify objects (Album, Track, and Artist) 
3. Spotify.py class file used for calling the API, extracting, transforming, and loading the data into the DB 
4. SpotifyDB.py class file for connecting to the DB to create the spotify DB and tables
5. SpotifyEndpoint.py the main entry for the application and contains the Flask set-up and methods
6. requirements.txt contains the packages required for the containers/app to run
7. spotify-app.yaml docker compose file to build the containers (Postgres and Spotify app)
8. Dockerfile used for packaging the spotify application to a docker image

## Execution Steps
To deploy the app run the below locally on a machine with Docker installed

```
docker-compose -f {YOUR_PATH}/spotify-app.yaml up
```

to stop and remove the containers execue 

```
docker-compose -f {YOUR_PATH}/spotify-app.yaml down
```

## Testing
After the docker container is launched and to test the app, open a web browser and follow these steps:
1. navigate to http://localhost:5000/ (this should print Spotify App)
2. navigate to http://localhost:5000/load?country=COUNTRY_CODE (replace country code with the country you want to get new releases for e.g. US, CA, EG,...etc), will default to US if left empty. Wait till you get "New releases for {country_code} loaded!" message
3. navigate to http://localhost:5000/top10 to get a list of top 10 popular artists
4. navigate to http://localhost:5000/tracks?artist=ARTIST_NAME (replace artist name with the singer's name to get all his/her loaded tracks), this defaults to "Drake" although I don't like his songs :)

## Spotify postgres tables

### Albums Table
```
album_id   ----PK
album_name 
release_date
artists    ----list of artists ids 
```

### Albums Table
```
album_id   ----PK
album_name 
release_date
artists    ----list of artists ids 
```

### Tracks Table
```
track_id   ----PK
track_name 
album_id
artists    ----list of artists ids 
```

### Artist Table
```
artist_id   ----PK
artist_name 
popularity
```

## No covered 
Some aspects are not covered in this task:
1. Logging 
2. Proper Exception handeling
3. Data Modeling 