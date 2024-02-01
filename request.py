import requests  

def getOne(id):
    fetch = requests.get(f'http://192.168.50.162:3000/queue/waiting')
    fetch = fetch.json()
    data = False
    for item in fetch:
        if item['queueId'] == id:
          data =True
    return data
def getData():
    fetch = requests.get('http://192.168.50.162:3000/queue/waiting')
    return fetch.json()
def updateData(id):
    data = {"queueId": int(id), "queueStatus": "accommodated"}
    headers = {'Content-Type': 'application/json'}
    fetch = requests.patch('http://192.168.50.162:3000/queue', json=data, headers=headers)
    result = fetch.json()
    message = f"{result['name']} is now {result['queueStatus']}" if fetch.status_code==200 else "Something Went Wrong"
    return message

