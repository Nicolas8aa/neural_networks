# -*- coding: utf-8 -*-
"""DL_ex_1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Y57_pSdeW8qcOXlpV3Dq2pCLw7eaimzI
"""

from keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
from keras.models import Sequential
from keras import layers
import matplotlib.pyplot as plt
import numpy as np

(X_train, y_train), (X_test, y_test) = mnist.load_data()

num_train_samples = X_train.shape[0]
num_test_samples = y_test.shape[0]
image_height = X_train.shape[1]
image_width = X_train.shape[2]
print("X_train.shape: " + str(X_train.shape))
print("X_test.shape: " + str(X_test.shape))
print("y_train.shape: " + str(y_train.shape))
print("y_test.shape: " + str(y_test.shape))
print("y_train sample 5 value: " + str(y_train[5]))
print("Train samples: " + str(num_train_samples))
print("Test samples: " + str(num_test_samples))
print("Image height: " + str(image_height))
print("Image width: " + str(image_width))

# Conv2D expects 4 dimmensions; the last one is the number of channels
num_channels = 1

X_train = X_train.reshape(num_train_samples,image_height,
                          image_width,num_channels)
X_test = X_test.reshape(num_test_samples,image_height,
                        image_width,num_channels)

X_train = X_train / 255   # values [0..1] improve results
X_test = X_test / 255

# np_utils is deprecated, use to_categorical directly
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

print("categorical y_train shape: " + str(y_train.shape))
print("categorical y_train sample 5 value: " + str(y_train[5]))
num_classes = y_test.shape[1]
print("Number of classes: " + str(num_classes))

model = Sequential()
model.add(layers.Conv2D(16, (3,3), activation='relu', input_shape=(image_height,image_width,num_channels)))
model.add(layers.MaxPooling2D((2,2)))
model.add(layers.Conv2D(32, (3,3), activation='relu'))
model.add(layers.MaxPooling2D((2,2)))
model.add(layers.Conv2D(64, (3,3), activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(32, activation='relu'))
model.add(layers.Dense(num_classes, activation='softmax'))

print(model.summary())

EPOCHS = 20
model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
history = model.fit(X_train, y_train, validation_data=(X_test, y_test),
                    epochs=EPOCHS, batch_size=128, verbose=0)

def plot(h):
    LOSS = 0; ACCURACY = 1
    training = np.zeros((2,EPOCHS)); testing = np.zeros((2,EPOCHS))
    training[LOSS] = h.history['loss']
    testing[LOSS] = h.history['val_loss']    # validation loss
    training[ACCURACY] = h.history['acc']
    testing[ACCURACY] = h.history['val_acc']  # validation accuracy

    epochs = range(1,EPOCHS+1)
    fig, axs = plt.subplots(1,2, figsize=(17,5))
    for i, label in zip((LOSS, ACCURACY),('loss', 'accuracy')):
        axs[i].plot(epochs, training[i], 'b-', label='Training ' + label)
        axs[i].plot(epochs, testing[i], 'y-', label='Test ' + label)
        axs[i].set_title('Training and test ' + label)
        axs[i].set_xlabel('Epochs')
        axs[i].set_ylabel(label)
        axs[i].legend()
    plt.show()
    loss, accuracy = model.evaluate(X_test,y_test,verbose=0)
    print("Loss: " + str(loss))
    print("Accuracy: " + str(accuracy))

plot(history)