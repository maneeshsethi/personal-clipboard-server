import sys
import psycopg2

host='xxx'
dbname='xxx'
user='xxx'
password='xxx'

conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password)

# create a cursor
cur = conn.cursor()

# execute a statement
print('PostgreSQL database version:')
cur.execute('SELECT version()')

# display the PostgreSQL database server version
db_version = cur.fetchone()
print(db_version)

#used this to create the table: cur.execute('CREATE table clips(id SERIAL PRIMARY KEY, data TEXT)')

cur.execute('select data from clips ORDER BY id DESC limit 1')
recent_clip = cur.fetchone()
print("Your most recent clip was: {}".format(recent_clip))

#for line in sys.stdin:
cur.execute("INSERT INTO clips (data) VALUES (%s)",(sys.stdin.read(),))
conn.commit()
    #sys.stdout.write(line)

# close the communication with the PostgreSQL
cur.close()

if conn is not None:
        conn.close()
        print('Database connection closed.')
