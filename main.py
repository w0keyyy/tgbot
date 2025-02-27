import telebot
from telebot import types
import random

bot = telebot.TeleBot('7595013592:AAGMHdGhfz7MaxGlyLEaCIJEZwlJN4XFIYA')

todo_list = []  

random_facts = [
    "⚡ Молния ударяет в Землю около 100 раз в секунду.",
    "🐘 Слоны могут узнавать себя в зеркале.",
    "🦈 Акулы существовали на Земле раньше, чем деревья.",
    "🌌 Вселенная расширяется быстрее, чем скорость света.",
    "🚀 В космосе нельзя слышать звуки из-за отсутствия атмосферы."
] * 20  

quiz_questions = {
    "❓ Сколько костей в человеческом теле?": "206",
    "🎵 Кто написал 9-ю симфонию?": "Бетховен",
    "⚽ Какая страна выиграла первый чемпионат мира по футболу?": "Уругвай",
    "🔬 Кто открыл закон всемирного тяготения?": "Ньютон",
    "📖 Какой самый продаваемый роман в мире?": "Дон Кихот"
}  

motivational_quotes = [
    "🔥 Никогда не сдавайся, потому что успех может быть за углом.",
    "💡 Великие вещи начинаются с маленьких шагов.",
    "🚀 Единственный способ достичь невозможного — это поверить, что оно возможно.",
    "🏆 Ты не проиграешь, если не сдашься.",
    "🌟 Успех — это 1% таланта и 99% труда."
] * 20  

user_quiz_answers = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Поздороваться")
    btn2 = types.KeyboardButton("Показать список дел")
    btn3 = types.KeyboardButton("Добавить задачу")
    btn4 = types.KeyboardButton("Удалить задачу")
    btn5 = types.KeyboardButton("Список команд")

    markup.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_message(message.chat.id, "Привет, я телеграм бот🤖", reply_markup=markup)

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(
        message.chat.id,
        "<b>Список доступных команд</b>\n"
        "/start - Приветствие\n"
        "/help - Описание команд\n"
        "/todo - Добавление и просмотр задач\n"
        "/schedule - Расписание на неделю\n"
        "/random_fact - Интересный факт\n"
        "/quiz - Викторина\n"
        "/motivation - Мотивация",
        parse_mode='HTML'
    )

@bot.message_handler(commands=['todo'])
def todo(message):
    if todo_list:
        bot.send_message(message.chat.id, "📌 Твои текущие задачи:\n" + "\n".join(todo_list))
    else:
        bot.send_message(message.chat.id, "✅ У тебя пока нет задач!")

@bot.message_handler(commands=['schedule'])
def schedule(message):
    schedule_text = (
        "📅 Расписание на неделю:\n"
        "1️⃣ Понедельник – зал\n"
        "2️⃣ Вторник – чилл\n"
        "3️⃣ Среда – зал\n"
        "4️⃣ Четверг – чилл\n"
        "5️⃣ Пятница – зал\n"
        "6️⃣ Суббота – шаг+чилл\n"
        "7️⃣ Воскресенье – чилл"
    )
    bot.send_message(message.chat.id, schedule_text)

@bot.message_handler(commands=['random_fact'])
def random_fact(message):
    fact = random.choice(random_facts)
    bot.send_message(message.chat.id, f"🔎 Интересный факт:\n{fact}")

@bot.message_handler(commands=['quiz'])
def quiz(message):
    question, answer = random.choice(list(quiz_questions.items()))
    user_quiz_answers[message.chat.id] = answer.lower()  
    bot.send_message(message.chat.id, f"🧠 Вопрос викторины:\n{question}")
    bot.register_next_step_handler(message, check_quiz_answer)

def check_quiz_answer(message):
    correct_answer = user_quiz_answers.get(message.chat.id, "").lower()
    user_answer = message.text.strip().lower()

    if user_answer == correct_answer:
        bot.send_message(message.chat.id, "✅ Правильно! Отличная работа!")
    else:
        bot.send_message(message.chat.id, f"❌ Неправильно. Правильный ответ: {correct_answer.capitalize()}")

@bot.message_handler(commands=['motivation'])
def motivation(message):
    quote = random.choice(motivational_quotes)
    bot.send_message(message.chat.id, f"🌟 Мотивация на сегодня:\n{quote}")

@bot.message_handler(content_types=['text'])
def get_message(message):
    if message.text == 'Поздороваться':
        bot.send_message(message.chat.id, "Привет✌️")
        bot.send_message(message.chat.id, "Нажми другую кнопку, чтобы продолжить.")

    elif message.text == 'help' or message.text == 'Список команд':
        help_command(message)

    elif message.text == 'Показать список дел':
        todo(message)

    elif message.text == 'Добавить задачу':
        send = bot.send_message(message.chat.id, '📝 Впиши новую задачу:')
        bot.register_next_step_handler(send, add_task)

    elif message.text == 'Удалить задачу':
        send = bot.send_message(message.chat.id, '🗑 Напиши задачу, которую хочешь удалить:')
        bot.register_next_step_handler(send, remove_task)

    elif message.text.lower() in ['расписание', '/schedule']:
        schedule(message)

    else:
        bot.send_message(message.chat.id, "🤷‍♂️ Я не понимаю вашу команду, нажмите другую кнопку")

def add_task(message):
    todo_list.append(message.text)
    bot.send_message(message.chat.id, f"✅ Задача '{message.text}' добавлена!")

def remove_task(message):
    task = message.text
    if task in todo_list:
        todo_list.remove(task)
        bot.send_message(message.chat.id, f"🗑 Задача '{task}' удалена!")
    else:
        bot.send_message(message.chat.id, f"❌ Задача '{task}' не найдена в списке!")

bot.polling(none_stop=True)
