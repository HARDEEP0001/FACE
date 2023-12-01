import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate("serviceaccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://face-11f6e-default-rtdb.firebaseio.com/"
})
ref=db.reference('Students')
data={
    "321654":{
        "name":"Hardeep Singh",
        "status":"In Jail",
        "starting_year":2021,
        "total_attendance":6,
        "standing":"g",
        "year":5,
        "last_attendance_time":"2022-12-11 00:54:34"


    },"852741":{
        "name":"Emlie",
        "status":"bailed on 2AUG 2021",
        "starting_year":2001,
        "total_attendance":8,
        "standing":"b",
        "year":6,
        "last_attendance_time":"2022-12-11 00:54:34"


    },"963852":{
        "name":"Elon Musk",
        "status":"Free",
        "starting_year":2003,
        "total_attendance":69,
        "standing":"e",
        "year":10,
        "last_attendance_time":"2022-12-11 00:54:34"


    }
}
for key,value in data.items():
    ref.child(key).set(value)