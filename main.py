import requests
import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

API_KEY = os.environ.get("OWM_API_KEY")
account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")

url = "https://api.openweathermap.org/data/2.5/forecast"

params = {
    "lat": 20.039657,
    "lon": -101.478589,
    "appid": API_KEY,
    "cnt": 4
}

response = requests.get(url, params=params)
response.raise_for_status()

weather_data = response.json()

will_rain = False

for item in weather_data["list"][:4]:
    weather_id = item["weather"][0]["id"]

    if weather_id < 700:
        will_rain = True
        break

if will_rain:
    client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
            body="It's going to rain today. Remember to bring an umbrella",
            from_="+19705781865",
            to="+524431463779"
        )

        print("Message status:", message.status)

    except TwilioRestException as e:
        print(f"Twilio error: {e}")

else:
    print("No rain expected.")
