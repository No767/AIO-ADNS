import sqlite3
import dns
import Processes.ServerInfo as si

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
    print(f'[+] Forwarded query to {si.backupServerInfo["google"]}')
    db.addAnswer(queryData.question[0].to_text(), str(forwardedResponse))
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