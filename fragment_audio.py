import os
from concurrent.futures import ThreadPoolExecutor
from itertools import chain
from pathlib import Path

from tqdm import tqdm


def process_audio(root: Path):
    audio_mp3 = root / (root.stem + ".mp3")
    split_valeu_path = root / "union.txt"

    audio_folder = root / "fragments"
    audio_folder.mkdir(exist_ok=True)

    with open(split_valeu_path) as f:
        for line in tqdm(f.readlines()):
            start_ms, end_ms, *_ = line.split()
            start_s = int(start_ms) / 1000 - 0.05
            end_s = int(end_ms) / 1000 + 0.05

            audio_name = f"{start_ms}_{end_ms}.mp3"
            audio_path = audio_folder / audio_name

            if not audio_path.exists():
                os.system(
                    f"ffmpeg -loglevel quiet -hide_banner -y -i {audio_mp3} -ss {start_s} -to {end_s} -c copy {audio_path}"
                )


executor = ThreadPoolExecutor(max_workers=16)

root1 = Path("transcricoes/guaxaverso")
root2 = Path("transcricoes/rpguaxa")
chain_root = chain(root1.iterdir(), root2.iterdir())

for root in sorted(chain_root):
    if root.is_dir():
        executor.submit(process_audio, root)
