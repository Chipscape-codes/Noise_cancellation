import pyaudio
import numpy as np
import webrtcvad
import signal
import sys
RATE = 48000            
FRAME_DURATION = 10        
FRAME_SIZE = int(RATE * FRAME_DURATION / 1000)  
AMPLIFY =  3.0            


vad = webrtcvad.Vad()
vad.set_mode(3)  

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,output=True,frames_per_buffer=FRAME_SIZE,stream_callback=None)  

print("speak")
def stop_handler(sig, frame):
    print("Stop")
    stream.stop_stream()
    stream.close()
    p.terminate()
    sys.exit(0)

signal.signal(signal.SIGINT, stop_handler)

while True:
    
    audio_data = stream.read(FRAME_SIZE, exception_on_overflow=False)
    
    
    if vad.is_speech(audio_data, RATE):
        
        samples = np.frombuffer(audio_data, dtype=np.int16)

       
        amplified = np.clip(samples * AMPLIFY, -32768, 32767).astype(np.int16)

       
        stream.write(amplified.tobytes())
    else:
     
        stream.write(np.zeros(FRAME_SIZE, dtype=np.int16).tobytes())
