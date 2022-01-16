import dns, dns.message, dns.query
import socket
import sqlite3
import Processes.Database as db
import Processes.ServerInfo as si
def run():
    # Create a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind the socket to the port
    try:
        s.bind((si.serverInfo['ip'], si.serverInfo['port']))
    except:
        print(f'Error: Port {si.serverInfo["port"]} is already in use.')
    print('[+] DNS Server')
    while True:
        # Receive data from the client
        data, addr = s.recvfrom(512)
        queryData = dns.message.from_wire(data)
        print(f'[+] Received query from {addr[0]} for: {queryData.question[0].to_text()}')
        # Create a response
        response = dns.message.make_response(queryData)
        # Add a response to the response
        response.answer = db.getAnswer(queryData)
        # Send the response to the client
        s.sendto(response.to_wire(), addr)