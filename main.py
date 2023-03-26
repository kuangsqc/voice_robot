import os, glob
from wakeup import picovoice
from tts import googlesr
from tts import azuretts as azuretts
from chatbot import chatgpt
from playsound import playsound
from common import config
from common.log import logger

def run():  
    logger.info("收到唤醒指令")
    playsound('mp3\\wait.mp3')
    q=googlesr.recognize_from_microphone()
    if len(q) == 0:
        logger.warn("语言识别失败！")
        playsound('mp3\\sorry.wav')
        return
    elif q=='network error':
        logger.warn("google连接失败！")
        playsound('mp3\\neterr.wav')
        return
    logger.info("你: {}".format(q))
    res = chatgpt.chatGpt(q)
    logger.info("GPT: {}".format(res))
    for file in glob.glob("tmp/*"):
        os.remove(file)
    MP3file=azuretts.text2voice(res)
    logger.info("GPT语音")
    playsound(MP3file)

def main():
    config.load_config()
    os.environ["http_proxy"] =  config.conf().get('proxy')
    os.environ["https_proxy"] =  os.environ["http_proxy"]
    logger.info("等待唤醒指令")
    picovoice.picovoice(run)
    
if __name__ == "__main__":
    main()