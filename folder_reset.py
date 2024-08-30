import os
import shutil

# Define the directories
converted_images_folder = 'converted_images'
images_folder = 'images'
reconstructed_images_folder = 'reconstructed_images'
bin_images_folder = 'bin_Images'

# Move all images from converted_images_folder to images_folder
for filename in os.listdir(converted_images_folder):
    file_path = os.path.join(converted_images_folder, filename)
    if os.path.isfile(file_path):
        shutil.move(file_path, os.path.join(images_folder, filename))
        print(f"Moved {filename} to {images_folder}")

# Delete all images from reconstructed_images_folder
for filename in os.listdir(reconstructed_images_folder):
    file_path = os.path.join(reconstructed_images_folder, filename)
    if os.path.isfile(file_path):
        os.remove(file_path)
        print(f"Deleted {filename} from {reconstructed_images_folder}")

# Delete all images from bin_images_folder
for filename in os.listdir(bin_images_folder):
    file_path = os.path.join(bin_images_folder, filename)
    if os.path.isfile(file_path):
        os.remove(file_path)
        print(f"Deleted {filename} from {bin_images_folder}")