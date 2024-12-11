import os
from src.video_editor.video_utils import download_video, get_video_transcript, cut_clips, join_clips, add_audio_to_video_ffmpeg, get_video_length
from fastapi import FastAPI
from pydantic import BaseModel
from src.video_editor.lnc import main as summarizer
from src.video_editor.tts import main as tts
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
    join_clips(output_dir, "video.mp4")
    summary = summarizer(url=video_url)
    tts(summary.summary)
    # length_in_seconds = get_video_length(video_path)
    add_audio_to_video_ffmpeg("video.mp4", "audio.mp3", "final.mp4")
    return {"result": "ok"}




