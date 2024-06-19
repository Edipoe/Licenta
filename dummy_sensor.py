import json
import requests
import random



URL = "http://localhost:8000/post_sensor_values_ajax/"

for i in range(100):
    sensor_data = {
        "sensor_name": "dummy",
        "ecg_data": random.uniform(0.6, 1.4),
        "spo2_level": random.randint(960, 999) / 10,
        "heart_rate": random.randint(70, 120),
        "fall_detected": True,
    }

    response = requests.post(URL, json=sensor_data)
    
    print(f"Request #{i+1}")
    print(f"Request status code: {response.status_code}")
    print(f"Response text: {response.text}")
    try:
        response_data = response.json()
        print(f"Parsed response JSON: {response_data}")
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON response: {e}")
