import requests
from bs4 import BeautifulSoup as bs
import sys

city = sys.argv[1]


def get_weather(place):
    place = place.replace(" ", "-")
    url = "https://www.weather-forecast.com/locations/" + place + "/forecasts/latest"
    r = requests.get(url)
    soup = bs(r.content, "lxml")
    weather = soup.findAll("span", {"class": "phrase"})[0].text
    return weather

#print(get_weather(city))
#print("the temperature is 25 degree Celsius")
print('{"quiz":{"sport":{"q1":{"question":"WhichoneiscorrectteamnameinNBA?","options":["NewYorkBulls","LosAngelesKings","GoldenStateWarriros","HustonRocket"],"answer":"HustonRocket"}},"maths":{"q1":{"question":"5+7=?","options":["10","11","12","13"],"answer":"12"},"q2":{"question":"12-8=?","options":["1","2","3","4"],"answer":"4"}}}}')
sys.stdout.flush()
