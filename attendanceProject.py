import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import glob
import database
path = "imagesAttendance"
images = []
classNames = []
myList = os.listdir(path)
#print(myList)
#using the above names and importing the above images one by one
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
#print(classNames)

#encoding process
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListKnwon = findEncodings(images)
#print('Encoding Complete')


#find matches between encodings and the images coming from web cam
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
nm="a"

#to get each frame
while True:
    success, img = cap.read()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)

    #finding matches
    for encodeFace, faceLoc in zip(encodesCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnwon,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnwon,encodeFace)
        #print(faceDis)
        matchIndex = np.argmin(faceDis) #gives index

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            y1,x1,y2,x2 = faceLoc
            y1, x1, y2, x2 = y1*4 , x1*4 ,y2*4 ,x2*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,0),2)
            cv2.rectangle(img,(x1,y2),(x2,y2),(255,0,0),cv2.FILLED)
            cv2.putText(img,name,(x1,y2),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)

            crTime = datetime.now().time()
            crDate = datetime.now().date()

            if(crTime.hour <16):
                if name != nm:
                    database.check_name_state(name, str(crTime), str(crDate),"Check In")
                    nm = name
            else:
                if (name != nm):
                    database.check_name_state_out(name, str(crTime), str(crDate),"Check Out")
                    nm = name

    cv2.putText(img, 'press q to exit', (10, 18), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 2)
    cv2.imshow("Web Cam",img)
    if(cv2.waitKey(1) & 0xFF==ord('q')):
        break

cap.release()
cv2.destroyAllWindows()



