import os
import re
import sys
import json
import random
import requests
from os import path

class UnsplashSpider:
    def getImage(self,downloadFolder):
        searchURL = 'https://unsplash.com/napi/search?client_id=%s&query=%s&page=1'
        client_id = 'fa60305aa82e74134cabc7093ef54c8e2c370c47e73152f72371c828daedfcd7'
        categories = ['nature','flowers','wallpaper','landscape','sky']
        searchURL = searchURL % (client_id,random.choice(categories))
        response = requests.get(searchURL)
        print(u'正在从Unsplash上搜索图片...')

        print(response.text)
        data = json.loads(response.text)
        results = data['photos']['results']
        print(u'已为您检索到图片共%s张' % str(len(results)))
        results = list(filter(lambda x:float(x['width'])/x['height'] >=1.33,results))
        result = random.choice(results)
        resultId = str(result['id'])
        resultURL = result['urls']['regular']

        print(u'正在为您下载图片:%s...' % resultId)
        if(not path.exists(downloadFolder)):
            os.makedirs(downloadFolder)
        jpgFile = resultId + '.jpg'
        jpgFile = os.path.join(downloadFolder, jpgFile)
        response = requests.get(resultURL)
        with open(jpgFile,'wb') as file:
            file.write(response.content)
        return jpgFile

