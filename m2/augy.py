import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tqdm import tqdm

# Set up paths
input_dir = "/Users/maximilianvh/Downloads/finalfire"
output_dir = "./augmented_images"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Define data augmentation parameters
datagen = ImageDataGenerator(
    rotation_range=0,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)
for class_folder in os.listdir(os.path.join(input_dir)):
    if os.path.isdir(os.path.join(input_dir, class_folder)):
        os.makedirs(os.path.join(output_dir, class_folder), exist_ok=True)
        # Loop through each image file in the class folder
        for filename in tqdm(os.listdir(os.path.join(input_dir, class_folder))):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                # Load image
                img = tf.keras.preprocessing.image.load_img(
                    os.path.join(input_dir, class_folder, filename)
                )
                img_array = tf.keras.preprocessing.image.img_to_array(img)
                img_array = np.expand_dims(img_array, axis=0)
                
                # Generate augmented images
                augmented_images = datagen.flow(
                    img_array,
                    batch_size=1,
                    save_to_dir=os.path.join(output_dir, class_folder),
                    save_prefix=filename[:-4],  # remove file extension
                    save_format='jpeg'
                )
                # Save augmented images
                for i in range(5):  # Save 5 augmented versions of each image
                    batch = augmented_images[0]
                    image = batch.astype('uint8')[0]
                    tf.keras.preprocessing.image.save_img(
                        os.path.join(output_dir, class_folder, f"{filename[:-4]}_{i}.jpg"),
                        image
                    )
