import requests , os
from dotenv import load_dotenv
load_dotenv()

def getOne(id):
    fetch = requests.get(f"{os.getenv('URL')}/queue/waiting")
    fetch = fetch.json()
    data = False
    for item in fetch:
        if item['queueId'] == id:
          data = item['queueStatus']
    return data
def getData():
    data = []
    fetch = requests.get(f'{os.getenv("URL")}/queue')
    fetch = fetch.json()
    for item in fetch:
        if item['queueStatus'] != 'accommodated':
            data.append(item)
    return data
def updateData(id):
    getOneQueue = getOne(id)
    status ="ongoing" if getOneQueue == "waiting" else "accommodated"
    data = {"queueId": int(id), "queueStatus": status}
    headers = {'Content-Type': 'application/json'}
    fetch = requests.patch(f'{os.getenv("URL")}/queue', json=data, headers=headers)
    result = fetch.json()
    message = f"{result['name']} is now {result['queueStatus']}" if fetch.status_code==200 else "Something Went Wrong"
    return message

