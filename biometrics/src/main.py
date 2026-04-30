import cv2
import numpy as np
import face_recognition
import os
def markAttendance(name):
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        now = datetime.now()
        dtString = now.strftime('%Y-%m-%d;%H:%M:%S; Present')
        found = False
        for i, line in enumerate(myDataList):
            entry = line.strip().split(';')
            if entry[0] == name:
                myDataList[i] = f'{name};{dtString}\n'
                found = True
                break
        if not found:
            myDataList.append(f'{name};{dtString}\n')
        f.seek(0)
        f.writelines(myDataList)
        f.truncate()
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodes = face_recognition.face_encodings(img)
        if encodes:
            encodeList.append(encodes[0])
    return encodeList


from datetime import datetime
path = 'ImagesAttendance'
images = []
classNames = []
myList = os.listdir(path)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
encodeListKnown = findEncodings(images)
cap = cv2.VideoCapture(0)
while True:
    success, img = cap.read()
    if not success:
        print("Failed to capture image")
        break
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = []
    if facesCurFrame:
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)
            if matches[matchIndex] and faceDis[matchIndex] < 0.50:
                name = classNames[matchIndex].upper()
            else:
                name = 'Unknown'
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            color = (0, 255, 0) if name != 'Unknown' else (0, 0, 255)
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), color, cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            if name != 'Unknown':
                markAttendance(name)
    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) & 0xFF == ord(' '):
        break
cap.release()
cv2.destroyAllWindows()
