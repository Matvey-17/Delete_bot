import telebot

from api_token import API_TOKEN

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    bot.send_message(message.chat.id,
                     f'Привет! Я помогу удалить "непослушных" пользователей ❌\n\n'
                     f'{telebot.formatting.hbold('Список команд:')}\n/start - начать\n'
                     f'/help - помощь\n/delete - удалить пользователя',
                     parse_mode='HTML')


@bot.message_handler(commands=['delete'])
def delete_user(message: telebot.types.Message):
    try:
        if bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id).status == 'left':
            bot.send_message(message.chat.id, 'Пользователь уже удален ✅')
        else:
            if bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id).status in ['creator',
                                                                                                      'administrator']:
                bot.send_message(message.chat.id, 'Нельзя удалять админов или создателя группы 🙅‍♂️')
            elif bot.get_chat_member(message.chat.id, message.from_user.id).status in ['creator', 'administrator']:
                bot.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id)
                bot.send_message(message.chat.id,
                                 f'Пользователь @{message.reply_to_message.from_user.username} удален 🗑')
            else:
                bot.send_message(message.chat.id, 'Вы не являетесь админом или создателем группы ❌')
    except AttributeError:
        with open('/Users/matveyvarlamov/cours_umschool/delete_bot/img/instance.png', 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption='Пример удаления пользователя')


if __name__ == '__main__':
    bot.infinity_polling()
