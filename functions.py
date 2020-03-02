import json
import time
import sqlite3
import requests

def get_payment_link(number, sum, comment=""):
	link = "https://qiwi.com/payment/form/99?extra%5B%27account%27%5D={}&amountInteger={}&amountFraction=0&extra%5B%27comment%27%5D={}&currency=643&blocked[0]=sum&blocked[2]=account"
	link = link.format(number, sum, comment)
	return link


def get_last_pay(qiwi_number, qiwi_token):
	url = "https://edge.qiwi.com/payment-history/v2/persons/{0}/payments".format(qiwi_number)
	headers = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": "Bearer " + qiwi_token}
	req = requests.get(url, params={"rows": 1, "operation": "IN"}, headers=headers)
	
	req = req.json()
	js = json.dumps(req)
	js = json.loads(js)
	description = js["data"][0]["comment"]
	sum = js["data"][0]["sum"]["amount"]

	return {"sum": sum, "description": description}






class DataBase:
	def __init__(self, path="DB.db"):
		self.con = sqlite3.connect(path)
		self.cursor = self.con.cursor()

	def close(self):
		self.con.commit()
		self.con.close()

	def search_user(self, chat_id):
		"""
		Поиск юзера по id
		В случае обнаруения возращает True(bool)
		Иначале False(bool)
		"""
		sql = "SELECT id, chat_id FROM Users WHERE chat_id = {}".format(chat_id)
		self.cursor.execute(sql)

		if self.cursor.fetchone() != None:
			resp = True
		else:
			resp = False

		return resp

	def new_user(self, chat_id, referer=None):
		"""
		Запись нового юзера
		"""
		self.cursor.execute("SELECT * FROM Users")
		id = len(self.cursor.fetchall()) + 1

		sql = "INSERT INTO Users VALUES (?, ?, ?, ?, ?)"
		values = (id, chat_id, 0, round(time.time()), referer)
		self.cursor.execute(sql, values)


	def get_all_users(self):
		sql = "SELECT * FROM Users"
		self.cursor.execute(sql)
		users = self.cursor.fetchall()
		return users