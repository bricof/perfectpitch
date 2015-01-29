# This script is used to record training data for the learning algorithm.
#
# It creates a folder 'wav', within which it creates the set of folders listed in 'folders'
# note that 'z' is meant to correspond to no note being played, 's' denotes a sharp,
# and the integer at the end of the folder name corresponds to the octave number.
# The notes in 'folders' are all of the notes on a standard melodion.
# 
# The user is intended to start running the script, wait for the non-note recording to 
# complete, and then play each note in turn for 10 seconds each, with a five second break
# between notes, as indicated by the "listening - [note name]" and "done listening" 
# feedback on the command line.
# 
# The result of the script will be a set of wav files in each of the folders, each file 
# containing of a 'chunksize' length of recording. These files will constitute a labeled 
# training set for the learning algorithm, with the folder name as the label and each
# wav file as a data point.


import pyaudio, wave, time, os

# configuration
chunksize = 1024
record_seconds = 10
iStart = 0
folders = [ 'z','f0','fs0','g0','gs0','a1','as1','b1','c1','cs1','d1','ds1','e1','f1',
            'fs1','g1','gs1','a2','as2','b2','c2','cs2','d2','ds2','e2','f2','fs2','g2',
            'gs2','a3','as3','b3','c3' ]

# open audio stream
pa = pyaudio.PyAudio()
stream = pa.open( format = pyaudio.paInt16,
                  channels = 1,
                  rate = 44100,
                  input = True,
                  frames_per_buffer = chunksize )


for fd in folders:

    # make folder
    if not os.path.exists('wav/' + fd):
        os.makedirs(fd)

    # record a set of wav files, each 'chunksize' samples long  (at 44100 samples/second)  
    print("* listening - " + str(fd))
    for i in range(iStart, iStart + int(record_seconds * 44100 / chunksize)):
        wf = wave.open('wav/' + fd + '/i'+str(i)+'.wav', 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(pa.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(stream.read(chunksize)))
        wf.close()
    print("* done listening" + str(fd))

    # let the user take a breath before starting on the next note
    time.sleep(5)


# stop and close audio stream
stream.stop_stream()
stream.close()
pa.terminate()
    
