import os
import cv2

# Define the directory
bin_videos_folder = 'bin_videos'

# Iterate over all video files in the bin_videos_folder
for video_file in os.listdir(bin_videos_folder):
    if video_file.endswith('.avi'):
        video_path = os.path.join(bin_videos_folder, video_file)
        
        # Open the video file
        video_capture = cv2.VideoCapture(video_path)
        
        # Get the total number of frames
        total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Get the frame rate
        frame_rate = video_capture.get(cv2.CAP_PROP_FPS)
        
        # Calculate the duration of the video
        duration = total_frames / frame_rate
        
        # Print the total number of frames and duration
        print(f"Video: {video_file}")
        print(f"Total Frames: {total_frames}")
        print(f"Duration: {duration:.2f} seconds")
        
        # Release the video capture object
        video_capture.release()