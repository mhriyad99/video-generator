import json
from urllib.parse import urlparse, parse_qs

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from pydantic import BaseModel, Field
from youtube_transcript_api import YouTubeTranscriptApi

# from src.video_editor.video_utils import get_youtube_video_id

template = """You are an expert in summarizing video transcripts. Your task is to provide a **1500-word summary** of the given transcript. The summary should:
- Be concise and capture the key points from the transcript.
- Be approximately 1500 words in length.
- Provide a coherent overview of the content, without including every detail.

Transcript:
{transcript_text}

Provide the results in JSON format:
- summary:  summary in a single, continuous paragraph"""
prompt = ChatPromptTemplate.from_template(template)
model = OllamaLLM(model="llama3.2", temperature=0.2, format='json')
chain = prompt | model


class Segment(BaseModel):
    summary: str = Field(..., description="Summary of the segment")


def parse_object_from_string(raw_response)->Segment:
    """
    Parse a JSON object from a raw string response.

    Args:
        raw_response (str): The raw response string containing a JSON object.

    Returns:
        dict: The parsed JSON object as a dictionary.
    """
    try:
        start_index = raw_response.index("{")
        json_str = raw_response[start_index:]
        parsed_object = json.loads(json_str)
        return Segment(**parsed_object)
    except (ValueError, json.JSONDecodeError) as e:
        print(f"Error parsing JSON: {e}")
        return None


def main(url:str)-> Segment:

    video_id = get_youtube_video_id(url)
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        exit(1)

    transcript_text = "\n".join([f"[{entry['start']}] {entry['text']}" for entry in transcript])
    while True:
        try:
            response = chain.invoke({"transcript_text": transcript_text})
            segments = parse_object_from_string(response)
            return segments
        except Exception as e:
            pass



def get_youtube_video_id(url):
    """
    Extract the video ID from a YouTube URL.

    Args:
        url (str): The YouTube video URL.

    Returns:
        str: The video ID if found, otherwise None.
    """
    try:
        # Parse the URL
        parsed_url = urlparse(url)
        # Extract query parameters
        query_params = parse_qs(parsed_url.query)
        # Return the video ID
        return query_params.get("v", [None])[0]
    except Exception as e:
        print(f"Error extracting video ID: {e}")
        return None


if __name__ == "__main__":
    main("https://www.youtube.com/watch?v=lfdt4Vs-yw8")