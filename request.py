import requests

fetch = requests.get('http://192.168.50.162:3000/queue')

# Check if the request was successful (status code 200)
def getData():
    if fetch.status_code == 200:
        data = fetch.json()  # Use json() method directly on the Response object
    else:
        print(f"Error: {fetch.status_code}")
    return data

