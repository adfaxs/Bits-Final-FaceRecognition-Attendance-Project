import cv2
import numpy as np
import face_recognition
import os
import mysql.connector as mariadb
import sys
from datetime import datetime



pa = 'ImagesAttendance'
img = []
imgname = []
Names=[]
Nameid=[]
id=[]
myli = os.listdir(pa)


for cl in myli:
    curImg = cv2.imread(f'{pa}/{cl}')
    img.append(curImg)
    imgname.append(os.path.splitext(cl)[0])


for ii in imgname:
    Nameid.append(ii.split(','))

i=0
for oo in Nameid:
    Names.append(Nameid[i][1])
    id.append(Nameid[i][0])
    i=i+1



print(Nameid)
print(id)
print(Names)

def findEncodings(img):
    encoded= []
    for img in img:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        enco = face_recognition.face_encodings(img)[0]
        encoded.append(enco)
    return encoded


def markAttendance(name,idd):
    with open('Attendance.csv', 'r+') as f:
        now = datetime.now()
        dtString = now.strftime("%Y-%m-%d")
        myDataList = f.readlines()
        nameList = []
        full = name+dtString

        for line in myDataList:
             entry = line.split(',')
             nameList.append(entry[0]+entry[1])

        if (full not in nameList):
           f.writelines(f'\n{name},{dtString},{idd}')
           print(name)

           # Connect to MariaDB Platform
           try:
               conn = mariadb.connect(
                   user="remote_connect",
                   password="remote_connect",
                   host="34.72.114.168",
                   port=3306,
                   database="wordpress"

               )
           except mariadb.Error as e:
               print(f"Error connecting to MariaDB Platform: {e}")
               sys.exit(1)

           cursor = conn.cursor()
           date = dtString
           staff_id = idd
           Name = name
           Attend = "P"
           cursor.execute("INSERT INTO Attendance (date,staff_id,Name,Attend) VALUES (%s,%s,%s,%s)", (date, staff_id, Name, Attend))
           conn.commit()
           conn.close()






encodKnown = findEncodings(img)
print('Encoding Complete')
cap = cv2.VideoCapture(0,cv2.CAP_V4L)

while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)


    facesCurFrame = face_recognition.face_locations(imgS)
    encosCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encosCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodKnown, encodeFace,0.45)
        faceDis = face_recognition.face_distance(encodKnown, encodeFace)
        # print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
         name = Names[matchIndex].upper()
         idd = id[matchIndex].upper()
         y11, x22, y22, x11 = faceLoc
         y11, x22, y22, x11 = y11 * 4, x22 * 4, y22 * 4, x11 * 4
         cv2.rectangle(img, (x11, y11), (x22, y22), (127, 0, 127), 1)
         cv2.rectangle(img, (x11, y22 - 35), (x22, y22), (127, 0, 127), cv2.FILLED)
         cv2.putText(img, name, (x11 + 6, y22 - 6), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
         markAttendance(name,idd)

    cv2.startWindowThread()
    cv2.namedWindow('Webcam', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Webcam', 1080, 800)
    cv2.imshow('Webcam', img)
    cv2.waitKey(1)