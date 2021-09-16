import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

MIREA_LOGIN=os.getenv('USER_LOGIN')
MIREA_PASSWORD=os.getenv('USER_PASSWORD')
MY_NAME=os.getenv('MY_NAME')
PORTAL_NAME='https://portal.stavuniver.ru/'

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
	
	sections = [
		BeautifulSoup(session.get(f'{PORTAL_NAME}edu_process.php?work_type=1').text, 'lxml').find('table', class_='table-hover'),
		BeautifulSoup(session.get(f'{PORTAL_NAME}edu_process.php?work_type=2').text, 'lxml').find('table', class_='table-hover'),
		BeautifulSoup(session.get(f'{PORTAL_NAME}edu_process.php?work_type=3').text, 'lxml').find('table', class_='table-hover'),
		BeautifulSoup(session.get(f'{PORTAL_NAME}edu_process.php?work_type=4').text, 'lxml').find('table', class_='table-hover'),
	]

	educators = []
	for section in sections:
		for line in section.find_all('tr')[1:]:
			if ('Закрыт' in line.find_all('td')[-1].text):
				print(line.find_all('td')[-2].text)



get_educators()

