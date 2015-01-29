# This script is used to compile training data from wav files and send it to 
# perfectpitch.train(). It is meant to be used with the data files constructed by 
# 'recorder.py'.
#
# The trained model will be saved by perfectpitch.train(), in pickled form, to svm.txt.


import wave, os

# construct training data, without preprocessing

folders = [ 'z','f0','fs0','g0','gs0','a1','as1','b1','c1','cs1','d1','ds1','e1','f1',
            'fs1','g1','gs1','a2','as2','b2','c2','cs2','d2','ds2','e2','f2','fs2','g2',
            'gs2','a3','as3','b3','c3' ]

X0 = []
y = []
for fd in folders:

    path, dirs, files = os.walk('wav/' + fd + '/').next()
    file_count = len(files) - 2

    for i in range(file_count):
        f = wave.open('wav/' + fd + '/i'+str(i)+'.wav')
        s = f.readframes(f.getnframes())
        f.close
        X0.append(s)
        y.append(fd)


# send training data to training routine
train_accuracy, test_accuracy = perfectpitch.train(X0,y)

# print performance
print "Accuracy: %0.2f " % train_accuracy
print "Accuracy: %0.2f " % test_accuracy
