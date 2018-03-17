import logging
import traceback
from math import radians, sin, cos, atan2, sqrt

import googlemaps
import requests
import telegram
from telegram import ReplyKeyboardRemove

from constants import GOOGLE_PLACES_API, GOOGLE_PLACES_API_ID, system_message, HTML_TEMPLATES, COMMANDS, KEYWORDS
from helpers import SizedTimedRotatingFileHandler
from models import pharmacy, pharmacy_details, location
from tokens import Google

# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     level=logging.INFO)
# LOGGER = logging

google_key = Google.get_api_key("staging")
gmaps = googlemaps.Client(key=google_key)


class Common:
    __logger__ = None
    __smslogger__ = None
    __msglogger__ = None

    def __init__(self):
        pass

    @classmethod
    def LOGGER(cls):
        if cls.__logger__ is None:
            # logger for logging
            print("Pharmacy BotInitializing Logger...")

            handler = SizedTimedRotatingFileHandler(filename="pharmacy_bot.log",
                                                    maxBytes=1 * 1024 * 1024 * 50,
                                                    backupCount=5, when='midnight', utc=True)

            handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(component)s - %(message)s')
            handler.setFormatter(formatter)
            logger_static = logging.getLogger("logger")
            logger_static.setLevel(logging.DEBUG)
            logger_static.addHandler(handler)

            logger_extra = {'component': "pharmacy bot"}
            cls.__logger__ = logging.LoggerAdapter(logger_static, logger_extra)
            cls.__logger__.info("******************* Logger Initialized *******************")
            cls.__logger__.propagate = False
            print("Common Log Initialized...")

        return cls.__logger__


def build_answer(pharmacy_results, user):
    lang = user.language
    place_url_list = []
    pharmacy_list = [
        pharmacy(item["place_id"], item["name"], build_location_from_google(item)) for item in pharmacy_results]

    pharmacy_place_link_list = [GOOGLE_PLACES_API_ID.format(pharma.place_id, google_key) for pharma in pharmacy_list]

    if len(pharmacy_place_link_list) == 0:
        return system_message["no_pharmacy_found"]
    max_size = 8 if len(pharmacy_place_link_list) > 7 else len(pharmacy_place_link_list)
    for place_link in pharmacy_place_link_list[:max_size]:
        Common.LOGGER().info("place link: {0}".format(place_link))
        r = requests.get(place_link)
        if r.status_code == 200:
            if r.json()["status"] == "NOT_FOUND":
                max_size += 1
                continue
            place_json = r.json()["result"]
            place_url = place_json["url"]
            place_id = place_json["place_id"]
            phone = place_json["formatted_phone_number"] if "formatted_phone_number" in place_json else ""
            place_name = place_json["name"]
            place_location = build_location_from_google(place_json)
            place_address = place_json["formatted_address"] if "formatted_address" in place_json else ""
            place_distance = calculate_distance_between_locations(place_location, user.location)
            place_url_list.append(
                pharmacy_details(place_id, place_name, place_address, place_location, phone, place_url, place_distance))

    place_url_list = sorted(place_url_list, key=lambda k: k.distance)

    pharmacy_answer_list = '\n\n'.join(
        [HTML_TEMPLATES["pharmacy_detail"].format(ph.url, ph.name, ph.distance,
                                                  ph.address, ph.phone)
         for ph in place_url_list])

    return system_message[lang]["explanation_nearby"].format(user.first_name) + pharmacy_answer_list


def build_and_send_pharmacies_list(results, bot, chat_id, user):
    lang = user.language
    if results.status_code == 200:
        bot.sendMessage(chat_id=chat_id, text=system_message[lang]["wait_for_response"],
                        parse_mode='Markdown', reply_markup=ReplyKeyboardRemove())
        answer = build_answer(results.json()["results"], user)
        bot.send_message(chat_id=chat_id, text=answer, parse_mode=telegram.ParseMode.HTML,
                         reply_markup=ReplyKeyboardRemove())


def build_fatality(bot, update, chat_id):
    catcherror = traceback.format_exc()
    Common.LOGGER().error(catcherror)
    info = update.message.from_user
    bot.sendMessage(chat_id=chat_id, text=system_message["error_message"],
                    parse_mode='Markdown', reply_markup=ReplyKeyboardRemove())


def build_location_from_google(item):
    return location(item["geometry"]["location"]["lat"],
                    item["geometry"]["location"]["lng"])


def google_place_api_req(latitude, longitude, lang):
    geo_loc = "{0},{1}".format(latitude, longitude)
    url = GOOGLE_PLACES_API.format(geo_loc, KEYWORDS[lang]["pharmacy"], google_key)
    Common.LOGGER().info("place_api url: {0}".format(url))
    return requests.get(url)


def google_geolocation_api_req(search_text):
    geocode_result = gmaps.geocode(search_text)
    geocode = geocode_result[0]
    location = geocode["geometry"]["location"]
    return location["lat"], location["lng"]


def answer_not_found(bot, chat_id):
    bot.sendMessage(chat_id=chat_id, text=system_message["no_pharmacy_found"],
                    parse_mode='Markdown', reply_markup=ReplyKeyboardRemove())


def calculate_distance_between_locations(loc1, loc2):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(loc1.latitude)
    lon1 = radians(loc1.longitude)
    lat2 = radians(loc2.latitude)
    lon2 = radians(loc2.longitude)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


def find_lang(text):
    return COMMANDS[text]
