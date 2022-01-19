import json

info = json.load(open('Processes/Serverinfo.json'))

def save():
    with open('Processes/Serverinfo.json', 'w') as f:
        json.dump(info, f)