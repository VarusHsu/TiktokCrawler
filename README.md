# TiktokCrawler
* 安装依赖项
```shell
  pip3 install -r requirements.txt	
```
* 打包库的安装
```shell
  pip3 install py2app
```
* 播放量爬虫打包命令
```shell
  py2applet --make-setup play_count_info.py
  python3 setup.py py2app 
```
* hashtag爬虫打包命令
```shell
  py2applet --make-setup user_by_hashtag.py
  python3 setup.py py2app 
```
* 播放量爬虫运行命令
```shell
  python3 play_count_info.py
```
* hashtag爬虫运行命令
```shell
  python3 user_by_hashtag.py
```
