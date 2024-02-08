import requests , os, configparser

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

def getOne(id):
    fetch = requests.get(f"{config.get('Configuration', 'URL')}/queue/waiting")
    fetch = fetch.json()
    data = False
    for item in fetch:
        if item['queueId'] == id:
          data = item['queueStatus']
    return data
def getTerminal():
    fetchTerminal = getOneTerminal()
    if(len(fetchTerminal.keys()) == 0):
        return None
    else:
        return fetchTerminal.get('transactionType')
def getOneRowWaiting():
    data = []
    transactionType = getTerminal()
    fetch = requests.get(f"{config.get('Configuration', 'URL')}/queue")
    fetch = fetch.json()
    for item in fetch:
        if item['queueStatus'] != 'accommodated' and item['transactionType'] == transactionType:
            data.append(item)
    if(len(data)>0):
        data_sorted = sorted(data, key=lambda x: x.get('queueId', ''))
        return data_sorted[0]
    return {}

def getOneTerminal():
    fetch = requests.get(f"{config.get('Configuration', 'URL')}/terminal/{config.get('Configuration', 'TERMINAL')}")
    fetch = fetch.json()
    return fetch

def updateData(id):
    getOneQueue = getOne(id)
    status ="ongoing" if getOneQueue == "waiting" else "accommodated"
    terminal = getOneTerminal()
    terminal = terminal.get('terminalName')
    data = {"queueId": int(id), "queueStatus": status,"terminal":terminal}
    headers = {'Content-Type': 'application/json'}
    fetch = requests.patch(f"{config.get('Configuration', 'URL')}/queue", json=data, headers=headers)
    result = fetch.json()
    message = f"{result['name']} is now {result['queueStatus']}" if fetch.status_code==200 else "Something Went Wrong"
    return message


