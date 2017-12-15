# Import statements necessary
from flask import Flask, render_template
from flask_script import Manager
from config import *
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

# cur.execute("""INSERT INTO
#     album_table(collectionId, collectionName, price, link, genre)
#     values(113, 'cjdh', 112, 'ajhdh', 'ljede')
#     on conflict do nothing""")

# cur.execute("""INSERT INTO
#     album_table(collectionId, collectionName, price, link, genre)
#     values(114, 'cjdh', 112, 'ajhdh', 'ljede')
#     on conflict do nothing""")

# cur.execute("""INSERT INTO
#     album_table(collectionId, collectionName, price, link, genre)
#     values(115, 'cjdh', 112, 'ajhdh', 'ljede')
#     on conflict do nothing""")

# cur.execute("""INSERT INTO
#     album_table(collectionId, collectionName, price, link, genre)
#     values(116, 'cjdh', 112, 'ajhdh', 'ljede')
#     on conflict do nothing""")

conn.commit()

# def execute_and_print(query, numer_of_results=30):
#     cur.execute(query)
#     results = cur.fetchall()
#     for r in results[:numer_of_results]:
#         #print(type(r))
#         print(r)
#     print('--> Result Rows:', len(results))

# cur.execute('select * from "Albums"')
# results = cur.fetchall()

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
    # cur.execute("""select "artistname", "artistid" from "artist_table" where lower("artistname") like lower('%coldplay%')""")
    # results = cur.fetchall()

#     cur.execute("""select "artistname", "artistid" from "artist_table" where lower("artistname") like lower('%coldplay%')""")
    
# print('==> Get Name, AlbumTitle of all tracks if Name contains fast or Fast')
# execute_and_print("""select "Name", "Title" as "AlbumTitle"
#     from "Track" INNER JOIN "Album" ON ("Track"."AlbumId" = "Album"."AlbumId")
#     where "Name" ilike '%fast%' """, 5)

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
    genreList = {}
    albums = []

    for i in range(len(itunes_data['results'])):
        # try:
        albums.append({
            "name" : itunes_data['results'][i]['collectionName'] if 'collectionName' in itunes_data['results'][i].keys() else itunes_data['results'][i]['collectionname'],
            "img" : itunes_data['results'][i]['artworkUrl100'] if 'artworkUrl100' in itunes_data['results'][i].keys() else itunes_data['results'][i]['albumart'],
            "price" : itunes_data['results'][i]['collectionPrice'] if 'collectionPrice' in itunes_data['results'][i].keys() else itunes_data['results'][i]['price'],
            "link" : itunes_data['results'][i]['collectionViewUrl'] if 'collectionViewUrl' in itunes_data['results'][i].keys() else itunes_data['results'][i]['link']

            })

        albumDetails = {}

        print(itunes_data['results'][i])
        
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

    return render_template('albums.html', list=albums, bubble = genreCount)

@app.route('/user/<yourname>')
def hello_name(yourname):
    return '<h1>Hello {}</h1>'.format(yourname)

@app.route('/showvalues/<name>')
def basic_values_list(name):
    lst = ["hello","goodbye","tomorrow","many","words","jabberwocky"]
    if len(name) > 3:
        longname = name
        shortname = None
    else:
        longname = None
        shortname = name
    return render_template('values.html',word_list=lst,long_name=longname,short_name=shortname)


## PART 1: Add another route /word/<new_word> as the instructions describe.


## PART 2: Edit the following route so that the photo_tags.html template will render
@app.route('/flickrphotos/<tag>/<num>')
def photo_titles(tag, num):
    # HINT: Trying out the flickr accessing code in another file and seeing what data you get will help debug what you need to add and send to the template!
    # HINT 2: This is almost all the same kind of nested data investigation you've done before!
    FLICKR_KEY = "" # TODO: fill in a flickr key
    baseurl = 'https://api.flickr.com/services/rest/'
    params = {}
    params['api_key'] = FLICKR_KEY
    params['method'] = 'flickr.photos.search'
    params['format'] = 'json'
    params['tag_mode'] = 'all'
    params['per_page'] = num
    params['tags'] = tag
    response_obj = requests.get(baseurl, params=params)
    trimmed_text = response_obj.text[14:-1]
    flickr_data = json.loads(trimmed_text)
    # TODO: Add some code here that processes flickr_data in some way to get what you nested
    # TODO: Edit the invocation to render_template to send the data you need
    return render_template('photo_tags.html')




if __name__ == '__main__':
    manager.run() # Runs the flask server in a special way that makes it nice to debug
