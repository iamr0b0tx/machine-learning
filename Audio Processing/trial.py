'''
Coder: Joshua Christian
Date: Sat Oct 13, 2018 2:17pm
Project: Adam
File: trial.py
'''

# import from std lib
import os, sys, json

# import third pirty libs
import numpy as np
import cv2

class Agent:
    def __init__(self):
        self.train()

    def sense(self):
        pass

    def train(self):
        print(os.getcwd())
        with open('mnist_data/mnist_data_index.json', 'r') as file:
            images = json.loads(file.read())
        
        for image in images:
            image_path = 'mnist_data/{}.jpg'.format(image)
            
            image_data = cv2.imread(image_path)
            image_meta_data = images[image]
            print(image_data[10, 0:5, :])

            image_data = np.int8(image_data)
            image_shift = image_data * 0
            image_shift[:,:-1,:] = image_data[:,1:,:]
            print(image_shift[10, 0:5, :])

            image_shift = np.subtract(image_shift, image_data)
            print(image_shift[10, 0:5, :])
            break


if __name__ == '__main__':
    ADAM = Agent()
