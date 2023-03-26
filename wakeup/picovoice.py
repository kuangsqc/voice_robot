import pvporcupine
import pyaudio
import struct
import wave
from  common.config import conf
import sys

def picovoice(f):
    porcupine = pvporcupine.create(
        access_key= conf().get('picovoice_access_key'),
        keyword_paths= [conf().get('picovoice_ppn')]
    )
    pa = pyaudio.PyAudio()
    audio_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length)
    while True:
        try:
            pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            _pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            keyword_index = porcupine.process(_pcm)
            if keyword_index >= 0:
                #play_wav('mp3\\wait.wav')
                f()
        except KeyboardInterrupt:
                print("\nbye...")
                sys.exit()

def play_wav(filepath):
     # 打开wav文件并读取数据                                                                                             │
    with wave.open(filepath, "rb") as audio_file:
        audio_data = audio_file.readframes(-1)
        # 初始化音频流                                                                                                      │
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(audio_file.getsampwidth()),
        channels=audio_file.getnchannels(), 
        rate=audio_file.getframerate(),output=True)
        # 播放音频数据                                                                                                      │
        stream.write(audio_data)
        # 关闭流和PyAudio                                                                                                   │
        stream.stop_stream()
        stream.close()
        p.terminate()