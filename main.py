import config
import requests
import telebot
import functions
from telebot import types




bot = telebot.TeleBot(config.TOKEN)
print("| Бот инициализирован.")



def send_in_group(text):
	if config.group_id != "":
		bot.send_message(config.group_id, text)
	else:
		bot.send_message(config.admin_id, text)

@bot.message_handler(commands=["start"])
def start_message(message):
	markup = types.ReplyKeyboardMarkup(True, False)
	markup.row("Каталог")
	markup.row("Обратная связь")
	markup.row("Тестовая оплата")

	bot.send_message(message.chat.id, "<b>Добро пожаловать в {}.</b>".format(config.BOT_NAME), reply_markup=markup, parse_mode="HTML")

	DB = functions.DataBase()
	if DB.search_user(message.chat.id) == False:
		refka = message.text[7:]
		user_from_worker = str(message.from_user.username)

		# Без реффки
		if refka == "":
			send_in_group("Новый айди юзера - @{}".format(user_from_worker))

			DB.new_user(message.chat.id)

		# С реффкой
		else:
			send_in_group("Новый юзер от работника @{}, айди юзера - @{}".format(refka, user_from_worker))

			DB.new_user(message.chat.id, referer=refka)

			with open("baza.txt","a", encoding="utf-8") as f:
				f.write("@{} | @{}".format(refka, user_from_worker))
	
	DB.close()

@bot.message_handler(commands=["users"])
def all_users(message):
	if message.chat.id == config.admin_id:
		DB = functions.DataBase()
		users = DB.get_all_users()
		DB.close()

		for mes in users:
			bot.send_message(message.chat.id, mes)




@bot.message_handler(content_types=['text'])
def messages(message):
	chat_id = message.chat.id
	username = message.chat.username

	if message.text == "Обратная связь":
		markup = telebot.types.InlineKeyboardMarkup()
		button = telebot.types.InlineKeyboardButton(text='Cвязаться с менеджером', url="t.me/{}".format(config.manager))
		markup.row(button)
		bot.send_message(chat_id,"Возникли <b>вопросы?</b>\nНеобходима большая <b>партия снюса?</b>\n\nВоспользуйтесь кнопкой ниже для связи с менеджером.", reply_markup=markup, parse_mode='HTML')

	elif message.text == "Тестовая оплата":
		link = functions.get_payment_link(config.qiwi_number, 1)

		file = str(chat_id)+"last_pay.txt"
		markup = telebot.types.InlineKeyboardMarkup()
		button = telebot.types.InlineKeyboardButton(text='Перейти к оплате', callback_data='payment', url=link)
		button1 = telebot.types.InlineKeyboardButton(text='ОПЛАТИЛ', callback_data='check_test')
		markup.row(button)
		markup.row(button1)

		bot.send_message(chat_id,"<b>Для проверки оплаты перейдите по ссылке ниже, и после оплаты нажмите ОПЛАТИЛ</b>\n\n<i>Сумма оплаты: 1 руб.</i>", parse_mode="HTML", reply_markup=markup)
		
		with open("history_payment/" + file, "w", encoding="utf-8") as f:
			f.write("1")

	elif "Каталог" == message.text:
		markup = types.ReplyKeyboardMarkup(True, False)
		element_list = ["Alfa","Arqa","Blax","Boshki","Nictech","Kurwa","Taboo"]
		for element in element_list:
			markup.row(element)
		markup.row("В меню")
		bot.send_message(chat_id, "Текст для каталога", reply_markup=markup)

	elif "Alfa" == message.text:
		markup = types.ReplyKeyboardMarkup(True, False)
		element_list = config.ALFA
		for element in element_list:
			markup.row(element)
		markup.row("В меню")
		bot.send_message(chat_id, "Каталог альфы", reply_markup=markup)

	elif "Arqa" == message.text:
		markup = types.ReplyKeyboardMarkup(True, False)
		element_list = config.ARQA
		for element in element_list:
			markup.row(element)
		markup.row("В меню")
		bot.send_message(chat_id, "Каталог арки", reply_markup=markup)

	elif "Blax" == message.text:
		markup = types.ReplyKeyboardMarkup(True, False)
		element_list = config.BLAX
		for element in element_list:
			markup.row(element)
		markup.row("В меню")
		bot.send_message(chat_id, "Каталог блакса", reply_markup=markup)

	elif "Boshki" == message.text:
		markup = types.ReplyKeyboardMarkup(True, False)
		element_list = config.BOSHKI
		for element in element_list:
			markup.row(element)
		markup.row("В меню")
		bot.send_message(chat_id, "Каталог бошки", reply_markup=markup)

	elif "Nictech" == message.text:
		markup = types.ReplyKeyboardMarkup(True, False)
		element_list = config.NICTECH
		for element in element_list:
			markup.row(element)
		markup.row("В меню")
		bot.send_message(chat_id, "Каталог никтех", reply_markup=markup)

	elif "Kurwa" == message.text:
		markup = types.ReplyKeyboardMarkup(True, False)
		element_list = config.KURWA
		for element in element_list:
			markup.row(element)
		markup.row("В меню")
		bot.send_message(chat_id, "Каталог курвы", reply_markup=markup)

	elif "Taboo" == message.text:
		markup = types.ReplyKeyboardMarkup(True, False)
		element_list = config.TABOO
		for element in element_list:
			markup.row(element)
		markup.row("В меню")
		bot.send_message(chat_id, "Каталог табу", reply_markup=markup)
		
	elif "В меню" == message.text:
		markup = types.ReplyKeyboardMarkup(True, False)
		markup.row("Каталог")
		markup.row("Обратная связь")
		markup.row("Тестовая оплата")
		bot.send_message(chat_id, "<b>Добро пожаловать в {}.</b>".format(config.BOT_NAME), parse_mode="HTML", reply_markup=markup)

	#оплата
	elif "|Цена:" in message.text:
		splitter = message.text.split("|")

		good = message.text[:10]
		sum = message.text[-3:]

		if sum < "200":
			bot.send_message(chat_id, "Произошла ошибка. Попробуйте снова, или через пару минут.\n\nНаши специалисты уже начали поиск проблемы.", parse_mode="HTML")
		else:
			link = functions.get_payment_link(config.qiwi_number, sum, good)

			file = str(chat_id) + "last_pay.txt"
			markup = telebot.types.InlineKeyboardMarkup(row_width=1)
			button = telebot.types.InlineKeyboardButton(text='Перейти к оплате', callback_data='payment', url=link)
			button1 = telebot.types.InlineKeyboardButton(text='ОПЛАТИЛ', callback_data='check')
			markup.row(button)
			markup.row(button1)
			bot.send_message(chat_id, "Ваш заказ:\n<i>{}\n{}\n\n</i>Сумма оплаты: {}{}".format(splitter[0], splitter[1], sum, config.A_T), parse_mode="HTML", reply_markup=markup)
			
			with open("history_payment/" + file, "w", encoding="utf-8") as f:
				f.write(sum)




@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	chat_id = call.from_user.id
	file = str(chat_id) + "last_pay.txt"
	if call.data == "check":
		with open("history_payment/" + file, "r", encoding="utf-8") as f:
			sum = f.readline()
		

		last_payment = functions.get_last_pay(config.qiwi_number, config.qiwi_token)
		
		# Оплата прошла
		if str(last_payment["sum"]) == str(sum):
			bot.send_message(chat_id, "<b>Ваша оплата успешно получена!</b>\n\n Полученный нами адрес:\n<i>{}</i>".format(last_payment["description"]), parse_mode="HTML")
			send_in_group("Получена оплата в размере - {}р от юзера @{} с chat_id {}".format(sum, call.message.chat.username, chat_id))

			DB = functions.DataBase()
			DB.pay(chat_id, sum)
			DB.close()

		# Оплаты нет
		else:
			bot.send_message(chat_id,"<b>К сожалению, ваша оплата пока не дошла до нас.</b>\n\n <i>Как только вы убедитесь в том что оплата успешно проведена, нажмите</i> <b>ОПЛАТИТЬ</b>",parse_mode="HTML")

	elif call.data == "check_test":
		with open("history_payment/" + file, "r", encoding="utf-8") as f:
			sum = f.readline()

		
		last_payment = functions.get_last_pay(config.qiwi_number, config.qiwi_token)

		# Получена тестовая оплата
		if str(last_payment["sum"]) == str(sum):
			bot.send_message(chat_id, "<b>Ваша оплата успешно получена!</b>\n\n Полученный нами адрес:\n<i>{}</i>".format(last_payment["description"]), parse_mode="HTML")
			send_in_group("Получена тестовая оплата в размере - {}р от юзера @{} с chat_id {}".format(sum, call.message.chat.username, chat_id))

			DB = functions.DataBase()
			DB.pay(chat_id, sum)
			DB.close()

		# Не получена
		else:
			bot.send_message(chat_id,"К сожалению, ваша оплата пока не дошла до нас. Как только вы убедитесь в том что оплата успешно проведена, нажмите ОПЛАТИТЬ")



		

bot.polling()

