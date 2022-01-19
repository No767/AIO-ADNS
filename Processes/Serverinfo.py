import json

info = json.load(open('Processes/Serverinfo.json'))

def save():
    '''
    It opens the Serverinfo.json file, and dumps the info variable into it.
    
    
    :return: None
    '''
    with open('Processes/Serverinfo.json', 'w') as f:
        json.dump(info, f)