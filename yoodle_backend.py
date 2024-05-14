import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import cv2



class MyModel:
    def __init__(self):
        self.model = tf.keras.models.load_model("yoodle\model\yoodle_1.h5")


    def classify(self, img, label):

        rgb_array = np.delete(arr=img, obj=3, axis=2)
        target_size = (256, 256)
        img_gray = cv2.resize(rgb_array, target_size)

        
        weights = np.array([0.299, 0.587, 0.114])
        grayscale = np.dot(img_gray, weights)
        resized_data = grayscale / 255.0
        input_tensor = np.expand_dims(resized_data, axis=-1)  # Add a channel dimension
        # Reshape the input tensor to match the model's expected input shape

        input_tensor = np.expand_dims(input_tensor, axis=0)  # Add a batch 
        print("---------------------------------------")
        print(input_tensor.shape) 
        print("Input Tensor Shape:", input_tensor.shape)

        real_predictions = self.model.predict(input_tensor)

        real_pred = [np.argmax(pred) for pred in real_predictions]
        print(f"prediction: {real_pred}")
        return real_pred

