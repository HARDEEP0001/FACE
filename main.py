import cv2
import os
import pickle
import cvzone

import face_recognition
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
#importing student images
cred = credentials.Certificate("serviceaccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://face-11f6e-default-rtdb.firebaseio.com/",
    'storageBucket':"face-11f6e.appspot.com"
})
bucket=storage.bucket()
cap = cv2.VideoCapture(0) # Use index 0 for the default camera
cap.set(2,640)
cap.set(4,480)
imgBackground=cv2.imread('Resources/background.png')
#importing mode images into a list
folderModePath='Resources/Modes'
modePathList=os.listdir(folderModePath)
imageModeList=[]
for path in modePathList:
    imageModeList.append(cv2.imread(os.path.join(folderModePath,path)))
#print(len(imageModeList))
#load the encoding file
print("loading encoding file..")
file=open('encodefile.p','rb')
encodeListKnownwithIds=pickle.load(file)
file.close()
encodeListKnown,studentIds=encodeListKnownwithIds

#print(studentIds)
print(" encode file loaded..")
modetype=0
counter=0
id=-1
imagestudent=[]
while True:
    success, img = cap.read()
    imgS=cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    faceCurFrame=face_recognition.face_locations(imgS)
    encodeCurFrame=face_recognition.face_encodings(imgS,faceCurFrame)



    imgBackground[162:162+480,55:55+640]=img
    imgBackground[44:44+633,808:808+414] = imageModeList[modetype]
    for encodeFace,faceLoc in  zip(encodeCurFrame,faceCurFrame):
        matches=face_recognition.compare_faces(encodeListKnown,encodeFace)
        facedis=face_recognition.face_distance(encodeListKnown,encodeFace)

        matchindex=np.argmin(facedis)

        if matches[matchindex]:
            #print("known face detected")
            #print(studentIds[matchindex])
            y1,x2,y2,x1=faceLoc
            y1, x2, y2, x1=y1*4,x2*4,y2*4,x1*4
            bbox=55+x1,162+y1,x2-x1,y2-y1
            imgBackground=cvzone.cornerRect(imgBackground,bbox,rt=0)
            id=studentIds[matchindex]
            if counter==0:
                counter=1
                modetype=1
        if counter!=0:
            if counter==1:
                #get the data
                studentInfo=db.reference(f'Students/{id}').get()
                print(studentInfo)
                #get the image from the storage
                blob=bucket.get_blob(f'Images/{id}.png')
                array=np.frombuffer(blob.download_as_string(),np.uint8)
                imagestudent= cv2.imdecode(array,cv2.COLOR_BGRA2BGR)
                ref=db.reference(f'Students/{id}')
                studentInfo['total_attendance']+=1
                ref.child('total_attendance').set(studentInfo['total_attendance'])
            cv2.putText(imgBackground,str(studentInfo['total_attendance']),(861,125),
                        cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)

            cv2.putText(imgBackground, str(studentInfo['status']), (1006, 550),
                        cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(imgBackground, str(studentInfo['year']), (1006, 493),
                        cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
            cv2.putText(imgBackground, str(studentInfo['year']), (1125, 625),
                        cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
            (w,h), _=cv2.getTextSize(studentInfo['name'],cv2.FONT_HERSHEY_COMPLEX,1,1)
            offset=(414-w)//2

            cv2.putText(imgBackground, str(studentInfo['name']), (808+offset, 445),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)
            imgBackground[175:175+216,909:909+216]=imagestudent




            counter+=1






    #cv2.imshow("Webcam", img)
    cv2.imshow("face attendance",imgBackground)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
