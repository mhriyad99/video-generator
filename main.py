import os
from src.video_editor.video_utils import download_video, get_video_transcript, cut_clips, join_clips

os.makedirs("./downloaded_videos", exist_ok=True)
os.makedirs("./clips", exist_ok=True)
video_url = "https://www.youtube.com/watch?v=W7ppd_RY-UE"

transcript= get_video_transcript(video_url)
title = download_video(video_url, download_dir="downloaded_videos")

video_path = os.path.join("downloaded_videos", title + ".mp4")
output_dir = cut_clips(video_path, title, transcript, clips_num=3)
join_clips(output_dir, "output2.mp4")


