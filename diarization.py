from itertools import chain
from pathlib import Path

import torch
import torchaudio
from dotenv import dotenv_values
from pyannote.audio import Pipeline
from pyannote.audio.pipelines.utils.hook import ProgressHook

env = dotenv_values(".env")
pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.0",
    use_auth_token=env["HUGGINGFACE_ACCESS_TOKEN"],
)
pipeline.to(torch.device("cuda"))


def diarize(audio_path):
    waveform, sample_rate = torchaudio.load(str(audio_path))
    audio_in_memory = {"waveform": waveform, "sample_rate": sample_rate}

    with ProgressHook() as hook:
        diarization = pipeline(
            audio_in_memory,
            hook=hook,
        )

    output_path = Path(audio_path).parent / "diarization.txt"
    with open(output_path, "w") as f:
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            f.write(
                f"start={int(turn.start*1000)}ms stop={int(turn.end*1000)}ms speaker_{speaker}\n"
            )


if __name__ == "__main__":
    root1 = Path("transcricoes/guaxaverso")
    root2 = Path("transcricoes/rpguaxa")
    chain_root = chain(root1.iterdir(), root2.iterdir())

    for dir in sorted(chain_root):
        audio_path = dir / (dir.stem + ".mp3")

        if not (dir / "diarization.txt").exists():
            print(audio_path)
            diarize(audio_path)
