import sys

from moviepy import VideoFileClip


def remove_audio(input_file: str, output_file: str):
    video = VideoFileClip(input_file)
    video_without_audio = video.without_audio()
    video_without_audio.write_videofile(output_file, codec="libx264", audio_codec="none")


remove_audio('./downloaded_videos/CGI Animated Short Film_ _Ice Cream_ by Super Dope _ @CGMeetup.mp4',
             './downloaded_videos/without_audio.mp4')