import os
import re
import sys
import json
import random
import requests
from os import path

class BingSpider:

    def getImage(self, downloadFolder):
        searchURL = 'https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN'
        response = requests.get(searchURL)
        data = json.loads(response.text)

        resultId = data['images'][0]['hsh']
        resultURL = 'https://cn.bing.com' + data['images'][0]['url']
        print(u'正在为您下载图片:%s...' % resultId)
        if(not path.exists(downloadFolder)):
            os.makedirs(downloadFolder)
        
        jpgFile = resultId + '.jpg'
        jpgFile = os.path.join(downloadFolder, jpgFile)
        response = requests.get(resultURL)
        with open(jpgFile,'wb') as file:
            file.write(response.content)
        return jpgFile