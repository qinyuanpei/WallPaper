import os
import re
import sys
import uuid
import json
import random
import requests
from os import path
from bs4 import BeautifulSoup

# Alphacoders
class AlphacodersSpider:

    def getImage(self, downloadFolder): 
        url = 'https://wall.alphacoders.com/newest_wallpapers.php?lang=Chinese' 
        response = requests.get(url) 
        # print(response.text)
        soup = BeautifulSoup(response.text,'html.parser')
        imgs = soup.find_all('img')
        length = len(imgs)
        if length > 0:
            match = random.choice(imgs)
            rawUrl = match.get('src')
            rawId = rawUrl.split('/')[-1]
            raw = requests.get(rawUrl) 
            imgFile = os.path.join(downloadFolder, rawId)
            with open(imgFile,'wb') as f:
                f.write(raw.content)
        return imgFile