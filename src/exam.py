import cv2 as cv2
import numpy as np
import json

def get_level(circle_object):
	return circle_object[1]
def get_col(circle_object):
	return circle_object[0]

def mark_exam(filename, questions, answer_key, firstname, lastname, studentid):
	letters = ['A', 'B', 'C', 'D']
	correct_answers = []
	#read answer key
	with open(f"../answer_key/{answer_key}.csv", "r+") as ans_key:
		for ans in ans_key:
			if not ans.isspace():
				correct_answers.append(ans.strip().replace(" ", "").split(","))

	#detect answers
	exam = cv2.imread(f"../images/{filename}.jpg")
	exam_template = cv2.imread(f"../images/{questions}questions_template.jpg")
	gray_template = cv2.cvtColor(exam_template, cv2.COLOR_BGR2GRAY)
	blur = cv2.blur(gray_template, (9,9))
	detected_circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 1, 30, param1=45, param2=135, minRadius=20, maxRadius=80)

	circle_levels = []
	for j in range(questions):
		circle_levels.append([])

	num_detected = len(detected_circles[0])

	print(f"{num_detected} circles detected")

	if num_detected > 0 and num_detected == (len(letters)*questions):
		circle_info = (np.uint16(np.around(detected_circles))).tolist()
		circle_info[0] = sorted(circle_info[0],key=get_level) #sort by question

		for i in range(len(circle_info[0])):
			circle_levels[(i//4)].append(circle_info[0][i])
	else:
		print("Please manually check and clean the exam image")
		exit(-1)

	for i in range(len(circle_levels)):
		circle_levels[i] = sorted(circle_levels[i], key=get_col)
		for j in range(len(circle_levels[i])):
			circle_levels[i][j] = Circle(circle_levels[i][j][0], circle_levels[i][j][1], circle_levels[i][j][2], letters[j], exam)

		circle_levels[i] = Question(circle_levels[i], circle_levels[i][0], exam)

	processed_exam = Exam(circle_levels, questions, exam, firstname, lastname, studentid)
	processed_exam.find_chosen_answers()
	selected_answers = processed_exam.get_chosen_answers()

	total_correct = 0

	#compare answers
	for i in range(len(correct_answers)):
		if correct_answers[i][1].lower() == selected_answers[i][1].lower():
			total_correct +=1
			processed_exam.get_question(i).draw_filled(correct=True) #green outline
		else:
			processed_exam.get_question(i).draw_filled() #red outline
	temp_json = {
		"firstname":processed_exam.get_first_name(),
		"lastname":processed_exam.get_last_name(),
		"studentid":processed_exam.get_student_id(),
		"score":total_correct,
		"selected_answers":processed_exam.get_answers_json()
	}
	temp_json = json.dumps(temp_json)
	cv2.imwrite(f"../marked/{filename}-marked.jpg", exam)

	return temp_json

class Circle:
	def __init__(self, x, y, radius, letter, exam_image):
		self.exam_image = cv2.cvtColor(exam_image, cv2.COLOR_BGR2GRAY)
		self.x = x 
		self.y = y
		self.letter = letter
		self.radius = radius
	def print_info(self):
		print(f"Circle at ({self.x, self.y}) with radius {self.radius}")

	def get_letter(self):
		return self.letter

	def set_letter(self, letter):
		self.letter = letter

	def get_image(self):
		return self.exam_image

	def set_image(self, image):
		self.exam_image = image

	def get_y(self):
		return self.y

	def set_y(self, y):
		self.y = y

	def get_x(self):
		return self.x

	def set_x(self, x):
		self.x = x

	def get_radius(self):
		return self.radius

	def set_radius(self, radius):
		self.radius = radius

	def draw(self, file, radius, b, g, r, thickness):
		cv2.circle(file, (self.x, self.y), radius, (b,g,r), thickness)

	def is_filled(self):
			blank = self.exam_image.copy()
			blank.fill(0)
			temp_circle = cv2.circle(blank, (self.get_x(), self.get_y()), self.get_radius(), (255,255,255), -1) #fill
			temp_masked = cv2.bitwise_and(self.exam_image, blank, mask=temp_circle)
			print(cv2.mean(self.exam_image, mask=temp_masked)[0])
			return ((cv2.mean(self.exam_image, mask=temp_masked)[0]) < 210)

class Question:

	def __init__(self, question_options, answer_choice, exam_image):
		self.exam_image = exam_image
		self.question_options = question_options #list of circles
		self.answer_choice = answer_choice

	def get_image(self):
		return self.exam_image

	def set_image(self, image):
		self.exam_image = image

	def draw_question(self):
		for choice in self.question_options:
			choice.draw(choice.get_image(), choice.get_radius(), 0, 0, 255, 3)

	def get_answer(self):
		return self.answer_choice

	def set_answer(self, index):
		self.answer_choice = index

	def get_option(self, index):
		return self.question_options[index]

	def set_option(self, index, option):
		self.question_options[index] = option

	def get_options(self):
		return self.question_options

	def set_options(self, options):
		self.question_options = options

	def draw_filled(self, correct=False):
		for option in self.question_options:
			if(option.is_filled()):
				if correct:
					option.draw(self.exam_image, option.get_radius(), 0, 255, 0, 3)
				else:
					option.draw(self.exam_image, option.get_radius(), 0, 0, 255, 3)

	def find_chosen_answer(self):
		#will go with first option detected as filled
		for option in self.question_options:
			if option.is_filled():
				self.answer_choice = option
				break

	def get_chosen_answer(self):
		return self.answer_choice.get_letter()



class Exam:

	def __init__(self, questions, num_questions, exam_image, first_name, last_name, student_id):
		self.exam_image = exam_image
		self.questions = questions #list of questions
		self.num_questions = num_questions
		self.first_name = first_name
		self.last_name = last_name
		self.student_id = student_id

	def get_first_name(self):
		return self.first_name

	def set_first_name(self, firstname):
		self.first_name = firstname

	def get_last_name(self):
		return self.last_name

	def set_last_name(self, lastname):
		self.last_name = lastname

	def get_student_id(self):
		return self.student_id

	def set_student_id(self, studentid):
		self.student_id = studentid

	def get_image(self):
		return self.exam_image

	def set_image(self, image):
		self.exam_image = image

	def get_question(self, question_index):

		if question_index >= len(self.questions): #if wrong index used
			return self.questions[len(self.questions)-1]
		return self.questions[question_index]

	def set_question(self, question_index, new_question):

		self.questions[question_index] = new_question

	def add_question(self):
		self.questions.append(question)

	def get_questions(self):
		return self.questions

	def set_questions(self, questions):
		self.questions = questions

	def get_num_questions(self):
		return self.num_questions

	def set_num_questions(self, num_questions):
		self.num_questions = num_questions

	def draw_filled(self):
		for question in self.questions:
			question.draw_filled()

	def find_chosen_answers(self):
		for question in self.questions:
			question.find_chosen_answer()

	def get_chosen_answers(self):
		chosen_answers = []
		for i in range(len(self.questions)):
			chosen_answers.append([i+1,self.questions[i].get_chosen_answer()])
		return chosen_answers

	def get_answers_json(self):
		temp_dict = {}
		for answer in self.get_chosen_answers():
			temp_dict[answer[0]] = answer[1]
		return temp_dict

	def print_chosen_answers(self):
		for i in range(len(self.questions)):
			print(f"Examinee chose option {self.questions[i].get_chosen_answer()} for Question # {i+1}.")