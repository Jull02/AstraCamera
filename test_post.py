import requests
from datetime import datetime

url = "http://localhost:5000/api/sesiones"

data = {
    "userId": "julissa.ruales",
    "timestamp": datetime.now().isoformat(),
    "leftElbow": 145.2,
    "rightElbow": 147.5,
    "leftKnee": 96.3,
    "rightKnee": 95.7,
    "prediccion": "correcto"
}

response = requests.post(url, json=data)
print(response.json())
