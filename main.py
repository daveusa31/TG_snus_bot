import json
import config
import telebot
import functions
from telebot import types
import config as const
import requests




bot = telebot.TeleBot(config.TOKEN)
print("| Бот инициализирован.")



def send_in_group(text):
	if config.group_id != "":
		bot.send_message(config.group_id, text)
	else:
		bot.send_message(config.admin_id, text)

@bot.message_handler(commands=["start"])
def start_message(message):
	markup = types.ReplyKeyboardMarkup()
	markup.row("Каталог")
	markup.row("Обратная связь")
	markup.row("Тестовая оплата")

	bot.send_message(message.chat.id, "*Добро пожаловать в {}.*".format(config.BOT_NAME), reply_markup=markup, parse_mode="markdown")

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




@bot.message_handler(content_types=['text'])
def messages(message):
	chat_id = message.chat.id
	username = message.chat.username

	if message.text == "Обратная связь":
		markup = telebot.types.InlineKeyboardMarkup()
		button = telebot.types.InlineKeyboardButton(text='Cвязаться с менеджером', url="t.me/{}".format(config.manager))
		markup.row(button)
		bot.send_message(chat_id,"Возникли *вопросы?*\nНеобходима большая *партия снюса?*\n\nВоспользуйтесь кнопкой ниже для связи с менеджером.",reply_markup=markup, parse_mode='markdown')

	elif message.text == "Тестовая оплата":
		link = functions.get_payment_link(config.qiwi_number, 1)

		file = str(chat_id)+"last_pay.txt"
		markup = telebot.types.InlineKeyboardMarkup()
		button = telebot.types.InlineKeyboardButton(text='Перейти к оплате', callback_data='payment', url=link)
		button1 = telebot.types.InlineKeyboardButton(text='ОПЛАТИЛ', callback_data='check_test')
		markup.row(button)
		markup.row(button1)

		bot.send_message(chat_id,"*Для проверки оплаты перейдите по ссылке ниже, и после оплаты нажмите ОПЛАТИЛ*\n\n_Сумма оплаты: 1 руб._",parse_mode="markdown",reply_markup=markup)
		
		with open("history_payment/" + file, "w", encoding="utf-8") as f:
			pay_writer.write("1")

	elif "Каталог" == message.text:
		markup = types.ReplyKeyboardMarkup()
		element_list = ["Alfa","Arqa","Blax","Boshki","Nictech","Kurwa","Taboo"]
		for element in element_list:
			markup.row(element)
		markup.row("В меню")
		bot.send_message(chat_id, "Текст для каталога", reply_markup=markup)

	elif "Alfa" == message.text:
		markup = types.ReplyKeyboardMarkup()
		element_list = const.ALFA
		for element in element_list:
			markup.row(element)
		markup.row("В меню")
		bot.send_message(chat_id, "Каталог альфы", reply_markup=markup)

	elif "Arqa" == message.text:
		markup = types.ReplyKeyboardMarkup()
		element_list = const.ARQA
		for element in element_list:
			markup.row(element)
		markup.row("В меню")
		bot.send_message(chat_id, "Каталог арки", reply_markup=markup)

	elif "Blax" == message.text:
		markup = types.ReplyKeyboardMarkup()
		element_list = const.BLAX
		for element in element_list:
			markup.row(element)
		markup.row("В меню")
		bot.send_message(chat_id, "Каталог блакса", reply_markup=markup)

	elif "Boshki" == message.text:
		markup = types.ReplyKeyboardMarkup()
		element_list = const.BOSHKI
		for element in element_list:
			markup.row(element)
		markup.row("В меню")
		bot.send_message(chat_id, "Каталог бошки", reply_markup=markup)

	elif "Nictech" == message.text:
		markup = types.ReplyKeyboardMarkup()
		element_list = const.NICTECH
		for element in element_list:
			markup.row(element)
		markup.row("В меню")
		bot.send_message(chat_id, "Каталог никтех", reply_markup=markup)

	elif "Kurwa" == message.text:
		markup = types.ReplyKeyboardMarkup()
		element_list = const.KURWA
		for element in element_list:
			markup.row(element)
		markup.row("В меню")
		bot.send_message(chat_id, "Каталог курвы", reply_markup=markup)

	elif "Taboo" == message.text:
		markup = types.ReplyKeyboardMarkup()
		element_list = const.TABOO
		for element in element_list:
			markup.row(element)
		markup.row("В меню")
		bot.send_message(chat_id, "Каталог табу", reply_markup=markup)
		
	elif "В меню" == message.text:
		markup = types.ReplyKeyboardMarkup()
		markup.row("Каталог")
		markup.row("Обратная связь")
		markup.row("Тестовая оплата")
		bot.send_message(chat_id, "*Добро пожаловать в YourName bot.*\n", parse_mode="markdown", reply_markup=markup)

	#оплата
	elif "|Цена:" in message.text:
		splitter = message.text.split("|")

		good = message.text[:10]
		sum = message.text[-3:]

		if sum < "200":
			bot.send_message(chat_id, "Произошла ошибка. Попробуйте снова, или через пару минут.\n\nНаши специалисты уже начали поиск проблемы.", parse_mode="markdown")
		else:
			link = functions.get_payment_link(config.qiwi_number, sum, good)

			file = str(chat_id) + "last_pay.txt"
			markup = telebot.types.InlineKeyboardMarkup(row_width=1)
			button = telebot.types.InlineKeyboardButton(text='Перейти к оплате', callback_data='payment', url=link)
			button1 = telebot.types.InlineKeyboardButton(text='ОПЛАТИЛ', callback_data='check')
			markup.row(button)
			markup.row(button1)
			bot.send_message(chat_id, "Ваш заказ:\n_{}_\n_{}\n\n_Сумма оплаты: {}_{}"format(splitter[0], splitter[1], sum, config.A_T) parse_mode="markdown", reply_markup=markup)
			
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
			bot.send_message(chat_id, "*Ваша оплата успешно получена!*\n\n Полученный нами адрес:\n_{}_".format(last_payment["description"]), parse_mode="markdown")
			send_in_group("Получена оплата в размере - {}р".format(sum))

		# Оплаты нет
		else:
			bot.send_message(chat_id,"*К сожалению, ваша оплата пока не дошла до нас.*\n\n _Как только вы убедитесь в том что оплата успешно проведена, нажмите_ *ОПЛАТИТЬ*",parse_mode="markdown")

	elif call.data == "check_test":
		with open("history_payment/" + file, "r", encoding="utf-8") as f:
			sum = f.readline()

		
		last_payment = functions.get_last_pay(config.qiwi_number, config.qiwi_token)

		# Получена тестовая оплата
		if str(last_payment["sum"]) == str(sum):
			bot.send_message(chat_id, "*Ваша оплата успешно получена!*\n\n Полученный нами адрес:\n_{}_".format(last_payment["description"]), parse_mode="markdown")
			send_in_group("Получена тестовая оплата в размере - {}р".format(sum))

		# Не получена
		else:
			bot.send_message(chat_id,"К сожалению, ваша оплата пока не дошла до нас. Как только вы убедитесь в том что оплата успешно проведена, нажмите ОПЛАТИТЬ")



		

bot.polling()

