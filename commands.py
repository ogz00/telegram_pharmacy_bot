import copy
import json

import telegram

from constants import system_message, languages
from models import User, location
from utils import google_geolocation_api_req, google_place_api_req, build_and_send_pharmacies_list, \
    build_fatality, answer_not_found, Common, find_lang


def search(bot, update, args):
    chat_id = -1
    try:
        chat_id = update.message.chat_id
        command = update.message.text
        lang = find_lang(command)
        serialized_user_message = json.dumps(update.message.to_dict(), indent="\t", sort_keys=True)
        Common.LOGGER().info("user message: %s" % serialized_user_message)
        if len(args) == 0:

            location_keyboard = telegram.KeyboardButton(text=system_message[lang]["send_location_btn"],
                                                        request_location=True)
            custom_keyboard = [[location_keyboard]]
            reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
            bot.send_message(chat_id=chat_id, text=system_message[lang]["send_location_prom"],
                             reply_markup=reply_markup)
        else:
            latitude, longitude = google_geolocation_api_req(str(args[0]).upper())
            results = google_place_api_req(latitude, longitude, lang)

            telegram_user = update.message.from_user
            curr_location = location(latitude, longitude)
            Common.LOGGER().info("Location of %s: %f / %f", telegram_user.first_name, curr_location.latitude,
                                 curr_location.longitude)

            user = User(telegram_user.first_name,
                        telegram_user.last_name if hasattr(telegram_user, "last_name") else "", telegram_user.username,
                        curr_location, lang)
            build_and_send_pharmacies_list(results, bot, chat_id, user)

    except:
        build_fatality(bot, update, chat_id)


def find_location_based(bot, update):
    chat_id = -1
    try:
        lang = languages["tr"] if update.message.text == system_message["tr"]["send_location_prom"] else "en"
        chat_id = copy.deepcopy(update.message.chat.id)
        serialized_location_message = json.dumps(update.message.to_dict(), indent="\t", sort_keys=True)
        Common.LOGGER().info("location message: %s" % serialized_location_message)

        telegram_user = update.message.from_user
        curr_location = location(update.message.location.latitude, update.message.location.longitude)

        Common.LOGGER().info("Location of %s: %f / %f", telegram_user.first_name, curr_location.latitude,
                             curr_location.longitude)

        user = User(telegram_user.first_name, telegram_user.last_name if hasattr(telegram_user, "last_name") else "",
                    telegram_user.username, curr_location, lang)

        results = google_place_api_req(curr_location.latitude, curr_location.longitude, lang)
        if results.json()["status"] == "ZERO_RESULTS":
            answer_not_found(bot, chat_id)
            return
        build_and_send_pharmacies_list(results, bot, chat_id, user)

    except:
        build_fatality(bot, update, chat_id)


def echo(bot, update):
    serialized_user_message = json.dumps(update.message.to_dict(), indent="\t", sort_keys=True)
    Common.LOGGER().info(serialized_user_message)
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)
