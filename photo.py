import face_recognition
import cv2
import eel
import base64
import pickle
import imutils
import os
import datetime
import time
from multiprocessing.pool import ThreadPool
#import mysql.connector
#import MySQLdb
from database import *

def recogFace(data,encoding):
	return face_recognition.compare_faces(data["encodings"], encoding, tolerance=0.5)

def recogEncodings(rgb,boxes):
	return face_recognition.face_encodings(rgb, boxes)

def recogLoc(rgb):
	return face_recognition.face_locations(rgb, model = "hog")

def recognizeFromPhoto(img, student_class):
	pool1 = ThreadPool(processes = 1)
	pool2 = ThreadPool(processes = 2)
	pool3 = ThreadPool(processes = 3)
	#print('.......class...')
	#print(student_class)
	#print('...............')
	# Load the known faces ids
	conn = create_connection()
	cursor = conn.cursor()
	sql = "SELECT student_id FROM student_data WHERE class =?"
	val =[student_class]
	cursor.execute(sql,val)
	student_data = cursor.fetchall()

    # Load the known face and encodings
	#print("[INFO] loading encodings ..")
	data = pickle.loads(open("encodings.pickle","rb").read())

	#inititlise the camera
	#cap = cv2.VideoCapture('http:192.168.0.2:4747/video')
	#time.sleep(2.0)

	encodings = []
	boxes = []
	Attendees_Names = {}
	frame = 0
	#start the videocapture
	#img = cv2.imread('group2.jpg')
	#Convert the BGR to RGB
	# a width of 750px (to speed up processing)
	rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	rgb = imutils.resize(img, width = 750)
	r = img.shape[1]/float(rgb.shape[1])

	#detect boxes
	if(frame%5 == 0):
		boxes = pool1.apply_async(recogLoc,(rgb,)).get()
		encodings = pool3.apply_async(recogEncodings,(rgb,boxes,)).get()
	names = []
		
	# loop over the facial encodings
	for encoding in encodings :
		matches = pool2.apply_async(recogFace,(data,encoding,)).get()
		name = "Unkown"

		# check to see if we have found a match
		if True in matches:
			#find the indexes of all matched faces then initialize a 
			# dicationary to count the total number of times each face matched
			matchedIds = [i for (i,b) in enumerate(matches) if b]
			counts ={}

			#loop over the recognized faces
			for i in matchedIds:
				name = data["names"][i]
				counts[name] = counts.get(name,0)+1

			#determine the recognized faces with largest number
			# of votes (note: in the event of an unlikely tie Python will select first entry in the dictionary)
			name = max(counts , key = counts.get)
			if(name not in Attendees_Names):
				Attendees_Names[name]= 1
				#print(name)
				#print('........student........')
				#print(student_data)
				for y in student_data:
					#print(y)
					if name in y:
						#print('find success')
						x = datetime.datetime.now()
						date = str(x.day)+"-"+str(x.month)+"-"+str(x.year)
						submit_photo_attendance(name,student_class,date)
						eel.updateAttendance(name)()

		names.append(name)


	# loop over recognized faces
	for ((top,right,bottom,left),name)in zip(boxes, names):
		top = int(top*r)
		right = int(right*r)
		bottom = int(bottom*r)
		left = int(left *r)
		# draw the predicted face name on the image
		cv2.rectangle(img, (left, top), (right, bottom),
				(0, 255, 0), 5)
		y = top - 15 if top - 15 > 15 else top + 15
		cv2.putText(img, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
				1, (0, 255, 0), 5)
	retval, buffer = cv2.imencode('.jpg', img)
	jpg_as_text = base64.b64encode(buffer)
	#cap.release()
	photo_string = "data:image/png;base64, " + jpg_as_text
	##print(photo_string)
	eel.updatePhotoAttendance(photo_string)
def submit_photo_attendance(student_id,student_class,date):
	attendance_class={
        "xii" : "INSERT INTO xii(student_id,attendance_date) VALUES(?, ?);",
        "xi"  : "INSERT INTO xi(student_id,attendance_date) VALUES(?, ?);",
    }
	conn = create_connection()
	cursor = conn.cursor()
	sql = attendance_class[student_class]
	val = [student_id, date]
	cursor.execute(sql, val)
	conn.commit()
	conn.close()
