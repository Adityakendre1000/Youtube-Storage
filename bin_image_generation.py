from PIL import Image
import io
import os
import shutil
import math

# Define folders
input_folder = 'images'
bin_images_folder = 'bin_Images'
converted_images_folder = 'converted_images'

# Create necessary folders
os.makedirs(bin_images_folder, exist_ok=True)
os.makedirs(converted_images_folder, exist_ok=True)

# YouTube video standard size
standard_width = 1280
standard_height = 720

# Get the list of all image files in the 'images' folder
image_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

# Loop through each image in the folder
for img_file_name in image_files:
    # Get the full path of the image
    image_path = os.path.join(input_folder, img_file_name)
    
    # Load the image
    image = Image.open(image_path)

    # Convert the image to binary data
    with io.BytesIO() as output:
        image.save(output, format=image.format)
        binary_data = output.getvalue()

    # Convert binary data to a binary string
    binary_string = ''.join(format(byte, '08b') for byte in binary_data)

    # Create a header with the original file name and size
    header = f"{img_file_name}:{len(binary_string)}:"
    header_binary = ''.join(format(ord(char), '08b') for char in header)
    
    # Combine header and binary data
    full_binary_string = header_binary + binary_string

    # Calculate the total number of 2x2 blocks that can fit in the standard size image
    num_blocks_width = standard_width // 2
    num_blocks_height = standard_height // 2
    total_blocks = num_blocks_width * num_blocks_height

    # Calculate the number of binary images needed
    num_images = math.ceil(len(full_binary_string) / total_blocks)

    # Create and save binary images
    for img_index in range(num_images):
        # Create a new image (mode "1" for 1-bit pixels, black and white)
        binary_image = Image.new('1', (standard_width, standard_height))
        pixels = binary_image.load()
        
        # Calculate the start and end indices for the current image
        start_index = img_index * total_blocks
        end_index = min(start_index + total_blocks, len(full_binary_string))
        
        # Get the binary string segment for the current image
        binary_segment = full_binary_string[start_index:end_index]
        
        # Pad the binary segment with '0's if it's too short to fill the image
        binary_segment = binary_segment.ljust(total_blocks, '0')
        
        # Populate the image with 2x2 blocks of pixels
        for block_y in range(num_blocks_height):
            for block_x in range(num_blocks_width):
                index = block_y * num_blocks_width + block_x
                pixel_value = int(binary_segment[index])
                
                # Set the 2x2 block of pixels
                pixels[block_x * 2, block_y * 2] = pixel_value
                pixels[block_x * 2 + 1, block_y * 2] = pixel_value
                pixels[block_x * 2, block_y * 2 + 1] = pixel_value
                pixels[block_x * 2 + 1, block_y * 2 + 1] = pixel_value
        
        # Save the new image in the 'bin_Images' folder
        output_image_name = os.path.join(bin_images_folder, f'{img_file_name}_binary_{img_index}.png')
        binary_image.save(output_image_name)
        print(f"Binary Image {img_index + 1} of {img_file_name} has been saved as {output_image_name}")

    # Close the image to release the file
    image.close()
    
    # Move the original image to 'converted_images' folder
    shutil.move(image_path, os.path.join(converted_images_folder, img_file_name))
    print(f"Original image {img_file_name} has been moved to {converted_images_folder}")

print("All images have been processed and moved to the converted_images folder.")