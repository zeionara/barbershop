import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import imread, imsave

def get_image_data(path):
    return imread(path).astype(np.float32)

image_data = get_image_data("ava.png")
print('Size: ', image_data.size)
print('Shape: ', image_data.shape)

print(type(image_data.all()))
print(image_data.tolist())
scaled_image_data = image_data / 255
plt.imshow(scaled_image_data)
plt.show()