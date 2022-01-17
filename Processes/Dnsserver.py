import dns, dns.message, dns.query
import socket
import sqlite3
import logging
from Processes import Database as db
from Processes import Serverinfo as si
def run():
    # Set up logging
    logging.basicConfig(filename = 'Logs/DNSServer.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.debug('[+] Starting DNS server')
    print('[+] Starting DNS server')
    # Create a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind the socket to the port
    try:
        s.bind((si.info['Dnsserver']['ip'], si.info['Dnsserver']['port']))
    except:
        logging.error(f"Port {si.info['Dnsserver']['port']} is already in use.")
    while True:
        # Receive data from the client
        data, addr = s.recvfrom(512)
        queryData = dns.message.from_wire(data)
        logging.info(f'[+] Received query from {addr[0]} for: {queryData.question[0].to_text()}')
        # Create a response
        response = dns.message.make_response(queryData)
        # Add a response to the response
        response.answer = db.getAnswer(queryData)
        # Send the response to the client
        s.sendto(response.to_wire(), addr)