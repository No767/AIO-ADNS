import sqlite3
import dns
import logging
import Processes.Serverinfo as si

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
        logging.debug(f'[+] Found answer in local database')
        conn.close()
    except:
        return None
    return dns.message.from_text(answer).answer

def getRemoteAnswer(queryData):
    useServer = {
        'ip': '0.0.0.0',
        'port': 53
    }
    for backupServerName in si.info['Dnsserver']['Backupservers'].keys():
        if (si.info['Dnsserver']['Backupservers'][backupServerName]['enabled']):
            useServer['ip'] = si.info['Dnsserver']['Backupservers'][backupServerName]['ip']
            useServer['port'] = si.info['Dnsserver']['Backupservers'][backupServerName]['port']
            break
    forwardedResponse = dns.query.udp(queryData, useServer['ip'], useServer['port'])
    logging.debug(f"[+] Forwarded query to {useServer['ip']}:{useServer['port']}")
    addAnswer(queryData.question[0].to_text(), str(forwardedResponse))
    logging.debug(f'[+] Found answer in remote nameserver and added to local database')
    return forwardedResponse.answer

def getAnswer(queryData):
    localAnswer = getLocalAnswer(queryData)
    if localAnswer is None:
        remoteAnswer = getRemoteAnswer(queryData)
        if remoteAnswer is not None:
            return remoteAnswer
        else:
            logging.debug(f'[-] No answer found')
            return None
    else:
        return localAnswer

def addAnswer(domain, answer):
    conn = sqlite3.connect('dns.db')
    c = conn.cursor()
    c.execute("INSERT INTO domains VALUES (?, ?)", (domain, answer))
    conn.commit()
    conn.close()