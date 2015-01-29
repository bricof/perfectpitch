import pyaudio
import matplotlib.pyplot as plt
import perfectpitch

chunksize = 1024

# set up plots
plt.ion()
plt.show()
plt.subplot(2,1,1)
plt.title('time domain')
plt.subplot(2,1,2)
plt.title('freqency domain')


for i in range(0, 500):

    # open audio stream
    pa = pyaudio.PyAudio()
    stream = pa.open( format = pyaudio.paInt16,
                      channels = 1,
                      rate = 44100,
                      input = True,
                      frames_per_buffer = chunksize )
    
    # send audio sample to perfectpitch, get predicted note name
    # along with other info for graphing
    p, amp, frq, signal = perfectpitch.predict(stream.read(chunksize))
    
    # stop and close audio stream
    stream.stop_stream()
    stream.close()
    pa.terminate()
    
    # update plots
    plt.subplot(2,1,1)
    l1 = plt.plot(range(len(signal)), signal, color='b')
    plt.subplot(2,1,2)
    l2 = plt.plot(frq, amp, color='b')
    t = plt.text(4000,0.7,p)
    plt.pause(0.01)
    l1.pop(0).remove()
    l2.pop(0).remove()
    t.remove()






