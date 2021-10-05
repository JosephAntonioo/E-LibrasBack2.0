import requests

BASE = "http://192.168.0.10:5000/post"

response = requests.post(BASE, files={'image': open('hand.jpg', 'rb')})
print(response.json())
