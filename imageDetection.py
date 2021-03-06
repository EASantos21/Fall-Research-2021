from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
from tensorflow.keras.optimizers import RMSprop
import matplotlib.pyplot as plt
import tensorflow as tf 
import numpy as np 
import cv2 
import os
import time

'''
img = image.load_img('training/shirts/shirt1.jpg')
plt.imshow(img)
#plt.show()
img2 = cv2.imread('training/shirts/shirt1.jpg')
dimensions = img2.shape
print(dimensions)
'''
train = ImageDataGenerator(rescale=1/255)
validation = ImageDataGenerator(rescale=1/255)
train_dataset = train.flow_from_directory('training/',
                                         target_size= (200,200),
                                         batch_size= 3,
                                         class_mode= 'binary')

validation_dataset = train.flow_from_directory('validation/',
                                         target_size= (200,200),
                                         batch_size= 3,
                                         class_mode= 'binary')

#print(train_dataset.class_indices)


model = tf.keras.models.Sequential([tf.keras.layers.Conv2D(16,(3,3), activation='relu',input_shape=(200,200,3)),
                                    tf.keras.layers.MaxPool2D(2,2),
                                    #
                                    tf.keras.layers.Conv2D(32,(3,3), activation='relu'),
                                    tf.keras.layers.MaxPool2D(2,2),
                                    #
                                    tf.keras.layers.Conv2D(64,(3,3), activation='relu'),
                                    tf.keras.layers.MaxPool2D(2,2),
                                    ##
                                    tf.keras.layers.Flatten(),
                                    ##
                                    tf.keras.layers.Dense(512,activation='relu'),
                                    ##
                                    tf.keras.layers.Dense(1,activation='sigmoid')
                                    ]) 

model.compile(loss='binary_crossentropy',
             optimizer=RMSprop(lr=0.001),
             metrics=['accuracy'])

model_fit = model.fit(train_dataset,
                    steps_per_epoch=6,
                    epochs=11,
                    validation_data=validation_dataset)

#print(model_fit)
#print(model.summary())
model.save("layDownDetector.h5py")
dir_path = 'testing/'
for i in os.listdir(dir_path):
    img = image.load_img(dir_path+'//'+i, target_size=(200,200))
    plt.imshow(img)
    X = image.img_to_array(img)
    X = np.expand_dims(X, axis = 0)
    images = np.vstack([X])
    val = model.predict(images)
    if val == 0:
        print("not laying down")
    else:
        print("laying down")
    plt.show()

