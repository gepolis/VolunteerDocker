import requests
from django.conf import settings

if not requests.get(f"https://school1236.ru/school/{settings.TOKEN}").json().get("ok"):
    print("School token error!")
    exit(1)