import textwrap

import nltk
import numpy as np
import torch
import torchaudio
from datasets import load_dataset
from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan

nltk.download('punkt')
nltk.download('punkt_tab')

checkpoint = "microsoft/speecht5_tts"
processor = SpeechT5Processor.from_pretrained(checkpoint)
model = SpeechT5ForTextToSpeech.from_pretrained(checkpoint)
vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")

embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
speaker_embedding = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)


def split_text_into_chunks(text, max_length=600):
    inputs = processor(text=text, return_tensors="pt")
    input_length = inputs["input_ids"].shape[1]

    if input_length <= max_length:
        return [text]

    words = text.split()
    wrapped_text = textwrap.wrap(' '.join(words), width=max_length)
    return wrapped_text


def add_pause_between_sentences(text):
    sentences = nltk.sent_tokenize(text)

    return " ".join([sentence + " ..." for sentence in sentences])


def main(text: str):
    print(f"Input Text: {text[:100]}...")

    text_with_pauses = add_pause_between_sentences(text)

    text_chunks = split_text_into_chunks(text_with_pauses)

    all_speech = []

    for chunk in text_chunks:
        print(f"Processing chunk: {chunk[:50]}...")

        inputs = processor(text=chunk, return_tensors="pt")

        speech = model.generate_speech(inputs["input_ids"], speaker_embedding, vocoder=vocoder)

        all_speech.append(speech.unsqueeze(0))

    final_speech = torch.cat(all_speech, dim=-1)

    final_speech = final_speech.squeeze(0).cpu().numpy()
    final_speech = np.int16(final_speech * 32767)

    output_file = "audio.mp3"
    torchaudio.save(output_file, torch.tensor(final_speech).unsqueeze(0), sample_rate=16000)

    return output_file


