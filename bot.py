import json
import os

import telebot
from dotenv import load_dotenv
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

import downloader_yt
import utils

load_dotenv()
token = os.getenv("TG_TOKEN")
bot = telebot.TeleBot(token, parse_mode=None)

users = {}
user_example = {
    "without_caption": 0,
    "admin": 0
}

links = [
    "youtu.be",
    "youtube.com",
    "soundcloud.com"
]

def update_users_write():
    with open('./users.json', 'w', encoding='UTF-8') as write_users:
        json.dump(users, write_users, ensure_ascii=False, indent=4)


def update_users_read():
    global users
    if not os.path.isfile('./users.json'):
        update_users_write()
    else:
        with open("./users.json", 'r', encoding='UTF-8') as read_users:
            users = json.load(read_users)


def get_songs_list_markup(message, song_req, page_num):
    songs_list = []
    
    try:
        songs_list = downloader_yt.search_song(song_req, page_num)
    except Exception:
        bot.send_message(message.chat.id, "retarded...")
        return
    if not songs_list:
        bot.send_message(message.chat.id, "not found(")
        return
    
    markup = InlineKeyboardMarkup()
    for song in songs_list:
        song_name = "{} - {} {}".format(song['title'], song['artist'], song['duration'])
        markup.add(InlineKeyboardButton(
            song_name, callback_data=f"dwnldsong|{song['id']}"))
    markup.add(InlineKeyboardButton("<", callback_data="page_prev|{}|{}".format(song_req, page_num)),
                InlineKeyboardButton("X", callback_data="delmsg"),
                InlineKeyboardButton(">", callback_data="page_next|{}|{}".format(song_req, page_num)))
    
    return markup


def send_song(message, title, artist, filename):
    audio = open('./songs/{}'.format(filename), 'rb')
    caption = "[via](https://t.me/lyp1noff_music_bot)"
    if users[str(message.chat.id)]["without_caption"]:
        caption = ""
    bot.send_audio(
        message.chat.id, audio, caption=caption,
        title=title,
        performer=artist,
        parse_mode="MarkdownV2"
    )


def sign_user(message):
    if str(message.from_user.id) in users.keys():
        pass
    elif str(message.from_user.id) not in users.keys():
        users[str(message.from_user.id)] = user_example
        update_users_write()


@bot.message_handler(commands=['start'])
def start(message):
    sign_user(message)
    bot.reply_to(message, "Send me song name, son of bitch <3")


@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, "help urself))0)")


@bot.message_handler(commands=['stop'])
def stop(message):
    bot.reply_to(message, "ama unstoppable")


@bot.message_handler(commands=['switch_caption'])
def switch_caption(message):
    if users[str(message.from_user.id)]["without_caption"]:
        users[str(message.from_user.id)]["without_caption"] = 0
        bot.send_message(message.chat.id, "Caption enabled")
    else:
        users[str(message.from_user.id)]["without_caption"] = 1
        bot.send_message(message.chat.id, "Caption disabled")
    update_users_write()


@bot.message_handler(func=lambda m: True)
def msg_handler(message):
    sign_user(message)
    if any(ext in message.text for ext in links):
        msg = bot.send_message(message.chat.id, "downloading...")
        data = downloader_yt.download_sond_by_url(message.text)
        send_song(message, data[0], "", data[1])
        bot.delete_message(msg.chat.id, msg.id)
    else:
        markup = get_songs_list_markup(message, message.text, 1)
        if markup:
            bot.send_message(message.chat.id, "Choose one of 'em", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    message = call.message
    data = str(call.data).split("|")

    if "page" in data[0]:
        song_req = data[1]
        page_num = int(data[2])
        if data[0] == "page_prev":
            if page_num - 1 <= 0:
                bot.answer_callback_query(call.id, "it's already first page -_-")
                return
            markup = get_songs_list_markup(message, song_req, page_num - 1)
            bot.edit_message_text(
                "Choose one of 'em", message.chat.id, message.id, reply_markup=markup)
        elif data[0] == "page_next":
            # TODO dont send another search to check pages (store pages count)
            if not downloader_yt.search_song(song_req, page_num + 1):
                bot.answer_callback_query(call.id, "it's last page -_-")
                return
            markup = get_songs_list_markup(message, song_req, page_num + 1)
            bot.edit_message_text(
                "Choose one of 'em", message.chat.id, message.id, reply_markup=markup)
            
    elif data[0] == "delmsg":
        bot.delete_message(message.chat.id, message.id)

    elif data[0] == "dwnldsong":
        bot.answer_callback_query(call.id, "downloading")
        title, author = downloader_yt.get_song_metadata(data[1])
        filename = downloader_yt.download_song(f"{title}-{author}", data[1])
        send_song(message, title, author, filename)

    else:
        print("wrong callback data")


if __name__ == '__main__':
    update_users_read()
    utils.cleanup()
    print("Started")
    bot.infinity_polling()
