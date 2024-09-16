import cv2 as cv
import numpy as np

filename = input("Blank Exam Filename: ")
questions = int(input("Number of Questions: "))
blank = np.zeros((1000,500, 3), dtype="uint8")
blank.fill(255)

letters = ['A', 'B', 'C', 'D']
#line1
for j in range(questions):
	for i in range(4):
		cv.circle(blank, ((blank.shape[1]//5)*(i+1), (150*(j))+70), 40, (0,0,0), thickness=3)
		cv.putText(blank, letters[i], ((blank.shape[1]//5)*(i+1)-10, (150*(j))+80), cv.FONT_HERSHEY_DUPLEX, 1.0, (0,0,0), 1)

cv.imwrite(f"../images/{filename}.jpg", blank)

cv.waitKey(0)