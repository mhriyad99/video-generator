from moviepy import VideoFileClip, concatenate_videoclips

# List of video file paths to merge
video_files = ["./assets/CGI Animated Short Film_ _Ice Cream_ by Super Dope _ @CGMeetup.mp4",
               "./assets/The Restaurant _ Funny Clip _ Mr. Bean Official.mp4"]

# Load all videos as VideoFileClip objects
clips = [VideoFileClip(file) for file in video_files]

# Concatenate the video clips
merged_clip = concatenate_videoclips(clips, method="compose")

# Export the merged video
output_file = "assets/merged_video.mp4"
merged_clip.write_videofile(output_file, codec="libx264", audio_codec="aac")

