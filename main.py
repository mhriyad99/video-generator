import os
from src.video_editor.video_utils import download_video, get_video_transcript, cut_clips, join_clips, add_audio_to_video_ffmpeg
from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()


os.makedirs("./downloaded_videos", exist_ok=True)
os.makedirs("./clips", exist_ok=True)

class Request(BaseModel):
    video_url: str

@app.post('/')
def get_generated_video(request: Request):
    video_url = request.video_url

    transcript = get_video_transcript(video_url)
    title = download_video(video_url, download_dir="downloaded_videos")

    video_path = os.path.join("downloaded_videos", title + ".mp4")
    output_dir = cut_clips(video_path, title, transcript, clips_num=3)
    join_clips(output_dir, "output.mp4")
    # add_audio_to_video_ffmpeg("output.mp4", "Rome.mp3", "final.mp4")
    return {"result": "ok"}