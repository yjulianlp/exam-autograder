import cv2
import json
import firebase_admin
from firebase_admin import credentials, db
import numpy as np
from exam import Exam, Question, Circle, mark_exam

letters = ['A', 'B', 'C', 'D']

#get info
filename = input("Completed Exam Filename: ")
questions = int(input("Number of Questions: "))
answer_key = input("Answer Key Filename (.csv): ")
firstname = input("Student Firstname: ")
lastname = input("Student Lastname: ")
studentid = int(input("Student ID: "))

#mark & get result
result = json.loads(mark_exam(filename, questions, answer_key, firstname, lastname, studentid))

#store details
cred = credentials.Certificate("../auth/firebasekey.json")
config = open("../auth/config.txt")
url = config.readline()
firebase_admin.initialize_app(cred, {"databaseURL":f"{url}"})
ref = db.reference(f"/exams/{studentid}")
ref.set(result)