GOOGLE_PLACES_API = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={0}&radius=6000&type=pharmacy&keyword={1}&key={2}"
GOOGLE_PLACES_API_ID = "https://maps.googleapis.com/maps/api/place/details/json?placeid={0}&key={1}"

system_message = {
    "en": {
        "error_message": """Something has gone wrong. An error log has been generated, please try again to \"/eczane \" command or use command with your location like "
                         \"/eczane çankaya,ankara\"""",
        "wait_for_response": "Please wait search is continue, I'll redirect the results to you in seconds",
        "explanation_nearby": "Hi {0}, Here is the neariest pharmacy for your location: \n",
        "no_pharmacy_found": "I can't be able to found any pharmacy 6km about to your location.",
        "send_location_btn": "Send  My Location",
        "send_location_prom": "Can you please share your location with me?"
    },
    "tr": {
        "error_message": """Birşeyler ters gitti ve bunun bilgisi kaydedildi, lütfen tekrar \"/eczane \" komutunu deneyiniz ya da özel bir konum ile beraber 
        \"/eczane çankaya,ankara\" komutunu kullanabilirsiniz.""",
        "wait_for_response": "Lütfen bekleyiniz, arama devam ediyor, saniyeler içinde sonuçları size yönlendireceğim..",
        "explanation_nearby": "Merhaba {0}, işte size en yakın Eczanelerin listesi \n",
        "no_pharmacy_found": "Belirttiğiniz konumun 6 km  çevresinde eczane bulmayı başaramadım.",
        "send_location_btn": "Konum Paylaş",
        "send_location_prom": "Lütfen konumunuzu benimle paylaşın?"
    }
}

COMMANDS = {
    "/pharmacy": "en",
    "/eczane": "tr"
}

KEYWORDS = {
    "tr": {
        "pharmacy": "eczane"
    },
    "en": {
        "pharmacy": "pharmacy"
    }
}

HTML_TEMPLATES = {
    "pharmacy_detail": """<a href=\"{0}\">{1}</a> (<b>{2:.2f} km </b>)
    <i>Address: {3} \n Phone: {4}</i>"""
}

languages = {
    "tr": "tr",
    "en": "en"
}
