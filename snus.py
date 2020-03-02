import telebot
from telebot import types
import const
import json
import requests

group_id = "" #айди группы для оповещений
number = "" #номер киви
qiwi_token = "" #токен киви для просмотра истории 
r_k = True
bot = telebot.TeleBot(const.TOKEN) #в модуле const.py заполняем переменную TOKEN, токеном от тг бота
print("| Бот инициализирован.")
markdown = const.MARKDOWN


def get_payment_link(pay,number):
	payment = "https://qiwi.com/payment/form/99?extra%5B%27account%27%5D="+number+"&amountInteger=" + pay + "&amountFraction=0&extra%5B%27comment%27%5D=Alfa%7CCold%7C%D0%9A%D0%BE%D0%BA%D0%BE%D1%81&currency=643&blocked[0]=sum&blocked[1]=comment&blocked[2]=account"
	return payment


@bot.message_handler(content_types=['text'])



def messages(message):
	userid = message.from_user.id
	username = message.from_user.username
	print(message.text + " | @" + username)
	if "/start" in message.text:
		markup = types.ReplyKeyboardMarkup(r_k)
		markup.row("Каталог")
		markup.row("Обратная связь")
		markup.row("Тестовая оплата")

		msg = message.text
		refka = msg[7:]
		user_from_worker = str(message.from_user.username)
		if refka == "":
			bot.send_message(group_id,"Новый айди юзера - @" + user_from_worker)
		if refka != "":
			bot.send_message(group_id,"Новый юзер от работника @" +refka + ", айди юзера - @" + user_from_worker)
			base_of_users = open("baza.txt","a")
			base_of_users.write("\n@" + refka + "|" + "@" + user_from_worker)

		bot.send_message(userid,"*Добро пожаловать в YourName bot.*\n",reply_markup=markup,parse_mode="markdown")

	if message.text == "Обратная связь":
		markup = telebot.types.InlineKeyboardMarkup(row_width=1)
		button = telebot.types.InlineKeyboardButton(text='Cвязаться с менеджером', callback_data='connect_to_manage', url="t.me/imogokuru1")
		markup.row(button)
		bot.send_message(userid,"Возникли *вопросы?*\nНеобходима большая *партия снюса?*\n\nВоспользуйтесь кнопкой ниже для связи с менеджером.",reply_markup=markup, parse_mode='markdown')

	if message.text == "Тестовая оплата":
		file = str(userid)+"last_pay.txt"
		link = get_payment_link(pay=1,number)
		markup = telebot.types.InlineKeyboardMarkup(row_width=1)
		button = telebot.types.InlineKeyboardButton(text='Перейти к оплате', callback_data='payment', url=link)
		button1 = telebot.types.InlineKeyboardButton(text='ОПЛАТИЛ', callback_data='check_test')
		markup.row(button)
		markup.row(button1)

		bot.send_message(userid,"*Для проверки оплаты перейдите по ссылке ниже, и после оплаты нажмите ОПЛАТИЛ*\n\n_Сумма оплаты: 1 руб._",parse_mode="markdown",reply_markup=markup)
		pay_writer = open("history_payment/" + file,"w")
		pay = 1
		pay_writer.write(str(pay))

	if "Каталог" == message.text:
		markup = types.ReplyKeyboardMarkup(r_k)
		element_list = ["Alfa","Arqa","Blax","Boshki","Nictech","Kurwa","Taboo"]
		for element in element_list:
			markup.row(element)
		markup.row("В меню")
		bot.send_message(userid,"Текст для каталога",reply_markup = markup)

	if "Alfa" == message.text:
		markup = types.ReplyKeyboardMarkup(r_k)
		element_list = const.ALFA
		for element in element_list:
			markup.row(element)
		markup.row("В меню")
		bot.send_message(userid,"Каталог альфы",reply_markup = markup)

	if "Arqa" == message.text:
		markup = types.ReplyKeyboardMarkup(r_k)
		element_list = const.ARQA
		for element in element_list:
			markup.row(element)
		markup.row("В меню")
		bot.send_message(userid,"Каталог арки",reply_markup = markup)

	if "Blax" == message.text:
		markup = types.ReplyKeyboardMarkup(r_k)
		element_list = const.BLAX
		for element in element_list:
			markup.row(element)
		markup.row("В меню")
		bot.send_message(userid,"Каталог блакса",reply_markup = markup)

	if "Boshki" == message.text:
		markup = types.ReplyKeyboardMarkup(r_k)
		element_list = const.BOSHKI
		for element in element_list:
			markup.row(element)
		markup.row("В меню")
		bot.send_message(userid,"Каталог бошки",reply_markup = markup)

	if "Nictech" == message.text:
		markup = types.ReplyKeyboardMarkup(r_k)
		element_list = const.NICTECH
		for element in element_list:
			markup.row(element)
		markup.row("В меню")
		bot.send_message(userid,"Каталог никтех",reply_markup = markup)

	if "Kurwa" == message.text:
		markup = types.ReplyKeyboardMarkup(r_k)
		element_list = const.KURWA
		for element in element_list:
			markup.row(element)
		markup.row("В меню")
		bot.send_message(userid,"Каталог курвы",reply_markup = markup)

	if "Taboo" == message.text:
		markup = types.ReplyKeyboardMarkup(r_k)
		element_list = const.TABOO
		for element in element_list:
			markup.row(element)
		markup.row("В меню")
		bot.send_message(userid,"Каталог табу",reply_markup = markup)
		
	if "В меню" == message.text:
		markup = types.ReplyKeyboardMarkup(r_k)
		markup.row("Каталог")
		markup.row("Обратная связь")
		markup.row("Тестовая оплата")
		bot.send_message(userid,"*Добро пожаловать в YourName bot.*\n",parse_mode="markdown",reply_markup=markup)

	#оплата
	if "|Цена:" in message.text:
		splitter = message.text.split("|")

		pay = message.text[-3:]
		if pay < "200":
			bot.send_message(userid,"Произошла ошибка. Попробуйте снова, или через пару минут.\n\nНаши специалисты уже начали поиск проблемы.",parse_mode="markdown")
		else:
			file = str(userid)+"last_pay.txt"
			link = get_payment_link(pay,number)
			markup = telebot.types.InlineKeyboardMarkup(row_width=1)
			button = telebot.types.InlineKeyboardButton(text='Перейти к оплате', callback_data='payment', url=link)
			button1 = telebot.types.InlineKeyboardButton(text='ОПЛАТИЛ', callback_data='check')
			markup.row(button)
			markup.row(button1)

			bot.send_message(userid,"Ваш заказ:\n_"+splitter[0]+"_\n_"+splitter[1]+"\n\n_Сумма оплаты: "+str(pay)+"_"+const.A_T,parse_mode="markdown",reply_markup=markup)
			pay_writer = open("history_payment/" + file,"w")
			pay_writer.write(str(pay))


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	userid = call.from_user.id
	file = str(userid)+"last_pay.txt"
	if call.data == "check":
		pay = open("history_payment/"+file,"r").readline()
		
		url = "https://edge.qiwi.com/payment-history/v2/persons/{0}/payments".format(str(qiwi))
		headers = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": "Bearer " + qiwi_token}
		req = requests.get(url, params={"rows": 1, "operation": "IN"}, headers = headers)
		if req.status_code == 200:
			req = req.json()

		js = json.dumps(req)
		js = json.loads(js)
		description = js["data"][0]["comment"]
		payment_last = js["data"][0]["sum"]["amount"]
		
		
		if str(payment_last) == str(pay):

			bot.send_message(userid,"*Ваша оплата успешно получена!*\n\n Полученный нами адрес:\n_"+str(description)+"_",parse_mode="markdown")
			bot.send_message(group_id,"Получена оплата в размере - "+str(pay))
		if str(payment_last) != str(pay):
			print(payment_last,pay)
			bot.send_message(userid,"*К сожалению, ваша оплата пока не дошла до нас.*\n\n _Как только вы убедитесь в том что оплата успешно проведена, нажмите_ *ОПЛАТИТЬ*",parse_mode="markdown")

	if call.data == "check_test":
		pay = open("history_payment/"+file,"r").readline()
		bot.send_message(userid,"1")
		

		
		url = "https://edge.qiwi.com/payment-history/v2/persons/{0}/payments".format(str(qiwi))
		headers = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": "Bearer " + qiwi_token}
		req = requests.get(url, params={"rows": 1, "operation": "IN"}, headers = headers)
		if req.status_code == 200:
			req = req.json()

		js = json.dumps(req)
		js = json.loads(js)
		description = js["data"][0]["comment"]
		payment_last = js["data"][0]["sum"]["amount"]
		
		
		
		if str(payment_last) == str(pay):
			bot.send_message(userid,"*Ваша оплата успешно получена!*\n\n Полученный нами адрес:\n_"+str(description)+"_",parse_mode="markdown")
			bot.send_message(group_id,"Получена оплата в размере - "+str(pay))
		if str(payment_last) != str(pay):
			bot.send_message(userid,"К сожалению, ваша оплата пока не дошла до нас. Как только вы убедитесь в том что оплата успешно проведена, нажмите ОПЛАТИТЬ")



		

bot.polling(none_stop=True,interval=0)

