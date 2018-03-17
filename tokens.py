_TELEGRAM_BOT_STAGING_TOKEN = ""
_TELEGRAM_BOT_LIVE_TOKEN = ""
_GOOGLE_API_KEY = ""

class bottoken():
    @staticmethod
    def token(x):
        if x == "staging":
            return _TELEGRAM_BOT_STAGING_TOKEN
        elif x == "live":
            return _TELEGRAM_BOT_LIVE_TOKEN


class SQL():
    @staticmethod
    def sqlinfo(x):
        if x == "host":
            return "localhost"
        elif x == "usn":
            return "<username>"
        elif x == "pw":
            return "<password>"
        elif x == "db":
            return "<dbname>"


class Google():
    @staticmethod
    def get_api_key(x):
        if x == "staging":
            return _GOOGLE_API_KEY


class errorchannel():
    @staticmethod
    def errorchannel(x):
        if x == "error":
            return "<error channel id>"  # id of the channel that you're using to broadcast your error messages
