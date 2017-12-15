# Import statements necessary
from flask import Flask, render_template
from flask_script import Manager
from config import *
from bs4 import BeautifulSoup
import psycopg2
import psycopg2.extras
import requests 
import json
import sys

def get_connection_and_cursor():
    global db_connection, db_cursor
    try:
        if db_password != "":
            db_connection = psycopg2.connect("dbname='{0}' user='{1}' password='{2}'".format(db_name, db_user, db_password))
            print("Success connecting to database")
        else:
            db_connection = psycopg2.connect("dbname='{0}' user='{1}'".format(db_name, db_user))
    except:
        print("Unable to connect to the database. Check server and credentials.")
        sys.exit(1) # Stop running program if there's no db connection.

    db_cursor = db_connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    return db_connection, db_cursor

conn, cur = get_connection_and_cursor()

def create_db():
    cur.execute("""CREATE TABLE IF NOT EXISTS album_table (
        collectionId INTEGER PRIMARY KEY,
        artistId NUMERIC,
        collectionName VARCHAR(255) NOT NULL,
        price NUMERIC,
        link VARCHAR(255),
        genre VARCHAR(128),
        albumart VARCHAR(255)

    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS artist_table (
        artistId NUMERIC PRIMARY KEY,
        artistName VARCHAR(255) NOT NULL
    )""")

    conn.commit()

create_db()


conn.commit()


conn.commit()

# Set up application
app = Flask(__name__)

manager = Manager(app)

# Routes

PRICE_LIMIT = 8

class Album():
    """
    This object is responsible for saving the album info in the database
    """
    def __init__(self, details):
        name = details['name']
        price = details['price']
        link = details['link']
        genre = details['genre']
        artistId = details['artistId']
        collectionId = details['collectionId']


        cur.execute("""INSERT INTO
            album_table(collectionId, artistId, collectionName, price, link, genre, albumart)
            values(%(collectionId)s, %(artistId)s, %(name)s, %(price)s, %(link)s, %(genre)s, %(albumart)s)
            on conflict do nothing""", details)

        conn.commit()


    def __str__(self, details):
        if int(self.price) > PRICE_LIMIT:
            return "Album " + self.name + " is available for $" + self.price
        else:
            return "Album " + self.name + " is available for only $" + self.price


class Artist():
    """
    This object is responsible for saving the album info in the database
    """
    def __init__(self, details):
        artistId = details['artistId']


        cur.execute("""INSERT INTO
            artist_table(artistId, artistName)
            values(%(artistId)s, %(artistName)s)
            on conflict do nothing""", details)

        conn.commit()


    def __str__(self, details):
        if int(self.price) > PRICE_LIMIT:
            return "Album " + self.name + " is available for $" + self.price
        else:
            return "Album " + self.name + " is available for only $" + self.price

def getArtistInfo(name):
    print(name)
    discogs_params = {}
    discogs_params['type'] = "all"
    discogs_params['q'] = name
    catData = requests.get("https://www.discogs.com/search", params = discogs_params).text
    catSoup = BeautifulSoup(catData, 'html.parser')

    href = catSoup.select('#search_results div.shortcut_navigable a.thumbnail_link')[0]['href']

    print(href)

    artData =  requests.get("https://www.discogs.com" + href).text
    artSoup = BeautifulSoup(artData, 'html.parser')

    mainImage = artSoup.select('.body .thumbnail_center img')[0]['src']

    return mainImage
    



@app.route('/')
def hello_world():
    cur.execute('select "artistname" from "artist_table"')
    results = cur.fetchall()
    suggestion = []
    for r in range(len(results)):
        suggestion.append(results[r]['artistname'])
    return render_template('start.html', list=suggestion)

@app.route('/artist/<name>')
def hello_artist(name):

    #check if artist exists in DB

    cur.execute("""select * from "album_table" INNER JOIN "artist_table" ON ("album_table"."artistid" = "artist_table"."artistid") 
        where lower("artistname") like lower('%""" + name + """%') OR lower("collectionname") like lower('%""" + name + """%') """)

    itunes_data = {}
    itunes_data['results'] = cur.fetchall()

    if(len(itunes_data['results']) == 0):
        baseurl = 'https://itunes.apple.com/search?'
        params = {}
        params['term'] = name
        params['limit'] = '300'
        params['entity'] = 'album'
        response_obj = requests.get(baseurl, params=params)

        itunes_data = json.loads(response_obj.text)

    try:
        mainImage = getArtistInfo(name)
    except:
        mainImage = ''
    genreList = {}
    albums = []

    for i in range(len(itunes_data['results'])):
        # try:
        data = {
            "name" : itunes_data['results'][i]['collectionName'] if 'collectionName' in itunes_data['results'][i].keys() else itunes_data['results'][i]['collectionname'],
            "img" : itunes_data['results'][i]['artworkUrl100'] if 'artworkUrl100' in itunes_data['results'][i].keys() else itunes_data['results'][i]['albumart'],
            "link" : itunes_data['results'][i]['collectionViewUrl'] if 'collectionViewUrl' in itunes_data['results'][i].keys() else itunes_data['results'][i]['link']
            }

        try:
            data['price'] = itunes_data['results'][i]['collectionPrice'] if 'collectionPrice' in itunes_data['results'][i].keys() else itunes_data['results'][i]['price']
        except:
            data['price'] = 0 
        
        albums.append(data)

        albumDetails = {}
        
        albumDetails['name'] = itunes_data['results'][i]['collectionName'] if 'collectionName' in itunes_data['results'][i].keys() else itunes_data['results'][i]['collectionname']
        albumDetails['genre'] = itunes_data['results'][i]['primaryGenreName'] if 'primaryGenreName' in itunes_data['results'][i].keys() else itunes_data['results'][i]['genre']
        albumDetails['link'] = itunes_data['results'][i]['collectionViewUrl'] if 'collectionViewUrl' in itunes_data['results'][i].keys() else itunes_data['results'][i]['link']
        albumDetails['collectionId'] = itunes_data['results'][i]['collectionId'] if 'collectionId' in itunes_data['results'][i].keys() else itunes_data['results'][i]['collectionid']
        albumDetails['artistName'] = itunes_data['results'][i]['artistName'] if 'artistName' in itunes_data['results'][i].keys() else itunes_data['results'][i]['artistname']
        albumDetails['albumart'] = itunes_data['results'][i]['artworkUrl100'] if 'artworkUrl100' in itunes_data['results'][i].keys() else itunes_data['results'][i]['albumart']
        try:
            albumDetails['price'] = itunes_data['results'][i]['collectionPrice'] if 'collectionPrice' in itunes_data['results'][i].keys() else itunes_data['results'][i]['price']
        except:
            albumDetails['price'] = 0
        albumDetails['artistId'] = itunes_data['results'][i]['artistId'] if 'artistId' in itunes_data['results'][i].keys() else itunes_data['results'][i]['artistid']

        alb = Album(albumDetails)
        art = Artist(albumDetails)

        genre = albumDetails['genre']
        if genre in dict.keys(genreList):
            genreList[genre] = genreList[genre] + 1
        else:
            genreList[genre] = 1;

        # except:
        #     albums.append(i)


    genreCount = ''
    for key, value in genreList.items():
        genreCount = genreCount + json.dumps({'name': key, 'value': int(value), 'group': 'group 1'}) + '~~'

    return render_template('albums.html', list=albums, bubble = genreCount, img=mainImage)


if __name__ == '__main__':
    manager.run() # Runs the flask server in a special way that makes it nice to debug
