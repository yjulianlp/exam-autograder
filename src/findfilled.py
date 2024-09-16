import cv2
import numpy as np
from exam import Exam, Question, Circle

def get_level(circle_object):
	return circle_object[1]
def get_col(circle_object):
	return circle_object[0]
filename = input("Completed Exam Filename: ")
questions = int(input("Number of Questions: "))

letters = ['A', 'B', 'C', 'D']
exam = cv2.imread(f"../images/{filename}.jpg")
gray_exam = cv2.cvtColor(exam, cv2.COLOR_BGR2GRAY)
blur = cv2.blur(gray_exam, (9,9))
detected_circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 1, 30, param1=45, param2=135, minRadius=20, maxRadius=80)

circle_levels = []
for j in range(questions):
	circle_levels.append([])

if len(detected_circles) > 0:
	circle_info = (np.uint16(np.around(detected_circles))).tolist()
	circle_info[0] = sorted(circle_info[0],key=get_level) #sort by question

	for i in range(len(circle_info[0])):
		circle_levels[(i//4)].append(circle_info[0][i])

for i in range(len(circle_levels)):
	circle_levels[i] = sorted(circle_levels[i], key=get_col)
	for j in range(len(circle_levels[i])):
		circle_levels[i][j] = Circle(circle_levels[i][j][0], circle_levels[i][j][1], circle_levels[i][j][2], letters[j], exam)

	circle_levels[i] = Question(circle_levels[i], 0, exam)
for level in circle_levels:
	level.draw_question()

print(f"has value {circle_levels[0].get_option(0).get_letter()}")
print(f"is filled? {circle_levels[0].get_option(0).is_filled()}")

exam2 = Exam(circle_levels, questions, exam)
exam2.draw_filled()
cv2.imshow("exam", exam)

cv2.waitKey(0)