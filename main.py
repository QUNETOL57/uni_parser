import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv, find_dotenv
import sqlite3

load_dotenv(find_dotenv())

MIREA_LOGIN=os.getenv('USER_LOGIN')
MIREA_PASSWORD=os.getenv('USER_PASSWORD')
MY_NAME=os.getenv('MY_NAME')
PORTAL_NAME='https://portal.stavuniver.ru/'
SEMESTR = 5


session  = requests.Session()
authorization = session.post(PORTAL_NAME, data = {'name':MIREA_LOGIN,'pass':MIREA_PASSWORD})
# tutor = session.get('{PORTAL_NAME}mail_messages.php?action=messages&id=7741')

# soup = BeautifulSoup(tutor.text, 'lxml')

# dylog_table = soup.find("table", id="ramka2")

# dylog_name = dylog_table.find('td', class_='main_head2').text

# TUTOR_NAME = dylog_name.replace('Диалог с', '').strip()

# for tr in dylog_table.find_all('tr')[2:]:
# 	for td in tr.find_all('td'):
# 		if TUTOR_NAME in td.text:
# 			print("TUTOR - ", end='')
# 		elif MY_NAME in td.text:
# 			print("ME - ", end='')
# 		else:
# 			print(td.text.strip())
# 			print('-'*30)


def get_educators():
	# Список страниц с предметами 
	sections = [BeautifulSoup(session.get(f'{PORTAL_NAME}edu_process.php?work_type={i}').text, 'lxml') for i in range(1,5)]

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




educators = get_educators()

def insert_educators(educators):
	connect = sqlite3.connect('base.db')
	cursor = connect.cursor()
	cursor.execute("""CREATE TABLE IF NOT EXISTS educators (
		id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
		name     VARCHAR (255) NOT NULL,
		subject  VARCHAR (255) NOT NULL,
		semestr  INTEGER (2)   NOT NULL,
		is_tutor BOOLEAN       NOT NULL
	)""")
	cursor.executemany("INSERT INTO educators (name, subject, semestr, is_tutor) VALUES (?,?,?,?)", educators)
	connect.commit()

insert_educators(educators)