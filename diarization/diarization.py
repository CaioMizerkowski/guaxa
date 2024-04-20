import torch
from dotenv import dotenv_values
from pyannote.audio import Pipeline

env = dotenv_values(".env")

pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1", use_auth_token=env["HUGGINGFACE_ACCESS_TOKEN"]
)

pipeline.to(torch.device("cuda"))
diarization = pipeline("audio.wav")

# print the result
for turn, _, speaker in diarization.itertracks(yield_label=True):
    print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
