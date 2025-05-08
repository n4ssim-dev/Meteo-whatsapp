import requests
from dotenv import load_dotenv
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

load_dotenv()

# Then access them
API_KEY = os.getenv('API_KEY')
ACCOUNT_SID = os.getenv('ACCOUNT_SID')
AUTH_TOKEN = os.getenv('AUTH_TOKEN')
PHONE_NUMBER = os.getenv('PHONE_NUMBER')
FROM_PHONE = os.getenv('FROM_PHONE')
CONTENT_SID = os.getenv('CONTENT_SID')

OW_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"

# Coordonnées pour Paris
MY_LAT: float = 48.85
MY_LONG: float = 2.35

# Paramètre de la requête API
parameters = {
    'lat':MY_LAT,
    'lon':MY_LONG,
    'appid':API_KEY,
    'units':'metric',
    'lang':'fr',
    'cnt': 4
}

response = requests.get(OW_ENDPOINT,params=parameters)

if response.status_code == requests.codes.ok:
    data = response.json()
    weather_list = data["list"]
    hour = 9
    raining_hours = []
    is_raining = False
    # Vérifie si dans les 4 premiers élements de list (9h-21h) il pleut à un moment, auquel cas un message est envoyé
    for weather in weather_list:
        hour = int(weather["dt_txt"].split(" ")[1].split(":")[0])

        if int(weather["weather"][0]["id"]) < 700:
            is_raining = True
            raining_hours.append(hour)

            """
            Paramètre le proxy pour rendre le code runable sur python anywhere
            proxy_client = TwilioHttpClient()
            proxy_client.session.proxies = {'https': os.environ['https_proxy']} ---> Passer dans client : ,http_client=proxy_client
            """
            client = Client(ACCOUNT_SID, AUTH_TOKEN)

            # Envoie un Message whatsapp pour nous notifier du mauvais temps.
            message = client.messages.create(
                from_=FROM_PHONE,
                body=f"Il va pleuvoir à Paris à partir de {hour}h, prend un parapluie ⛈️",
                to=PHONE_NUMBER
            )
            break

else:
    print("Error: ", response.status_code, response.text)