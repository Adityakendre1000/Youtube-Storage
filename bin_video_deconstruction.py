import os
import cv2

# Define the directories
bin_videos_folder = 'bin_videos'
bin_images_folder = 'bin_Images'
video_filename = 'output_video.avi'
video_path = os.path.join(bin_videos_folder, video_filename)

# Create bin_images_folder if it doesn't exist
if not os.path.exists(bin_images_folder):
    os.makedirs(bin_images_folder)

# Open the video file
video_capture = cv2.VideoCapture(video_path)

# Get the total number of frames and frame rate
total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
frame_rate = video_capture.get(cv2.CAP_PROP_FPS)
print(f"Total frames in video: {total_frames}")
print(f"Frame rate of video: {frame_rate}")

frame_count = 0
while True:
    ret, frame = video_capture.read()
    if not ret:
        break
    frame_filename = f"frame_{frame_count:04d}.png"
    frame_path = os.path.join(bin_images_folder, frame_filename)
    cv2.imwrite(frame_path, frame)
    frame_count += 1

# Release the video capture object
video_capture.release()

print(f"Extracted {frame_count} frames from the video and saved them in {bin_images_folder}")