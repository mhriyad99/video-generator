from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List


class Segment(BaseModel):
    """ Represents a segment of a video"""
    start_time: float = Field(..., description="The start time of the segment in seconds")
    end_time: float = Field(..., description="The end time of the segment in seconds")
    yt_title: str = Field(..., description="The youtube title to make this segment as a viral sub-topic")
    description: str = Field(..., description="The detailed youtube description to make this segment viral ")
    duration : int = Field(..., description="The duration of the segment in seconds")


class VideoTranscript(BaseModel):
    """ Represents the transcript of a video with identified viral segments"""
    segments: List[Segment] = Field(..., description="List of viral segments in the video")