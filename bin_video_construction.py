import os
import cv2
import numpy as np

# Define the directories
bin_images_folder = 'bin_Images'
bin_videos_folder = 'bin_videos'
video_filename = 'output_video.avi'
video_path = os.path.join(bin_videos_folder, video_filename)

# Get all image files from bin_images_folder
image_files = sorted([f for f in os.listdir(bin_images_folder) if f.endswith('.png')])

# Determine the maximum dimensions
max_width = 0
max_height = 0
for image_file in image_files:
    image_path = os.path.join(bin_images_folder, image_file)
    frame = cv2.imread(image_path)
    height, width, _ = frame.shape
    if width > max_width:
        max_width = width
    if height > max_height:
        max_height = height

# Create a VideoWriter object
frame_rate = 12
frame_size = (max_width, max_height)
video_writer = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'XVID'), frame_rate, frame_size)

# Write each image to the video
frame_count = 0
for image_file in image_files:
    image_path = os.path.join(bin_images_folder, image_file)
    frame = cv2.imread(image_path)
    if frame is None:
        print(f"Failed to read frame: {image_file}")
        continue
    
    # Resize the image while maintaining aspect ratio
    h, w, _ = frame.shape
    scale = min(max_width / w, max_height / h)
    new_w = int(w * scale)
    new_h = int(h * scale)
    resized_frame = cv2.resize(frame, (new_w, new_h))
    
    # Pad the resized image to the maximum dimensions
    top = (max_height - new_h) // 2
    bottom = max_height - new_h - top
    left = (max_width - new_w) // 2
    right = max_width - new_w - left
    padded_frame = cv2.copyMakeBorder(resized_frame, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0, 0, 0])
    
    video_writer.write(padded_frame)
    frame_count += 1
    print(f"Writing frame {frame_count}: {image_file}")

# Release the VideoWriter object
video_writer.release()

# Calculate and print the duration of the video
video_duration = frame_count / frame_rate
print(f"The video has been saved as {video_path}")
print(f"The duration of the video is {video_duration} seconds")
print(f"Total frames written: {frame_count}")
print(f"Frame rate: {frame_rate}")