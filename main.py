import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv, find_dotenv

import db

load_dotenv(find_dotenv())

MIREA_LOGIN=os.getenv('USER_LOGIN')
MIREA_PASSWORD=os.getenv('USER_PASSWORD')
MY_NAME=os.getenv('MY_NAME')
PORTAL_URL='https://portal.stavuniver.ru/'
SEMESTR = 5

session  = requests.Session()
authorization = session.post(PORTAL_URL, data = {'name':MIREA_LOGIN,'pass':MIREA_PASSWORD})

sections = {i: BeautifulSoup(session.get(f'{PORTAL_URL}edu_process.php?work_type={i}').text, 'lxml') for i in range(1,5)}

def get_educators():
	"""Список страниц с предметами"""
	educators = []
	for section in sections:
		# title = section.find('h4', class_='zag').text.strip()
		# print('\t' + title)
		for line in section.find('table', class_='table-hover').find_all('tr')[1:]:
			if line.find_all('td')[-1].find('a', class_='btn-danger'):
				educator_name = line.find_all('td')[-2].text
				educator_subject = line.find_all('td')[0].text

				if not any(educator_subject == educator[1] for educator in educators):
					educators.append([
						educator_name,
						educator_subject,
						SEMESTR,
						False
					])
	return educators

def set_teachers():
	"""Загружает в базу список предподавателей"""
	teachers = set()
	for section in sections.values():
		for line in section.find('table', class_='table-hover').find_all('tr')[1:]:
			if line.find_all('td')[-1].find('a', class_='btn-danger'):
				teacher_name = line.find_all('td')[-2].text
				teachers.add(teacher_name)

	teachers = list(map(lambda teacher: [teacher, False], teachers))

	tutor = BeautifulSoup(session.get(f'{PORTAL_URL}mail_messages.php?action=messages&id=7741').text, 'lxml').find('td', class_='main_head2').text
	tutor = tutor.replace('Диалог с', '').strip()
	teachers.append([tutor, True])

	for teacher in teachers:
		db.insert('teacher', {
			'name'		: teacher[0],
			'is_tutor'	: teacher[1]
		})

def set_subjects():
	"""Загружаем в базу список предметов"""
	for key, section in sections.items():
		semestr = section.find('option', selected=True)['value'] if section.find('option', selected=True) else ''
		type_id = key
		for line in section.find('table', class_='table-hover').find_all('tr')[1:]:
			if line.find_all('td')[-1].find('a', class_='btn-danger'):
				subject_name = line.find_all('td')[0].text
				teacher_name = line.find_all('td')[-2].text
				teacher_id = db.feach('teacher', {'name': teacher_name})[0]

				db.insert('subject', {
					'name': subject_name,
					'semestr': semestr,
					'type_id': type_id,
					'teacher_id': teacher_id
				})
				

def set_themes():
	"""Загружаем в базу все темы для предметов"""
		


# set_teachers()