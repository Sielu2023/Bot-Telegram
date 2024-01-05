import telebot

TOKEN = '6559521791:AAHitQ3bzkqIHPLKWRb0yWqctW53mRBlQdc'
ADMIN_ID = '276803858'

bot = telebot.TeleBot(TOKEN)

name = None
username = None
user1_mess = None
user2_mess = None
user3_mess = None
user_photo = None
user_city = None  # Добавляем переменную для хранения города

@bot.message_handler(commands=['start'])
def start_message(message):
    global name, username
    name = message.from_user.first_name
    username = message.from_user.username
    bot.send_message(message.chat.id, "Привет! Это бот для заявок. Чтобы подать заявку, заполните анкету.")
    form1(message)

def form1(message):
    bot.send_message(message.chat.id, "1. Как вас зовут?")
    bot.register_next_step_handler(message, form2)

def form2(message):
    global user1_mess
    user1_mess = message.text
    bot.send_message(message.chat.id, "2. Сколько вам лет?")
    bot.register_next_step_handler(message, form3)

def form3(message):
    global user2_mess
    user2_mess = message.text
    bot.send_message(message.chat.id, "3. Укажите номер телефона:")
    bot.register_next_step_handler(message, form4)

def form4(message):
    global user3_mess
    user3_mess = message.text
    bot.send_message(message.chat.id, "4. В каком городе вы живете?")
    bot.register_next_step_handler(message, form5)  # Переход к запросу города

def form5(message):
    global user_city
    user_city = message.text
    bot.send_message(message.chat.id, "5. Пришлите вашу фотографию (фото):")
    bot.register_next_step_handler(message, get_photo)

def get_photo(message):
    global user_photo
    try:
        if message.photo:
            user_photo = message.photo[-1].file_id
            send_application(message)

        else:
            bot.send_message(message.chat.id, "Извините, это не фотография. Пожалуйста, отправьте фотографию.")

    except Exception as e:
        bot.send_message(message.chat.id, "Извините, что-то пошло не так. Пожалуйста, отправьте фотографию еще раз.")

def send_application(message):
    global user_photo
    # Создаем HTML-разметку для сообщения
    application_text = f'''
    <b>Новая заявка от {name}:</b>
    - Имя: {user1_mess}
    - Возраст: {user2_mess}
    - Номер телефона: {user3_mess}
    - Город: {user_city}

    Telegram:
    - Имя: {name}
    - Username: @{username}
    '''

    # Отправляем сообщение с HTML-разметкой и фотографией администратору
    bot.send_photo(ADMIN_ID, user_photo, caption=application_text, parse_mode='HTML')

    # Опционально, отправляем пользователю уведомление о успешной заявке
    bot.send_message(message.chat.id, "Спасибо за заявку! Скоро наш менеджер свяжется с вами. Всего доброго!")

def admin_app(ADMIN_ID):
    ankets = f'''Новая заявка от {name}!
    Имя: {user1_mess}
    Возраст: {user2_mess}
    Номер телефона: {user3_mess}
    Город: {user_city}

    Telegram:
    Name: {name}
    Username: @{username}'''

    bot.send_message(ADMIN_ID, ankets)

bot.polling()
