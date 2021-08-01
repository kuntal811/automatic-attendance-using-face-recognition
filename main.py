import eel
import cv2
import io
import numpy as np
import base64
import os
import time
import face_recognition
import pickle
import imutils
import datetime
from multiprocessing.pool import ThreadPool
import random
import shutil

from database import *
from camera import VideoCamera
from SceneChangeDetect import sceneChangeDetect
import photo
import login
import encode_student_data
import warnings
warnings.filterwarnings('ignore')

eel.init('web')

"""
def recognizeFromPhoto(image):
	#cap = cv2.VideoCapture('http://192.168.0.2:4747/video')
	#retval, image = cap.read()
	retval, buffer = cv2.imencode('.jpg', image)
	jpg_as_text = base64.b64encode(buffer)
	cap.release()
	return "data:image/png;base64, " + jpg_as_text
"""
#------ Global Variable ----

camera_status = 1
capture_status = False
student_id = ''
"""
def show_error(title, msg):
    root = Tk()
    root.withdraw()  # hide main window
    messagebox.showerror(title, msg)
    root.destroy()
"""


def recogFace(data,encoding):
    return face_recognition.compare_faces(data["encodings"], encoding, tolerance=0.5)

def recogEncodings(rgb,boxes):
    return face_recognition.face_encodings(rgb, boxes)

def recogLoc(rgb):
    return face_recognition.face_locations(rgb, model = "hog")


def gen1(url,student_class):
    #change camera status for loading
    eel.camera_status(3)

    pool1 = ThreadPool(processes = 1)
    pool2 = ThreadPool(processes = 2)
    pool3 = ThreadPool(processes = 3)
    pool4 = ThreadPool(processes = 4)
    pool5 = ThreadPool(processes = 5)

    conn = create_connection()
    cursor = conn.cursor()
    sql = "SELECT student_id FROM student_data WHERE class = ? "
    val =[student_class]
    cursor.execute(sql,val)
    student_data = cursor.fetchall()
    #print(student_data)
    # Load the known face and encodings
    #print("[INFO] loading encodings ..")
    data = pickle.loads(open("encodings.pickle","rb").read())

    Attendees_Names = {}
    encodings = []
    boxes = []
    frame = 0
    Scene = sceneChangeDetect() 
    video = cv2.VideoCapture(url)
    time.sleep(1.0)
    global camera_status
    camera_status = 1
    #change the camera status
    eel.camera_status(1)
    while camera_status == 1:
        frame +=1
        if(frame==100):
            frame = 0
        #print(camera_status)
        #img = camera.get_frame()
        success, img = video.read()
        #if camera can't read frame(Camera error)
        if success == False:
            eel.camera_status(2)
            break
        if(Scene.detectChange(img) == True):
            #Convert the BGR to RGB
            # a width of 750px (to speed up processing)
            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            rgb = imutils.resize(img, width = 750)
            r = img.shape[1]/float(rgb.shape[1])

            #detect boxes
            if(frame%2 == 0):
                boxes = pool1.apply_async(recogLoc,(rgb,)).get()
                encodings = pool3.apply_async(recogEncodings,(rgb,boxes,)).get()
            names = []

                # loop over the facial encodings
            for encoding in encodings :
                # attempt to match each face then initialise a dicationary
                #matches = face_recognition.compare_faces(data["encodings"], encoding,tolerance=0.5)
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
                        for y in student_data:
                            if name in y:
                                x = datetime.datetime.now()
                                date = str(x.day)+"-"+str(x.month)+"-"+str(x.year)
                                pool4.apply_async(submit_live_attendance,(name,student_class,date,))
                                #submit_live_attendance(name,student_class,date)
                                eel.updateAttendance(name)()

                names.append(name)


        # loop over recognized faces
        """
        for ((top,right,bottom,left),name)in zip(boxes, names):
            top = int(top*r)
            right = int(right*r)
            bottom = int(bottom*r)
            left = int(left *r)
            # draw the predicted face name on the image
            cv2.rectangle(img, (left, top), (right, bottom),
                (0, 255, 0), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(img, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                0.75, (0, 255, 0), 2)
        """
        ret, jpeg = cv2.imencode('.jpg', img)
        img = jpeg.tobytes()
        yield img
    #camera is stopped by user
    if success == True:
        eel.camera_status(0)
        #cv2.imshow("Frame", img)
        #key = cv2.waitKey(1) & 0xFF
        # if the `q` key was pressed, break from the loop
        #if key == ord("q"):
            #break


@eel.expose
def start_video_py(cam_type,student_class,url = ''):
    #x = VideoCamera()
    switch={
        '1' : 0,
        '2' : 1,
        '3' : url,
    }
    y = gen1(switch[cam_type],student_class)
    for each in y:
        # Convert bytes to base64 encoded str, as we can only pass json to frontend
        blob = base64.b64encode(each)
        blob = blob.decode("utf-8")
        eel.updateImageSrc(blob)()
        # time.sleep(0.1)
@eel.expose
def stop_video_py():
    global camera_status
    camera_status = 0

@eel.expose
def photoUpload(b64_string,student_class):
    encoded_data = b64_string.split(',')[1]
    decoded_data = base64.b64decode(encoded_data)
    nparr = np.fromstring(decoded_data, np.uint8)
    #nparr = np.fromstring(encoded_data.decode('base64'), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    photo.recognizeFromPhoto(img,student_class)
    ##print(photo_string)
    #return photo_string
@eel.expose
def capture_photo_py(url):
    #x = VideoCamera()
    y = gen(url)
    for each in y:
        # Converted to base64 encoded str, as we can only pass json to frontend
        blob = base64.b64encode(each)
        blob = blob.decode("utf-8")
        eel.updateStudentImageSrc(blob)()
        # time.sleep(0.1)
def gen(url):
    video = cv2.VideoCapture(url)
    time.sleep(2.0)
    global camera_status
    global capture_status
    camera_status = 1
    #change the camera statu
    while camera_status == 1:
        #img = camera.get_frame()
        success, img = video.read()
        #if camera can't read frame
        if success == False:
            #print("cam nt cnt")
            break
        if capture_status == True:
            save_path = 'dataset/'+student_id
            filename = save_path+"/photo"+str(random.randint(0, 999))+".jpg"
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            cv2.imwrite(filename, img)
            send_capture_photo(img)
            capture_status = False
        ret, jpeg = cv2.imencode('.jpg', img)
        img = jpeg.tobytes()
        yield img

#add new user data    
#@eel.expose
#def add_new_student(new_student_id):
    ##print(new_student_id)
    #encode_student_data.encode_student_data(new_studentId)
def submit_live_attendance(stu_id, student_class,date):
    attendance_class={
        "xii" : "INSERT INTO xii(student_id,attendance_date) VALUES(?, ?);",
        "xi"  : "INSERT INTO xi(student_id,attendance_date) VALUES(?, ?);",
    }
    #adding data to database
    conn = create_connection()
    cursor = conn.cursor()
    sql = attendance_class[student_class]
    val = [stu_id, date]
    cursor.execute(sql, val)
    conn.commit()
    conn.close()
    
@eel.expose
def save_photo(studentId):
    global student_id
    global capture_status
    student_id = studentId
    capture_status = True

def send_capture_photo(img):
    ret, jpeg = cv2.imencode('.jpg', img)
    img = jpeg.tobytes()
    blob = base64.b64encode(img)
    blob = blob.decode("utf-8")
    eel.showCapturePhoto(blob)
#adding new student data
@eel.expose
def submit_student_data(stu_id, fullname, student_class, session):
    try:
        encode_student_data.encode_student_data(stu_id)
        #adding data to database
        conn = create_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO student_data(student_id,fullname,class,session) VALUES(?, ?, ?, ?);"
        val = [stu_id, fullname, student_class, session]
        cursor.execute(sql, val)
        conn.commit()
        eel.student_data_saved()
        conn.close()

    except:
        #delete face data from file
        delete_student_data_file(student_id)
        eel.failed_data_submit()

@eel.expose
def fetch_class_data(search_class):
    conn = create_connection()
    cursor = conn.cursor()
    val = [search_class]
    sql = "SELECT * FROM student_data WHERE class = ?"
    result = cursor.execute(sql,val)
    for x in result:
        eel.setTableData(x[0],x[1],x[2],x[3])
    conn.close()

def delete_student_data_file(student_id):
    #delete face data from file
    #load the face data
    with open('encodings.pickle', 'rb') as f:
            face_data = pickle.load(f)
    index = []
    encodings = face_data['encodings']
    names    = face_data['names']

    #count face data length
    for i,item in enumerate(names):
        if student_id in item:
            index.append(i)
    #delete id
    for i in index:
        names.remove(student_id)
    #delete encoding
    for i in index:
        del encodings[index[0]]
            
    #saved modified face data
    face_data['names'] = names
    face_data['encodings'] = encodings
        
    f = open("encodings.pickle","wb")
    f.write(pickle.dumps(face_data))
    f.close()

@eel.expose
def deleteStudent(student_id):
    try:
        ##print("connect to database")
        ##print(student_id)

        #delete student image folder
        try:
            path = 'dataset/'+student_id
            shutil.rmtree(path)
        except Exception as e:
            print(e)

        #delete student data from database
        conn = create_connection()
        cursor = conn.cursor()
        val = [student_id]
        sql = "DELETE FROM student_data where student_id = ?"
        cursor.execute(sql,val)
        conn.commit()
        conn.close()
        ##print("delete success database")

        #delete face data from file
        delete_student_data_file(student_id)
        eel.deleteStatus(student_id)
    except Exception as e:
        print(e)
        eel.deleteStatus("")

@eel.expose
def fetchAttendance(attendanceClass, attendanceDate):
    student_class={
        'xi'  : "SELECT DISTINCT(d.student_id),d.fullname,d.class,ac.attendance_date FROM xi ac,student_data d WHERE ac.student_id=d.student_id AND attendance_date = ?;",
        'xii' : "SELECT DISTINCT(d.student_id),d.fullname,d.class,ac.attendance_date FROM xii ac,student_data d WHERE ac.student_id=d.student_id AND attendance_date = ?;",
    }
    conn = create_connection()
    cursor = conn.cursor()
    val = [attendanceDate]
    sql = student_class[attendanceClass]
    cursor.execute(sql,val)
    result = cursor.fetchall()
    print(len(result))
    if len(result)>0:
        for x in result:
            eel.attendanceTable(x[0],x[1],x[2],x[3])
    else:
        eel.attendanceTable("no result found","","","")
    conn.close()

@eel.expose
def fetch_graph_data(graphClass):
    student_class = {
        'xi'  : "SELECT DISTINCT(attendance_date) FROM xi ORDER BY attendance_date ASC LIMIT 06 ",
        'xii' : "SELECT DISTINCT(attendance_date) FROM xii ORDER BY attendance_date ASC LIMIT 06 ",
    }
    attendance_class = {
        'xi'  : "SELECT COUNT(DISTINCT(student_id)) FROM xi WHERE attendance_date = ? ;",
        'xii' : "SELECT COUNT(DISTINCT(student_id)) FROM xii WHERE attendance_date = ? ;",
    }

    conn = create_connection()
    cursor = conn.cursor()
    sql = student_class[ graphClass ]
    result = cursor.execute(sql)
    date_arr = []
    data_arr = []
    for x in result:
        date_arr.append(x[0])
    #print(date_arr)
    sql = attendance_class[ graphClass ]
    for x in date_arr:
        val = [x]
        result = cursor.execute(sql,val)
        for x in result:
            data_arr.append(x[0])
    #print(data_arr)
    cursor.close()
    eel.updateGraph(date_arr,data_arr)

@eel.expose
def get_user_details():
    return login.session['user_name']


eel.start('login.html',size =(1307,713))