import requests
from bs4 import BeautifulSoup
from notation import INTERVALS
import os
import json

filename = "chords.json"

def scrape():
    r = requests.get('https://www.guitar.ch/en-us/guitar/chord_finder/chord_finder-chord-formula.html')
    page = BeautifulSoup(r.content, 'html.parser')

    # grabbing the list of div items containing each chord information
    listDiv = page.find('div', id="chordTable")
    itemDivs = listDiv.find_all('div', class_="tableInit")[2:]

    chordDict = {}

    for item in itemDivs:
        # getting the name and intervals of the chord
        nameStr = min(item.find('div', class_="name").find('a').text.replace(' ', '').split(','), key=len)
        intervalDiv = item.find('div', class_="interval")
        # creating list of interval steps relative to root
        intList = []
        for i in intervalDiv.find_all('div', class_="number"):
            intName = i.text.strip()
            if(intName != ''):
                intList.append(INTERVALS[intName])
        chordDict[nameStr] = intList
    return chordDict

def readChordData():
    if(os.path.exists(filename)):
        return json.load(open(filename))
    else:
        data = scrape()
        json.dump(data, open(filename, 'w'))
        return data

        
    