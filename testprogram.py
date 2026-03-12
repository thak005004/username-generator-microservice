import requests

url = "http://127.0.0.1:5002/generate_name"

data = {
    "theme": "space"
}

response = requests.post(url, json=data)

print("Status code:", response.status_code)
print("Response JSON:", response.json())