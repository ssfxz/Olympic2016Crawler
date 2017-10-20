# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import traceback
import os
import sys
import socket

def fetchUrl(url, retryNum = 5):
    i = 0
    while i < retryNum:
        try:
            response = urllib2.urlopen(url, timeout=1).read()
            return response
        except socket.timeout:
            i += 1
            print "Timeout! Retry", i
        except:
            print "Failure!"
    return "Failure!"

def fetchSportsList(url):
    response = fetchUrl(url)
    soup = BeautifulSoup(response, 'html.parser', from_encoding='utf-8')

    sportList = soup("div", class_="sports_list_item")
    print "Sport Count:", len(sportList)
    for item in sportList:
        caption = item.a.div.find("div", class_="cn").get_text(strip=True)
        print caption
        sportUrl = item.a['href']
        fetchPlayerList(sportUrl)

def fetchPlayerList(url):
    global total
    response = fetchUrl(url)
    soup = BeautifulSoup(response, 'html.parser', from_encoding='utf-8')

    playerList = soup("div", class_="player_item")
    total += len(playerList)
    print "Player Count:", len(playerList)
    for item in playerList:
        playerUrl = "http://2016chinateam.olympic.cn" + item.a['href']
        # print playerUrl
        fetchPlayerInfo(playerUrl)

def fetchPlayerInfo(url):
    global done
    response = fetchUrl(url)
    soup = BeautifulSoup(response, 'html.parser', from_encoding='GBK')

    done += 1
    td = soup("td")
    text = ""
    i = 0
    while i < len(td):
        text += td[i].get_text(strip=True) + "\t"
        i += 1
    output(text)

def output(text):
    print text
    fo.write(text.encode("utf-8"))
    fo.write('\n')


fo = open("./players.txt", "wb+")
fo.write("")
total = 0
done = 0

url = "http://www.olympic.cn/zt/Rio2016/chinateam/"
fetchSportsList(url)

print done, "/", total

fo.close()
