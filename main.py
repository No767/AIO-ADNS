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

def getAnswer(domain):
    try:
        conn = sqlite3.connect('dns.db')
        c = conn.cursor()
        c.execute("SELECT answer FROM domains WHERE domain = ?", (domain,))
        answer = c.fetchone()[0]
        conn.close()
    except:
        answer = None
    return answer

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
            try:
                answer = getAnswer(queryData.question[0].to_text())
                print(f'[+] Found answer in database: {answer}')
                if answer != None:
                    response.answer = dns.message.from_text(answer).answer
                else:
                    forwardedResponse = dns.query.udp(queryData, backupServerInfo['google'], serverInfo['port'])
                    print(f'[+] Forwarded query to {backupServerInfo["google"]}')
                    response.answer = forwardedResponse.answer
                    addAnswer(queryData.question[0].to_text(), str(response))
            except Exception as e:
                print(e)
            # Send the response to the client
            s.sendto(response.to_wire(), addr)
    except KeyboardInterrupt:
        # Close the socket
        print('\nExiting...')
        s.close()
    # Exit the program
    exit()