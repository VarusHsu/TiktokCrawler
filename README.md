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
  make generate-play-count
```
* 定时任务播放量客户端
```shell
  make generate-client 
```
* hashtag爬虫打包命令
```shell
  make generate-hashtag
```
* 播放量爬虫运行命令
```shell
  make run-play-count
```
* hashtag爬虫运行命令
```shell
  make run-hashtag
```
* 清除已经打的包以及打包缓存
```shell
  make clear
```
* 生成默认输出路径
```shell
  make path
```
* 服务器上部署服务
```shell
  sudo nohup make serve &
```

* 项目结构（Version 1.1.1）
```
.
├── README.md
├── client
│   ├── internal.py
│   └── main.py
├── common
│   ├── __init__.py
│   ├── config_reader.py
│   ├── config_windows.py
│   ├── enums.py
│   ├── feishu.py
│   ├── internal.py
│   ├── internalV2.py
│   ├── logger.py
│   ├── reporter.py
│   ├── requester.py
│   ├── signals.py
│   ├── util.py
│   └── xlsx_worker.py
├── config
│   └── config.yaml
├── generate
│   └── __init__.py
├── hashtag
│   ├── internal.py
│   └── main.py
├── makefile
├── play_count
│   ├── internal.py
│   └── main.py
├── requirements.txt
├── scheduler_job
│   ├── get_increase.py
│   ├── played_count_job.py
│   └── source.py
├── script
│   ├── get_increase.sh
│   ├── scheduler_get_play_count.sh
│   └── set_default_path.sh
└── server
    ├── generate
    ├── go.mod
    ├── go.sum
    ├── history
    │   ├── by_increase
    │   ├── by_time
    │   └── compare_cache
    ├── logger
    │   └── logger.go
    ├── main
    │   └── main.go
    └── source
```