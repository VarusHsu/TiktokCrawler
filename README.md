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
  make play_count
```
* 定时任务播放量客户端
```shell
  make client 
```
* hashtag爬虫打包命令
```shell
  make hashtag
```
* 播放量爬虫运行命令
```shell
  make run_play_count
```
* hashtag爬虫运行命令
```shell
  make run_hashtag
```
* 清除已经打的包以及打包缓存
```shell
  make clear
```
* 生成默认输出路径
```shell
  make path
```