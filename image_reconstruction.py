from PIL import Image
import io
import os

# Define folders
bin_images_folder = 'bin_Images'
reconstructed_images_folder = 'reconstructed_images'

# Create the reconstructed_images folder if it doesn't exist
os.makedirs(reconstructed_images_folder, exist_ok=True)

# Collect all binary image files
binary_files = [f for f in os.listdir(bin_images_folder) if f.endswith('.png')]
binary_files.sort()  # Ensure files are read in the correct order

# YouTube video standard size
standard_width = 1280
standard_height = 720

# Process binary files to reconstruct images
i = 0
while i < len(binary_files):
    binary_string = ''
    base_name = None
    original_size = None

    while i < len(binary_files):
        binary_image_path = os.path.join(bin_images_folder, binary_files[i])
        binary_image = Image.open(binary_image_path)
        width, height = binary_image.size

        # Extract the binary string from the image
        pixels = binary_image.load()
        num_blocks_width = standard_width // 2
        num_blocks_height = standard_height // 2

        for block_y in range(num_blocks_height):
            for block_x in range(num_blocks_width):
                # Check the top-left pixel of the 2x2 block to determine the bit value
                pixel_value = pixels[block_x * 2, block_y * 2]
                binary_string += '1' if pixel_value == 255 else '0'

        # Check for header (file name and size)
        if base_name is None:
            header_end_index = binary_string.find('0011101000111010')  # ':' in binary
            if header_end_index != -1:
                header_binary = binary_string[:header_end_index + 16]
                header = ''.join(chr(int(header_binary[i:i+8], 2)) for i in range(0, len(header_binary), 8))
                base_name, original_size = header.split(':')
                original_size = int(original_size)
                binary_string = binary_string[header_end_index + 16:]
            else:
                # If header not found, continue collecting data
                i += 1
                continue

        # Check if we have collected enough data
        if len(binary_string) >= original_size:
            binary_string = binary_string[:original_size]
            break

        # Move to the next file if not enough data
        i += 1

    # Convert the binary string back to binary data
    binary_data = bytearray()
    for j in range(0, len(binary_string), 8):
        byte = binary_string[j:j+8]
        binary_data.append(int(byte, 2))

    # Reconstruct the original image from the binary data
    try:
        original_image = Image.open(io.BytesIO(binary_data))
        # Save the reconstructed image in the 'reconstructed_images' folder
        reconstructed_image_path = os.path.join(reconstructed_images_folder, base_name)
        original_image.save(reconstructed_image_path)
        print(f"Reconstructed image has been saved as {reconstructed_image_path}")

        # Remove all binary image files used for reconstruction
        for file_to_remove in binary_files[:i+1]:
            os.remove(os.path.join(bin_images_folder, file_to_remove))
            print(f"Binary image {file_to_remove} has been deleted.")
        
        # Update the list of binary files after deletion
        binary_files = [f for f in os.listdir(bin_images_folder) if f.endswith('.png')]
        binary_files.sort()  # Ensure files are read in the correct order

    except Exception as e:
        print(f"Error reconstructing the image {base_name}: {e}")

    # Move to the next batch of binary images
    i = 0  # Restart the loop with updated binary files list

print("All images have been processed and removed.")