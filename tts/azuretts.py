# 来源 https://github.com/OS984/DiscordBotBackend/blob/3b06b8be39e4dbc07722b0afefeee4c18c136102/NeuralTTS.py
# A completely innocent attempt to borrow proprietary Microsoft technology for a much better TTS experience
#import requests
import websockets
import asyncio
from datetime import datetime
import time
import re
import uuid
import os

import re
#import threading


# Fix the time to match Americanisms
def hr_cr(hr):
    corrected = (hr - 1) % 24
    return str(corrected)

# Add zeros in the right places i.e 22:1:5 -> 22:01:05
def fr(input_string):
    corr = ''
    i = 2 - len(input_string)
    while (i > 0):
        corr += '0'
        i -= 1
    return corr + input_string

# Generate X-Timestamp all correctly formatted
def getXTime():
    now = datetime.now()
    return fr(str(now.year)) + '-' + fr(str(now.month)) + '-' + fr(str(now.day)) + 'T' + fr(hr_cr(int(now.hour))) + ':' + fr(str(now.minute)) + ':' + fr(str(now.second)) + '.' + str(now.microsecond)[:3] + 'Z'

# Async function for actually communicating with the websocket
async def transferMsTTSData(SSML_text, outputPath):
    req_id = uuid.uuid4().hex.upper()
    # 目前该接口没有认证可能很快失效
    endpoint2 = f"wss://eastus.api.speech.microsoft.com/cognitiveservices/websocket/v1?TrafficType=AzureDemo&Authorization=bearer%20undefined&X-ConnectionId={req_id}"
    async with websockets.connect(endpoint2,extra_headers={'Origin':'https://azure.microsoft.com'}) as websocket:
        payload_1 = '{"context":{"system":{"name":"SpeechSDK","version":"1.12.1-rc.1","build":"JavaScript","lang":"JavaScript","os":{"platform":"Browser/Linux x86_64","name":"Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0","version":"5.0 (X11)"}}}}'
        message_1 = 'Path : speech.config\r\nX-RequestId: ' + req_id + '\r\nX-Timestamp: ' + \
            getXTime() + '\r\nContent-Type: application/json\r\n\r\n' + payload_1
        await websocket.send(message_1)

        payload_2 = '{"synthesis":{"audio":{"metadataOptions":{"sentenceBoundaryEnabled":false,"wordBoundaryEnabled":false},"outputFormat":"audio-16khz-32kbitrate-mono-mp3"}}}'
        message_2 = 'Path : synthesis.context\r\nX-RequestId: ' + req_id + '\r\nX-Timestamp: ' + \
            getXTime() + '\r\nContent-Type: application/json\r\n\r\n' + payload_2
        await websocket.send(message_2)
        
        payload_3 = SSML_text
        message_3 = 'Path: ssml\r\nX-RequestId: ' + req_id + '\r\nX-Timestamp: ' + \
            getXTime() + '\r\nContent-Type: application/ssml+xml\r\n\r\n' + payload_3
        await websocket.send(message_3)

        # Checks for close connection message
        end_resp_pat = re.compile('Path:turn.end')
        audio_stream = b''
        while(True):
            response = await websocket.recv()
            if (re.search(end_resp_pat, str(response)) == None):
                if type(response) == type(bytes()):
                    try:
                        needle = b'Path:audio\r\n'
                        start_ind = response.find(needle) + len(needle)
                        audio_stream += response[start_ind:]
                    except:
                        pass
            else:
                break
        with open(f'{outputPath}.mp3', 'wb') as audio_out:
            audio_out.write(audio_stream)


async def mainSeq(SSML_text, outputPath):
    await transferMsTTSData(SSML_text, outputPath)

def get_SSML(path):
    with open(path,'r',encoding='utf-8') as f:
        return f.read()


def text2voice(txt,index=0):
    SSML_text=get_SSML('.\\tts\\SSML.xml').format(txt)
    if os.path.exists('.\\tmp')==False:
        os.makedirs('.\\tmp')
    output_path = '.\\tmp\\output_'+ str(int(time.time()*1000))+str(index)
    event_loop = asyncio.new_event_loop()
    event_loop.run_until_complete(mainSeq(SSML_text, output_path))
    #asyncio.get_event_loop().run_until_complete(mainSeq(SSML_text, output_path))
    return output_path+".mp3"


#多线程同步处理 会封ip
def playwiththreads(strs):
    slist= re.split(r'[？。]', strs)
    slist=[item for item in slist if item]
    list=[]

    def gettts(text,index):
        file = text2voice(text,index)
        print(text)
        print(file,index)
        for j in range(len(list)):
            if list[j]['i']==index:
                list[j]['file']=file
                break

    # for i in range(len(slist)):
    #     list.append({'i':i,'file':''})
    #     tpstr=str(i)+slist[i]
    #     t= threading.Thread(target=gettts, args=(tpstr,i,))
    #     t.start()

    # while len(list)>0:
    #     if list[0]['file']!='':
    #         playsound(list[0]['file'],False)
    #         list.pop(0)