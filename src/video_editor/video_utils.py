import os
import re
import random
import shutil
import subprocess
from yt_dlp import YoutubeDL
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from moviepy import VideoFileClip, concatenate_videoclips, AudioFileClip, CompositeVideoClip


def sanitize_filename(name):
    """Sanitize a filename by removing invalid characters and quotes."""
    # Remove invalid characters and replace spaces with underscores
    sanitized = re.sub(r'[<>:"/\\|?*]', '', name).strip().replace(' ', '_')
    # Remove single and double quotes
    sanitized = sanitized.replace("'", '').replace('"', '')
    return sanitized


def get_video_info(video_url):
    """Get video info using yt_dlp without downloading."""
    ydl_opts = {
        'skip_download': True,  # Skip downloading the video
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
    return info


def download_video(video_url, download_dir):
    """Download the video with a sanitized title."""
    os.makedirs(download_dir, exist_ok=True)

    # Get video info first
    info = get_video_info(video_url)
    video_title = info.get('title')  # Extract the title

    # Sanitize the video title
    sanitized_title = sanitize_filename(video_title)
    output_path = os.path.join(download_dir, f"{sanitized_title}.%(ext)s")

    # Download the video with the sanitized title
    ydl_opts = {
        'outtmpl': output_path,  # Use the sanitized title for the output file
        'format': 'bv[height=480]',  # Download video with 480p height
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    return sanitized_title


def get_video_transcript(video_url:str):
    yt = YouTube(video_url)
    video_id = yt.video_id
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return transcript


def cut_clips(video_path: str, title:str,transcript: list, clips_num: int):

    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    if not shutil.which("ffmpeg"):
        raise EnvironmentError("FFmpeg is not installed or not in PATH.")


    output_dir = os.path.join("clips", title)
    os.makedirs(output_dir, exist_ok=True)

    # Select random clips from the transcript
    selected_clips = random.sample(transcript, min(clips_num, len(transcript)))
    print(selected_clips)
    for idx, clip in enumerate(selected_clips):
        print(clip)
        start_time = clip["start"]
        duration = clip["duration"] + 3
        output_clip_path = os.path.join(output_dir, f"clip_{idx + 1}.mp4")

        # FFmpeg command to cut the clip
        command = [
            "ffmpeg",
            "-i", video_path,
            "-ss", str(start_time),
            "-t", str(duration),
            "-c:v", "copy",
            "-c:a", "copy",
            output_clip_path
        ]

        try:
            subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"Clip {idx + 1} saved to {output_clip_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error cutting clip {idx + 1}: {e.stderr.decode('utf-8')}")

    return output_dir


# def join_clips(output_dir, final_video_path):
#     """Join video clips into a single video."""
#     # Create a concatenation file listing all clips
#     concat_file_path = os.path.join(output_dir, "concat_list.txt")
#     with open(concat_file_path, "w") as concat_file:
#         for clip_name in sorted(os.listdir(output_dir)):
#             if clip_name.endswith(".mp4") and clip_name.startswith("clip_"):
#                 # Use forward slashes in paths
#                 full_path = os.path.join(output_dir, clip_name).replace("\\", "/")
#                 concat_file.write(f"file '{full_path}'\n")
#
#     # Use ffmpeg to join clips
#     try:
#         subprocess.run([
#             "ffmpeg", "-f", "concat", "-safe", "0", "-i", concat_file_path,
#             "-c", "copy", final_video_path
#         ], check=True)
#         print(f"Final video created successfully: {final_video_path}")
#     except subprocess.CalledProcessError as e:
#         print(f"Error joining clips: {e}")
#         raise


def join_clips(output_dir, final_video_path):
    """Concatenate video clips using moviepy."""
    clips = []
    for clip_name in sorted(os.listdir(output_dir)):
        if clip_name.endswith(".mp4") and clip_name.startswith("clip_"):
            # Load the clip using VideoFileClip
            clip_path = os.path.join(output_dir, clip_name)
            clips.append(VideoFileClip(clip_path))

    if not clips:
        raise ValueError("No clips found to concatenate!")

    # Concatenate clips
    final_clip = concatenate_videoclips(clips, method="compose")

    # Write the final video
    final_clip.write_videofile(final_video_path, codec="libx264", audio_codec="aac")
    print(f"Final video created successfully: {final_video_path}")


def add_audio_to_video(video_path, audio_path, output_path):
    """Add audio to a video using moviepy."""
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)

    # Adjust audio duration to match video (optional)
    audio_clip = audio_clip.set_duration(video_clip.duration)

    final_clip = video_clip.set_audio(audio_clip)

    output_path = f"{output_path}"
    final_clip.write_videofile(output_path, audio_codec='aac')


def add_audio_to_video_ffmpeg(video_path, audio_path, output_path):
    """Add audio to a video using ffmpeg."""
    command = [
        "ffmpeg",
        "-i", video_path,
        "-i", audio_path,
        "-c:v", "copy",
        "-c:a", "aac",
        "-strict", "experimental",
        output_path
    ]
    try:
        subprocess.run(command, check=True)
        print(f"Video with audio saved as: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error adding audio to video: {e}")
