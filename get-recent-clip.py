import sys
import psycopg2
import os
import creds


host=creds.host
dbname=creds.dbname
user=creds.user
password=creds.password

conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password)

# create a cursor
cur = conn.cursor()

#if rows_back is 1, you'll get the most recent entry. If it's two, you'll get the second most recent. And so on.
rows_back = 1

#used this to create the table: cur.execute('CREATE table clips(id SERIAL PRIMARY KEY, data TEXT)')
if (rows_back == 1):
    cur.execute('select * from clips ORDER BY id DESC limit 1')
else:
    cur.execute("SELECT * FROM (SELECT * FROM clips ORDER BY id DESC LIMIT {}) as foo ORDER BY id ASC;".format(rows_back))

recent_clip_record = cur.fetchone()
recent_clip = recent_clip_record[1]
#print(recent_clip)
#print("Your most recent clip was: {}".format(recent_clip))
recent_clip.replace('"','\"')
#print("x_clip=$'{}'".format(recent_clip))
#os.system("x_clip=\"{}\";".format(recent_clip))

with open("lastclip.txt", "w") as text_file:
    text_file.write(recent_clip)
os.system("cat lastclip.txt | clipboard")
#os.system("printf '%s\n' \"$x_clip\" | clipboard")
    #$'{}'printf '{}' | clipboard".format((recent_clip)))}


# close the communication with the PostgreSQL
cur.close()

if conn is not None:
        conn.close()
        print('Database connection closed.')

