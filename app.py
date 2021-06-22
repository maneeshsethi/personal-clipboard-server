from flask import Flask
from flask_restful import Resource, Api, reqparse
import sys
import json
import psycopg2
import creds

app = Flask(__name__)
api = Api(app)
CLIPS = {}
if __name__ == "__main__":
      app.run(debug=True)

CLIPS = {
    '1': {'clip': 'Hiya! This is your first default clip.'}
}

conn = psycopg2.connect(host=creds.host, dbname=creds.dbname, user=creds.user, password=creds.password)

# create a cursor
cur = conn.cursor()

#used this to create the table: cur.execute('CREATE table clips(id SERIAL PRIMARY KEY, data TEXT)')


parser = reqparse.RequestParser()


@app.route('/')
def hello_world():
        return 'Hello, World!'


@app.route('/get_db')
def get_from_db():
    clipcount=10
    cur.execute("SELECT * FROM (SELECT * FROM clips ORDER BY id DESC LIMIT {}) as foo ORDER BY id ASC;".format(clipcount))
    return json.dumps(cur.fetchall())

class ClipsList(Resource):
    def get(self):
        return CLIPS

    def post(self):
      parser.add_argument("clip")
      parser.add_argument("user_id")
      parser.add_argument("ip")
      args = parser.parse_args()
      clip_id = int(max(CLIPS.keys())) + 1
      clip_id = '%i' % clip_id
      CLIPS[clip_id] = {
        "clip": args["clip"],
        "user_id": args["user_id"],
        "ip": args["ip"],
      }


      cur.execute('select clip from clips ORDER BY id DESC limit 1')
      recent_clip = cur.fetchone()
      print("Your most recent clip was: {}".format(recent_clip))

      #for line in sys.stdin:
      cur.execute("INSERT INTO clips (clip) VALUES (%s)",(args["clip"],))
      conn.commit()
      #sys.stdout.write(line)

      return CLIPS[clip_id], 201
  
api.add_resource(ClipsList, '/clips/')

