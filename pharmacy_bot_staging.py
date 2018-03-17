from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from commands import search, find_location_based, echo
from tokens import bottoken

t = bottoken
updater = Updater(token=t.token("staging"))
dispatcher = updater.dispatcher

search_pharmacies_handler_tr = CommandHandler('eczane', search, pass_args=True)
search_pharmacies_handler_en = CommandHandler('pharmacy', search, pass_args=True)
location_based_pharmacies_handler = MessageHandler(Filters.location, find_location_based)
echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(search_pharmacies_handler_tr)
dispatcher.add_handler(search_pharmacies_handler_en)
dispatcher.add_handler(location_based_pharmacies_handler)
dispatcher.add_handler(echo_handler)
updater.start_polling()
