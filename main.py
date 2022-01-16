import dns, dns.message, dns.query
import socket
import sqlite3

serverInfo = {
    'ip': '127.0.0.1',
    'port': 53
}
backupServerInfo = {
    'google': '8.8.8.8'
}

def initdb():
    conn = sqlite3.connect('dns.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS domains (
        domain text PRIMARY KEY,
        answer text
    )''')
    conn.commit()
    conn.close()

def getLocalAnswer(queryData):
    try:
        conn = sqlite3.connect('dns.db')
        c = conn.cursor()
        c.execute("SELECT answer FROM domains WHERE domain = ?", (queryData.question[0].to_text(),))
        answer = c.fetchone()[0]
        conn.close()
    except:
        return None
    return dns.message.from_text(answer).answer

def getRemoteAnswer(queryData):
    forwardedResponse = dns.query.udp(queryData, backupServerInfo['google'], serverInfo['port'])
    print(f'[+] Forwarded query to {backupServerInfo["google"]}')
    addAnswer(queryData.question[0].to_text(), str(forwardedResponse))
    return forwardedResponse.answer

def getAnswer(queryData):
    localAnswer = getLocalAnswer(queryData)
    if localAnswer is not None:
        print(f'[+] Found answer in local database')
        return localAnswer
    else:
        remoteAnswer = getRemoteAnswer(queryData)
        if remoteAnswer is not None:
            print(f'[+] Found answer in remote nameserver')
            return remoteAnswer
        else:
            print(f'[-] No answer found')
            return None

def addAnswer(domain, answer):
    conn = sqlite3.connect('dns.db')
    c = conn.cursor()
    c.execute("INSERT INTO domains VALUES (?, ?)", (domain, answer))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    initdb()
    # Create a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind the socket to the port
    try:
        s.bind((serverInfo['ip'], serverInfo['port']))
    except:
        print(f'Error: Port {serverInfo["port"]} is already in use.')
    print('[+] DNS Server')
    try:
        while True:
            # Receive data from the client
            data, addr = s.recvfrom(512)
            queryData = dns.message.from_wire(data)
            print(f'[+] Received query from {addr[0]} for: {queryData.question[0].to_text()}')
            # Create a response
            response = dns.message.make_response(queryData)
            # Add a response to the response
            response.answer = getAnswer(queryData)
            # Send the response to the client
            s.sendto(response.to_wire(), addr)
    except KeyboardInterrupt:
        # Close the socket
        print('\nExiting...')
        s.close()
    # Exit the program
    exit()