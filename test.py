import pickle
import base64
from database import *
import cPickle
face_data = pickle.loads(open("encodings.pickle","a+").read())

face_data = cPickle.dumps(face_data, cPickle.HIGHEST_PROTOCOL)

conn = create_connection()
cursor = conn.cursor()

cursor.execute("insert into face_data(data) values (%s)", sqlite3.Binary(face_data))


conn.commit()
conn.close()
"""
face_data = open("encodings.pickle","a+").read()
print(face_data)
index = []
encodings = face_data['encodings']
names    = face_data['names']
"""