import os
import requests
import datetime
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.environ.get("APP_ID")
APP_KEY = os.environ.get("APP_KEY")
GENDER = os.environ.get("GENDER")
WEIGHT_KG = os.environ.get("WEIGHT_KG")
HEIGHT_CM = os.environ.get("HEIGHT_CM")
AGE = os.environ.get("AGE")
OAUTH = os.environ.get("OAUTH")

NUTRITIONIX_ENDPOINT=  "https://trackapi.nutritionix.com/v2/natural/exercise"
SHEETY_ENDPOINT = "https://api.sheety.co/6240a87d3f8d3cfa8256bd3eb0754ba0/myWorkouts/workouts"

header = {
    "x-app-id" : APP_ID,
    "x-app-key" : APP_KEY,
}
params = {
    # "query" : "Ran 5 km and cycled 1 km",
    "query" : input("Tell me which exercise you did: "),
    "weight_kg" : WEIGHT_KG,
    "height_cm" : HEIGHT_CM,
    "age" : AGE
}

response = requests.post(url= NUTRITIONIX_ENDPOINT, json= params, headers= header)
result = response.json()

today_date = datetime.datetime.now().strftime("%d/%m/%Y")
now_time = datetime.datetime.now().strftime("%X")
# %X	Local version of time	17:41:00
today = datetime.datetime.today()

for every_workout in result["exercises"]:
    basic_auth = {
        "Authorization" : f"{OAUTH}"
    }

    workout_params = {
        "workout" : {
            "date" : today_date,
            "time" : now_time,
            "exercise" : every_workout["name"].title(),
            "duration" : float(every_workout["duration_min"]),
            "calories" : every_workout["nf_calories"]
            }
    }

    print(workout_params)
    # print(every_workout["duration_min"])
    sheety_response = requests.post(url= SHEETY_ENDPOINT, json= workout_params, headers= basic_auth)
    # sheety_response = requests.post(url= SHEETY_ENDPOINT, json= workout_params, headers= bearer_auth)
    print(sheety_response.text)