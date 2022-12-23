## Description
Download Grafana panel image by using 
[Grafana Image Renderer](https://grafana.com/grafana/plugins/grafana-image-renderer/) plugin 
and send it to Telegram chat or channel. 

## Features
- Request to render image for specified Grafana panel
- Download the requested image
- (Optional) Add watermark to image 
- (Optional) Send image to Telegram chat or channel

## Dependencies
- [Requests project](https://pypi.org/project/requests/)
<!-- termynal -->
```
$ pip install requests
```
- [Pillow project](https://pypi.org/project/Pillow/)
<!-- termynal -->
```
$ pip install pillow
```
- [python-telegram-bot project](https://github.com/python-telegram-bot/python-telegram-bot)
<!-- termynal -->
```
$ pip install python-telegram-bot
```

## Grafana requirements
Grafana Image Renderer must be installed before using the tool.
Please read [Plugin installation](https://grafana.com/grafana/plugins/grafana-image-renderer/) instruction 
carefully, especially if you are going to use Grafana Docker image.    

### Grafana Docker image
Please use the following 
[instruction](https://grafana.com/docs/grafana/v8.5/installation/docker/#build-with-grafana-image-renderer-plugin-pre-installed)
to run Grafana Docker image with the plugin installed. 
The instruction is working pretty well with Grafana 9.3.2 and latest 
[Dockerfile](https://github.com/grafana/grafana/blob/05c9af511057b221e50454033ee798df13fbc987/packaging/docker/custom/Dockerfile) 

### Grafana API Key
Please generate [API Key](https://grafana.com/docs/grafana/latest/administration/api-keys/) for the tool. 


Navigate: Configuration -> API Keys menu 


## Tested environment
- Python 3.10 
- Grafana 9.3.2 

## Configuration
Configuration can be specified via [settings.ini](settings.ini) file.
### Section GRAFANA
Specify Grafana host, port and api key 
### Section PANEL_IMAGE
Specify settings and panel to render:
- `DASHBOARD_UID` - copy from dashboard url or dashboard json. 
- `PANEL_ID` - copy from panel view url or panel json.
- `FROM_DATE` - recommendation is using quick ranges (example: now-1d etc.) or convert datetime to milliseconds   
- `TO_DATE` - recommendation is using quick ranges (example: now etc.) or convert datetime to milliseconds
- `ORG_ID` - copy from panel view url
- `WIDTH`, `HEIGHT`, `TZ` - as you wish  
### Section TEMP_STORAGE
Specify file path to save rendered image. 
Note: Directory must be created. 
### Section WATERMARK
Specify settings to add watermark on panel image:
- `TEXT` - watermark text. Keep empty to disable functionality.
- `FONT` and `FONT_SIZE` - text font settings. 
- `MARGIN` - margin size for watermark
### Section TELEGRAM
Specify settings to send image to Telegram chat or channel:
- `BOT_TOKEN` - telegram bot token.
- `CHAT_ID` - id of chat or channel. 
- `IMAGE_DESCRIPTION` - optional description for image

## Command line arguments 
- `--dashboard` - dashboard uid
- `--panel` - panel id
- `--f` - from date
- `--t` - to date
- `--file` - path to file

## Watermark
Watermark is optional and can be disabled if `TEXT` (watermark text) is empty.


Watermark is drawing in the bottom right corner. 

## Telegram
Telegram is optional and can be disabled if `BOT_TOKEN` and\or `CHAT_ID` are empty.


Telegram bot can be easily created in a few seconds via @BotFather.  
Please note the easiest way to find [chat_id](https://stackoverflow.com/a/56546442).  

## Logging
All logs are written in logs/downloader.log.
Any kind of settings can be changed in main.py code

## Project change log
[Here](CHANGELOG.md)

## Disclaimer
The author is not responsible for any errors or omissions obtained from the use of this tool.
