import speech_recognition as sr

def recognize_from_microphone():
  # 创建Recognizer对象
  r = sr.Recognizer()
  # 打开麦克风并开始录音  
  with sr.Microphone() as source:
    #print("Please speak...")
    audio = r.listen(source)
    # 将录音转化为文字 
    try:     
        text = r.recognize_google(audio, language='zh-CN', show_all= True)
        #print(f"You said: {text['alternative'][0]['transcript']}")
        if text['final']==True :
            return text['alternative'][0]['transcript']
        return ""
    except sr.UnknownValueError: 
        print("Could not understand audio")
        return ""
    except sr.RequestError as e: 
        print(f"Error: {e}")
        return "network error"

#语言文件转文字
def s2text(filepath):
    r = sr.Recognizer()
    test = sr.AudioFile(filepath)
    with test as source:
        audio = r.record(source)
    type (audio)
    print(r.recognize_google(audio, language='zh-CN', show_all= True))