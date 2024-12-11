from typing import List

from langchain.prompts import PromptTemplate


temp_llama_question_router = PromptTemplate(
    template=f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|> Provided to you is a transcript of a video. 
                    Please identify all segments that can be extracted as 
                    subtopics from the video based on the transcript.
                    Make sure each segment is between 30-500 seconds in duration.
                    Make sure you provide extremely accruate timestamps
                    and respond only in the format provided. 
                    \n Here is the transcription : \n {transcript}
                  <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
                  input_variables=["question"],
)