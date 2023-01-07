#!/usr/bin/env python
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import sys
 

artist = "data"

def convertToSoup(link):
    driver = webdriver.Chrome()
    driver.get(link)
    time.sleep(5)
    content = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(content,"html.parser")
    return soup


def writeSongstoFile(trs):
    dataHeaders = ["Title/Composer","Performer","Duration","Stream on"]
    with open(artist+'.json', 'a') as f:
        x = 0
        for tr in trs:
            finalComma = ",\n"
            if((x+1)==len(trs)):
                finalComma = ""
            title_composer = tr.find('td',{'class': 'title-composer'})
            title = title_composer.find('div',{'class': 'title'})
            performer = tr.find('td',{'class': 'performer'})
            time = tr.find('td',{'class': 'time'})
            stream = tr.find('td',{'class': 'stream'})
            data = [title.text.strip(),performer.text.strip(),time.text.strip(),stream.text.strip()]
            f.write("\t{")
            for y in range(0, len(dataHeaders)):
                end = ","
                if((y+1)==(len(dataHeaders))):
                    end = ""
                f.write('\n\t\t"'+dataHeaders[y]+'": '+'"'+data[y]+'"'+end)
            f.write("\n\t}"+finalComma)
            x+=1

def returnSongData(soup):
    body = soup.find('body')
    albumContainer = body.find('div',{'class','overflow-container album'})
    cmn_wrap = albumContainer.find('div',{'id': 'cmn_wrap'})
    content_container = cmn_wrap.find('div',{'class': 'content-container'})
    content = content_container.find('div',{'class': 'content'})
    track_listing = content.find('section',{'class': 'track-listing'})
    disc = track_listing.find('div',{'class': 'disc'})
    table = disc.find('table')
    tbody = table.find('tbody')
    trs = tbody.find_all('tr',{'class': 'track'})
    return trs


def finishingTouch():
    with open(artist+'.json', 'r') as f:
        allData = f.read()
    with open(artist+'.json', 'w') as w:
        w.write("[\n"+str(allData)+"\n]")


def getAlbum(link):
    soup = convertToSoup(link)
    trs = returnSongData(soup)
    writeSongstoFile(trs)
    finishingTouch()

def getDiscography(link):
    soup = convertToSoup(link)
    body = soup.find('body')
    artistContainer = body.find('div',{'class','overflow-container artist'})
    cmn_wrap = artistContainer.find('div',{'id': 'cmn_wrap'})
    content_container = cmn_wrap.find('div',{'class': 'content-container'})
    content = content_container.find('div',{'class': 'content'})
    discography = content.find('section',{'class': 'discography'})
    table = discography.find('table')
    tbody = table.find('tbody')
    trs = tbody.find_all('tr')
    x = 0
    trsLength = len(trs)
    for tr in trs:
        title = tr.find('td',{'class': 'title'})
        a = title.find('a')
        newLink = a.get('href')
        print(newLink)
        newDriver = webdriver.Chrome()
        newDriver.get(newLink)
        time.sleep(5)
        newContent = newDriver.page_source.encode('utf-8').strip()
        newSoup = BeautifulSoup(newContent,"html.parser")
        newTrs = returnSongData(newSoup)
        writeSongstoFile(newTrs)
        if((x+1)!=trsLength):
            with open(artist+'.json', 'a') as f:
                f.write(',\n')
        x+=1
    finishingTouch()