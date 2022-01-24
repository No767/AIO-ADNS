import sqlite3
import dns
import logging
import Processes.Serverinfo as si
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import Column, MetaData, Table, select, String


def initdb():
    '''
    Create a database called dns.db if it doesn't exist, and create a table called domains if it doesn't
    exist.
    
    
    :return: None
    '''
    meta = MetaData()
    Table("domains", meta, Column("domain", String, primary_key=True), Column("answer", String))
    engine = create_async_engine("sqlite+aiosqlite///dns.db")
    async with engine.begin() as conn:
        await conn.run_sync(meta.create_all)


def getLocalAnswer(queryData):
    '''
    It takes a queryData object as an argument, and then searches the database for the domain name in
    the question section of the queryData object. If it finds a match, it returns the answer section of
    the DNS message that is stored in the database.
    
    :param queryData: The DNS query data
    :return: The answer to the question
    '''
    try:
        meta = MetaData()
        domains2 = Table("domains", meta, Column("domain", String, primary_key=True), Column("answer", String))
        engine = create_async_engine("sqlite+aiosqlite///dns.db")
        async with engine.connect() as conn:
            s = select(domains2.c.answer).filter(domains2.c.domain == queryData.question[0].to_text())
            res = await conn.execute(s)
            answer = res.fetchone()
            logging.debug('[+] Found answer in local database')
    except:
        return None
    return dns.message.from_text(answer).answer

def getRemoteAnswer(queryData):
    '''
    It forwards the query to the remote nameserver and returns the answer.
    
    :param queryData: The query data that was sent to the remote nameserver
    :return: The answer from the remote nameserver
    '''
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
    '''
    If the local answer is not None, return it. Otherwise, if the remote answer is not None, return it.
    Otherwise, return None.
    
    :param queryData: The query data to be sent to the server
    :return: A list of dictionaries
    '''
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
    '''
    It adds a domain and its IP address to the database.
    
    :param domain: The domain name that we're looking up
    :param answer: The answer to the question
    :return: None
    '''
    meta = MetaData()
    domains3 = Table("domains", meta, Column("domain", String, primary_key=True), Column("answer", String))
    engine = create_async_engine("sqlite+aiosqlite///dns.db")
    async with engine.begin() as conn:
        ins = domains3.insert().values(domain=domain, answer=answer)
        await conn.execute(ins)