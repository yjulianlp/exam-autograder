import cv2
import numpy as np
from exam import Exam, Question, Circle, mark_exam

letters = ['A', 'B', 'C', 'D']

#get filenames
filename = input("Completed Exam Filename: ")
questions = int(input("Number of Questions: "))
answer_key = input("Answer Key Filename (.csv): ")

mark_exam(filename, questions, answer_key)