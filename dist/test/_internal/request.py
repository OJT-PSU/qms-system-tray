import requests , os, configparser,sys

def read_config(key):
    config = configparser.ConfigParser()
    if getattr(sys, 'frozen', False):  # Check if running from PyInstaller bundle
        exe_dir = os.path.dirname(sys.executable)
    else:
        exe_dir = os.path.dirname(__file__)  # Get the directory where the script is located

    config_file_path = os.path.join(exe_dir, 'config.ini')

    if os.path.exists(config_file_path):
        config.read(config_file_path)
        return config['Configuration'].get(key, None)
    else:

        raise FileNotFoundError("Config file config.ini not found.")
    
def getOne(id):
    fetch = requests.get(f"{read_config('URL')}/queue/waiting")
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
    fetch = requests.get(f"{read_config('URL')}/queue")
    fetch = fetch.json()
    for item in fetch:
        if item['queueStatus'] != 'accommodated' and item['transactionType'] == transactionType and item['toDisplay'] == 0:
            data.append(item)
    if(len(data)>0):
        data_sorted = sorted(data, key=lambda x: x.get('queueId', ''))
        return data_sorted[0]
    return {}

def getOneTerminal():
    fetch = requests.get(f"{read_config('URL')}/terminal/{read_config('TERMINAL')}")
    fetch = fetch.json()
    return fetch

def updateData(id):
    getOneQueue = getOne(id)
    status ="ongoing" if getOneQueue == "waiting" else "accommodated"
    terminal = getOneTerminal()
    terminal = terminal.get('terminalName')
    data = {"queueId": int(id), "queueStatus": status,"terminal":terminal}
    headers = {'Content-Type': 'application/json'}
    fetch = requests.patch(f"{read_config('URL')}/queue", json=data, headers=headers)
    result = fetch.json()
    message = f"{result['name']} is now {result['queueStatus']}" if fetch.status_code==200 else "Something Went Wrong"
    return message


