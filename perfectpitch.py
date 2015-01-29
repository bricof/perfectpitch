import pyaudio
import numpy as np
from scipy import fft, arange
from sklearn import svm, cross_validation
import pickle


def convert_freq(frames):

    # note: this code is adapted from the code available here:
    # http://glowingpython.blogspot.ro/2011/08/how-to-plot-frequency-spectrum-with.html

    # configuration variables
    # note that frqMin and frqMax are set to the min and max frequencies on a piano
    Fs = 44100.0
    frqMin = 27.5
    frqMax = 4186
    
    signal = np.fromstring(frames, np.short)

    # setting up local variables for fft calculation
    n = len(signal) # length of the signal
    k = arange(n)
    T = n/Fs
    frq = k/T # two sides frequency range
    frq = frq[range(n/2)] # one side frequency range

    # fft (fast fourier transform) computing and normalization
    Y = fft(signal)/n 
    Y = abs(Y[range(n/2)])
    
    # trim the frq and Y arrays to the max and min hz considered
    Y = Y[np.logical_and(frq[:] > frqMin, frq[:] < frqMax)]
    frq = frq[np.logical_and(frq[:] > frqMin, frq[:] < frqMax)]
    
    # note: may wish to divide into a smaller number of frequency bands in future iterations
    # num_levels = 10
    # frq = np.linspace(frqMin, frqMax, num_levels)
    # Y_means = (np.histogram(Y, frq, weights=Y)[0] /
    #                                 np.histogram(Y, frq)[0])    
    
    # normalize Y to [0,1]
    Y *= 1/Y.max()

    return Y, frq, signal


def train(X0,y):
    
    # convert audio signal into the frequency domain
    X = []
    for frames in X0:
        amp, frq, signal = convert_freq(frames)
        X.append(amp)
    
    # split training data into train and validate sets
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(
                    X, y, test_size=0.3, random_state=42)
    
    # train svm
    m = svm.SVC()
    m.fit(X_train, y_train) 
    
    # write svm to file
    s = pickle.dumps(m)
    f = open('svm.txt','w')
    f.write(s)
    f.close()
    
    # calculate svm performance
    train_accuracy = m.score(X_train, y_train)
    test_accuracy = m.score(X_test, y_test)
    
    return train_accuracy, test_accuracy
    

def predict(frames):

    # convert audio signal into the frequency domain
    amp, frq, signal = convert_freq(frames)
    
    # open the trained svm from its pickled state
    f = open('svm.txt','r')
    s = f.read()
    f.close()
    m = pickle.loads(s)

    # use the trained svm to predict the note name
    X = amp
    y = m.predict(X)
    
    # return predicted note name (string)
    # along with ndarrays of the raw signal and its conversion to frequency and amplitude
    return y[0], amp, frq, signal


def get_audio():

    # open audio stream
    chunksize = 1024
    pa = pyaudio.PyAudio()
    stream = pa.open( format = pyaudio.paInt16,
                      channels = 1,
                      rate = 44100,
                      input = True,
                      frames_per_buffer = chunksize )

    # read chunk from audio stream and send to predict function
    p, amp, frq, signal = predict(stream.read(chunksize))
    
    # stop and close audio stream
    stream.stop_stream()
    stream.close()
    pa.terminate()
    
    # return predicted note name (string)
    # along with ndarrays of the raw signal and its conversion to frequency and amplitude
    return p, amp, frq, signal


