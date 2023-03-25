import telebot
from telebot import types

TOKEN = ''
bot = telebot.TeleBot(TOKEN)

ideas = []
tasks = []

def create_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Добавить идею", "Добавить дело")
    keyboard.add("Показать идеи", "Показать дела")
    keyboard.add("Удалить идею", "Удалить дело")
    return keyboard

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Добро пожаловать! Выберите действие:", reply_markup=create_keyboard())

@bot.message_handler(func=lambda message: message.text == "Добавить идею")
def add_idea(message):
    msg = bot.send_message(message.chat.id, "Введите идею:")
    bot.register_next_step_handler(msg, save_idea)

def save_idea(message):
    ideas.append(message.text)
    bot.send_message(message.chat.id, "Идея добавлена.", reply_markup=create_keyboard())

@bot.message_handler(func=lambda message: message.text == "Добавить дело")
def add_task(message):
    msg = bot.send_message(message.chat.id, "Введите дело:")
    bot.register_next_step_handler(msg, save_task)

def save_task(message):
    tasks.append(message.text)
    bot.send_message(message.chat.id, "Дело добавлено.", reply_markup=create_keyboard())

@bot.message_handler(func=lambda message: message.text == "Показать идеи")
def show_ideas(message):
    if ideas:
        response = "\n".join(f"{i+1}. {idea}" for i, idea in enumerate(ideas))
        bot.send_message(message.chat.id, f"Список идей:\n{response}")
    else:
        bot.send_message(message.chat.id, "Список идей пуст.")

@bot.message_handler(func=lambda message: message.text == "Показать дела")
def show_tasks(message):
    if tasks:
        response = "\n".join(f"{i+1}. {task}" for i, task in enumerate(tasks))
        bot.send_message(message.chat.id, f"Список дел:\n{response}")
    else:
        bot.send_message(message.chat.id, "Список дел пуст.")

@bot.message_handler(func=lambda message: message.text == "Удалить идею")
def remove_idea(message):
    if ideas:
        msg = bot.send_message(message.chat.id, "Введите номер идеи для удаления:")
        bot.register_next_step_handler(msg, delete_idea)
    else:
        bot.send_message(message.chat.id, "Список идей пуст.")

def delete_idea(message):
    try:
        index = int(message.text) - 1
        if 0 <= index < len(ideas):
            del ideas[index]
            bot.send_message(message.chat.id, "Идея удалена.", reply_markup=create_keyboard())
        else:
            bot.send_message(message.chat.id, "Неверный номер идеи.")
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите корректный номер идеи.")

@bot.message_handler(func=lambda message: message.text == "Удалить дело")
def remove_task(message):
    if tasks:
        msg = bot.send_message(message.chat.id, "Введите номер дела для удаления:")
        bot.register_next_step_handler(msg, delete_task)
    else:
        bot.send_message(message.chat.id, "Список дел пуст.")

def delete_task(message):
    try:
        index = int(message.text) - 1
        if 0 <= index < len(tasks):
            del tasks[index]
            bot.send_message(message.chat.id, "Дело удалено.", reply_markup=create_keyboard())
        else:
            bot.send_message(message.chat.id, "Неверный номер дела.")
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите корректный номер дела.")

bot.polling(none_stop=True)

