import dns, socket, dns.message, dns.rrset, dns.resolver

serverInfo = {
    'ip': '127.0.0.1',
    'port': 53
}
backupServerInfo = {
    'google': '8.8.8.8'
}

if __name__ == '__main__':
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
                forwardedResponse = dns.query.udp(queryData, backupServerInfo['google'], serverInfo['port'])
                response.answer = forwardedResponse.answer
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