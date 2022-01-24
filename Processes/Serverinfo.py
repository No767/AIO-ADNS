import ujson
info = ujson.load(open('Processes/Serverinfo.json'))
def save():
    '''
    It opens the Serverinfo.json file, and dumps the info variable into it.
    
    
    :return: None
    '''
    with open('Processes/ServerinfoTest.json', 'w') as f:
        ujson.dump(info, f)