import requests
import random
import json

def make_data():
    req_url = "https://sturdy-rotary-phone-wwrq465rppwcg5r9-5000.app.github.dev/api/cars"

    for i in range(1, 101):
        if i <= 33:
            brand = 'Honda'
        elif i <= 66:
            brand = 'Ford'
        else:
            brand = 'BMW'

        model = brand + ' ' + str(i)
        transmission = 'AUTOMATIC' if i % 2 != 0 else 'MANUAL'
        price = random.randint(30000, 80000)
        release_year = 2020 + (i % 3)

        payload = {
            "brand": brand,
            "model": model,
            "transmission": transmission,
            "price": price,
            "release_year": f"{release_year}-01-01T00:00:00"
        }

        response = requests.post(req_url, json=payload)
        if response.status_code != 201:
            print(f"Failed to add {model}: {response.status_code}, {response.text}")
        else:
            print(f"Added {model} successfully")

make_data()
