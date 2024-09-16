import cv2 as cv2
import numpy as np

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

	def __init__(self, question_options, answer_choice_index, exam_image):
		self.exam_image = exam_image
		self.question_options = question_options #list of circles
		self.answer_choice = answer_choice_index

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

	def draw_filled(self):
		for option in self.question_options:
			if(option.is_filled()):
				option.draw(self.exam_image, option.get_radius(), 0, 0, 255, 3)

class Exam:

	def __init__(self, questions, num_questions, exam_image):
		self.exam_image = exam_image
		self.questions = questions #list of questions
		self.num_questions = num_questions

	def get_image(self):
		return self.exam_image

	def set_image(self, image):
		self.exam_image = image

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