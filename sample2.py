import psycopg2
import psycopg2.extras
from config import *

def get_connection_and_cursor():
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

# All columns
#print('==> Get all columns of all tracks')
cur.execute('select * from "Track"')
results = cur.fetchall()
#<class 'psycopg2.extras.RealDictRow'>
#print(results[0]['Name'])
#print('--> Result Rows:', len(results))
#print()

def execute_and_print(query, numer_of_results=30):
    cur.execute(query)
    results = cur.fetchall()
    for r in results[:numer_of_results]:
        #print(type(r))
        print(r)
    print('--> Result Rows:', len(results))
    print()

# Single column

#print('==> Get names of all tracks')
#execute_and_print('select "Name" from "Track"',3)

# Multiple columns
print('==> Get Name, AlbumId of all tracks')
execute_and_print('select "Name", "ArtistId" from "Artist"')
'''
# Multiple columns conditional using equals operator
print('==> Get Name and AlbumId of all tracks with AlbumId 3')
execute_and_print('select "Name", "AlbumId" from "Track" where "AlbumId"=3')
'''
'''
# Multiple columns conditional using comparison operator
print('==> Get Name and AlbumId of all tracks with AlbumId upto 5')
execute_and_print('select "Name", "AlbumId" from "Track" where "AlbumId"<=5')
'''
'''
# Multiple columns conditional using 'in' operator
print('==> Get Name and AlbumId of all tracks with AlbumId 3, 5, and 7')
execute_and_print('select "Name", "AlbumId" from "Track" where "AlbumId" in (3, 5, 7)')
'''
'''
# Multiple columns conditional like
print('==> Get Name and AlbumId of all tracks if Name contains fast')
execute_and_print("""select "Name", "AlbumId" from "Track" where "Name" like '%fast%'""")

'''
'''
# Multiple columns conditional case insensitive like
print('==> Get Name and AlbumId of all tracks if Name contains fast or Fast')
execute_and_print("""select "Name", "AlbumId" from "Track" where "Name" ilike '%fast%'""")

'''
'''
# get count of Tracks
print('==> Get count of all tracks using *')
execute_and_print(""" select count(*) from "Track" where "Name" like '%fast%'""")
'''
'''
# Difference between count(*), count("TrackId"), count("Composer")
print('==> Get count of all tracks using TrackId')
execute_and_print(""" select count("TrackId") from "Track" """)
'''
'''
print('==> Get count of all tracks using Composer')
execute_and_print(""" select count("Composer") from "Track" """)
'''
'''
# get count of Tracks conditional
print('==> Get count of all tracks with AlbumId 3')
execute_and_print(""" select count(*) from "Track" where "AlbumId"=3""")
'''
'''
# AVG
print('==> Get average playtime of all tracks')
execute_and_print(""" select "Milliseconds" from "Track" """)
'''
'''
# AVG in minutes
print('==> Get average playtime in minutes of all tracks')
execute_and_print(""" select avg("Milliseconds") / 60000.0 as "Minutess" from "Track" """)
'''
'''
# AVG conditional
print('==> Get average playtime of all tracks with AlbumId 3')
execute_and_print(""" select avg("Milliseconds") from "Track" where "AlbumId"=3 """)
'''
'''
# GROUP BY
print('==> Get average playtime of all tracks for each Album')
execute_and_print(""" select "AlbumId", avg("Milliseconds") from "Track" group by "AlbumId" """)
'''
# GROUP BY conditional
print('==> Get average playtime of all tracks for each Album and having avg playtime upto 5 minutes')
execute_and_print(""" select "AlbumId", (avg("Milliseconds") / 60000.0) as "Minutes"
    from "Track" group by "AlbumId" having (avg("Milliseconds") / 60000.0) <= 4 """, 5)
'''
# ORDER BY
print('==> Get average playtime of all tracks for each Album and order them by AlbumId')
execute_and_print(""" select "AlbumId", avg("Milliseconds") from "Track"
    group by "AlbumId" order by "AlbumId" """, 5)

# ORDER BY DESC
print('==> Get Name, AlbumId of all tracks and sort them by Name in descending order')
execute_and_print('select "Name", "AlbumId" from "Track" order by "Name" desc', 5)

# ORDER BY Multiple
print('==> Get Name, AlbumId of all tracks and sort them by AlbumId, and then by Name')
execute_and_print('select "Name", "AlbumId" from "Track" order by "AlbumId", "Name"', 5)

# ORDER BY Multiple different orders
print('==> Get Name, AlbumId of all tracks and sort them by AlbumId, and then by Name in descending order')
execute_and_print('select "Name", "AlbumId" from "Track" order by "AlbumId", "Name" desc', 5)

# INNER JOIN ON condition
print('==> Get Name, AlbumTitle of all tracks')
execute_and_print("""select "Name", "Title" as "AlbumTitle"
    from "Track" INNER JOIN "Album" ON ("Track"."AlbumId" = "Album"."AlbumId") """)

# INNER JOIN ON condition with filter conditions
print('==> Get Name, AlbumTitle of all tracks if Name contains fast or Fast')
execute_and_print("""select "Name", "Title" as "AlbumTitle"
    from "Track" INNER JOIN "Album" ON ("Track"."AlbumId" = "Album"."AlbumId")
    where "Name" ilike '%fast%' """, 5)

# INNER JOIN ON condition with group by
print('==> Get AlbumTitle, count of all tracks per AlbumTitle')
execute_and_print("""select "Title" as "AlbumTitle", count(*)
    from "Track" INNER JOIN "Album" ON ("Track"."AlbumId" = "Album"."AlbumId")
    group by "Title" order by "Title" """, 5)

# INNER JOIN ON condition with group by and conditional
print('==> Get AlbumTitle, count of all tracks per AlbumTitle containing more than 20 tracks')
execute_and_print("""select "Title" as "AlbumTitle", count(*)
    from "Track" INNER JOIN "Album" ON ("Track"."AlbumId" = "Album"."AlbumId")
    group by "Title" having count(*) > 20 """, 5)

# Subquery as a column
print('==> Get Name, AlbumTitle of all tracks using Subquery')
execute_and_print("""select "Name", (select "Title" from "Album" where "Album"."AlbumId"="Track"."AlbumId")
    from "Track" """, 5)

# Subquery as a column with filter condition
print('==> Get Name, AlbumTitle of all tracks using Subquery if Name contains fast or Fast')
execute_and_print("""select "Name", (select "Title" from "Album" where "Album"."AlbumId"="Track"."AlbumId")
    from "Track"  where "Name" ilike '%fast%' """, 5)

# Subquery as a where condition
print('==> Get Name, AlbumId of all tracks if Album Title is Iron Maiden (using subquery and case insensitive)')
execute_and_print("""select "Name", "AlbumId" from "Track"  where
    "AlbumId" = (select "AlbumId" from "Album" where "Title" = 'Iron Maiden') """, 5)
'''
