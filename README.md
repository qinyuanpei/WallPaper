# WallPaper
一个基于Python的Windows下的壁纸更换工具，支持以扩展的方式从不同源上抓取壁纸。目前已支持以下站点：
* [Unsplash](https://unsplash.com) (默认)
* [必应壁纸](https://cn.bing.com/)
* [WallHaven](https://wallhaven.cc)
* [国家地理](https://www.nationalgeographic.com/photography/photo-of-the-day/2019/10/plane-fuel-pilot-aerial/)

# 使用方法
python main.py 或者 main.exe

# 插件开发
在plugins目录中新建一个.py文件，类名任意，只需要实现getImage()方法即可：

```Python
# 必应每日壁纸插件
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
```

接下里，修改配置文件config.ini:

```
[Main]
DownloadFolder = download

[Plugin]
PluginName = BingSpider
PluginFile = bingSpider.py
```

Enjoy! 

# 技术细节
https://qinyuanpei.github.io/posts/2822230423/

