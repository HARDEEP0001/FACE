import cv2
import face_recognition
import pickle
import os
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
folderPath='Images'
pathList=os.listdir(folderPath)
print(pathList)
imageList=[]
studentIds=[]
for path in pathList:
    imageList.append(cv2.imread(os.path.join(folderPath,path)))
    #print(path)
    #print(os.path.splitext(path)[0])
    studentIds.append(os.path.splitext(path)[0])

    filename=f'{folderPath}/{path}'
    bucket=storage.bucket()
    blob=bucket.blob(filename)
    blob.upload_from_filename(filename)

print(studentIds)

def findEncodings(imageList):
    encodeList=[]

    for image in imageList:
        image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(image)[0]
        encodeList.append(encode)


    return encodeList
print("encoding started")
encodeListKnown=findEncodings(imageList)
encodeListKnownwithIds=[encodeListKnown,studentIds]
print("encoding complete")
file=open('encodefile.p','wb')
pickle.dump(encodeListKnownwithIds,file)
file.close()
print("file saved ")

