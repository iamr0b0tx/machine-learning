#basic imports
import glob, os
import IPython
from random import randint
from itertools import combinations

#data processing
import librosa
import numpy as np

from progressbar import ProgressBar

#modelling
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, accuracy_score
from matplotlib import pyplot as plt

from keras import backend as K
from keras.layers import Activation
from keras.layers import Input, Lambda, Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from keras.models import Model, Sequential
from keras.optimizers import RMSprop, Adam

CWD = '.'

def audio2vector(file_path, max_pad_len=400):
    
    #read the audio file
    audio, sr = librosa.load(file_path, mono=True)
    #reduce the shape
    audio = audio[::3]
    
    #extract the audio embeddings using MFCC
    mfcc = librosa.feature.mfcc(audio, sr=sr) 
    
    #as the audio embeddings length varies for different audio, we keep the maximum length as 400
    #pad them with zeros
    pad_width = max_pad_len - mfcc.shape[1]
    mfcc = np.pad(mfcc, pad_width=((0, 0), (0, pad_width)), mode='constant')
    return mfcc



def get_training_data(d):

    pairs, labels = [], []
    dirs = sorted(os.listdir('{}/data/guitar_sample'.format(CWD)))    
    
    #audio files
    di = dirs.index(d)
    afs = glob.glob('{}/data/guitar_sample/{}/*.wav'.format(CWD, d))
    
    n = len(afs)
    combs = combinations(range(0, n), 2)

    for i, j in combs:
        ri = randint(0, len(dirs)-1)
        while ri == di:
            ri = randint(0, len(dirs)-1)
                            
        #other audio files
        oafs = glob.glob('{}/data/guitar_sample/{}/*.wav'.format(CWD, dirs[ri]))
        
        k = randint(0, len(oafs)-1)
        x, y, z = audio2vector(afs[i]), audio2vector(afs[j]), audio2vector(oafs[k])
        
        #print(i, j, k)
        
        #genuine pair
        pairs.append([x, y])
        labels.append(1)

        #imposite pair
        pairs.append([y, z])
        labels.append(0)
            
            
    return np.array(pairs, dtype=float), np.array(labels, dtype=float)

def euclidean_distance(vects):
    x, y = vects
    return K.sqrt(K.sum(K.square(x - y), axis=1, keepdims=True))


def eucl_dist_output_shape(shapes):
    shape1, shape2 = shapes
    return (shape1[0], 1)


def build_base_network(input_shape):
    model = Sequential()
    
    model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=input_shape))
    model.add(Conv2D(32, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    
    model.add(Conv2D(32, kernel_size=(3, 3), activation='relu'))
    model.add(Conv2D(32, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    
    model.add(Flatten())
    model.add(Dense(1024))
    model.add(Dropout(0.1))
    
    model.add(Dense(256))
    model.add(Dropout(0.1))
    
    model.add(Dense(128))
    model.add(Dropout(0.1))
    
    return model


def distance(emb1, emb2):
    return np.sum(np.square(emb1 - emb2))


def predict(afs, y, threshold=0.5):
    print(afs.shape)
    acc = 0
    preds = model.predict([afs[:, 0], afs[:, 1]])
    for i in range(len(preds)):
        p = preds[i][0]
        z = int(p < threshold)
        if z == y[i]:
            acc += 1
        print(z, y[i], f"{p:.4f}")
    print('acc = {:.4f}%'.format(acc*100/len(preds)))

def contrastive_loss(y_true, y_pred):
    margin = 1
    return K.mean(y_true * K.square(y_pred) + (1 - y_true) * K.square(K.maximum(margin - y_pred, 0)))


class IdentityMetadata():
    def __init__(self, base, name, file):
        # dataset base directory
        self.base = base
        
        # identity name
        self.name = name
        
        # image file name
        self.file = file

    def __repr__(self):
        return self.path()

    def path(self):
        return os.path.join(self.base, self.name, self.file) 
    
def load_metadata(path):
    metadata = []
    for i in os.listdir(path):
        for f in os.listdir(os.path.join(path, i)):
            # Check file extension. Allow only jpg/jpeg' files.
            ext = os.path.splitext(f)[1]
            if ext == '.wav':
                metadata.append(IdentityMetadata(path, i, f))
    return np.array(metadata)

def get_model():
    # initialize network architecture
    input_dim = (20, 400, 1)

    audio_a = Input(shape=input_dim)
    audio_b = Input(shape=input_dim)

    base_network = build_base_network(input_dim)

    feat_vecs_a = base_network(audio_a)
    feat_vecs_b = base_network(audio_b)

    difference = Lambda(euclidean_distance, output_shape=eucl_dist_output_shape)([feat_vecs_a, feat_vecs_b])

    # initialize training params
    epochs = 64
    batch_size = 24
    optimizer = Adam() #RMSprop()

    # initialize the network
    model = Model(inputs=[audio_a, audio_b], outputs=difference)
    model.compile(loss=contrastive_loss, optimizer=optimizer)
    return model

def run(label, train=True):
    model = get_model()
    weights_path = f'weights/{label}_weights.h5'

    XX, Y = get_training_data(label)
    X = XX.reshape(tuple(list(XX.shape) + [1]))

    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)

    if train or not os.path.exists(weights_path):
        # call datasets
        audio_1 = X_train[:, 0]
        audio_2 = X_train[:, 1]

        # train model
        model.fit([audio_1, audio_2], y_train, validation_split=.25, batch_size=batch_size, verbose=0, epochs=epochs)

        # save weights
        model.save_weights(weights_path)

    else:
        # load weights
        model.load_weights(weights_path)

    # predict
    predict(X_test, y_test)

def main():
    labels = ["A", "B", "D", "E", "EH", "G"]

    for label in labels:
        print(label)
        run(label)

if __name__ == '__main__':
    main()
