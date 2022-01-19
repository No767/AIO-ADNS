import dns, dns.message, dns.query
import socket
import sqlite3
import logging
from Processes import Database as db
from Processes import Serverinfo as si
import multiprocessing.dummy as multiprocessing

def job(s, data, addr):
    '''
    It takes a socket, a data packet, and an address as arguments. It then parses the data packet into a
    dns.message object. It then logs the query and then sends the response to the client.
    
    :param s: The socket
    :param data: The data received from the client
    :param addr: The address of the client
    :return: None
    '''
    queryData = dns.message.from_wire(data)
    logging.info(f'[+] Received query from {addr[0]} for: {queryData.question[0].to_text()}')
    # Create a response
    response = dns.message.make_response(queryData)
    # Add a response to the response
    response.answer = db.getAnswer(queryData)
    # Send the response to the client
    s.sendto(response.to_wire(), addr)

def run():
    '''
    Create a socket, bind it to the port, and wait for data.
    
    
    :return: None
    '''
    # Set up logging
    logging.basicConfig(filename = 'Logs/Server.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
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
        # Start a new thread to handle the request
        p = multiprocessing.Process(target=job, args=(s, data, addr))
        p.start()