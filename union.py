from itertools import chain
from pathlib import Path


def process_diarization(dia: list[str]):
    if "ms" in dia[0]:
        dia = [
            line.replace("ms", "")
            .replace("start=", "")
            .replace("stop=", "")
            .replace("speaker_SPEAKER_", "")
            .strip()
            .split()
            for line in dia
        ]

    else:
        dia = [
            line.replace("start=", "")
            .replace("stop=", "")
            .replace("speaker_SPEAKER_", "")
            .strip()
            .split()
            for line in dia
        ]
        dia = [
            (
                float(start.replace("s", "")) * 1000,
                float(stop.replace("s", "")) * 1000,
                speaker,
            )
            for start, stop, speaker in dia
        ]

    return [(int(start), int(stop), speaker) for start, stop, speaker in dia]


def process_transcription(trans: list[str]):
    trans = [line.strip().split("\t") for line in trans]
    return [(int(t[0]), int(t[1]), t[2]) for t in trans if len(t) == 3]


def intersection_1d(start_a: int, stop_a: int, start_b: int, stop_b: int) -> int:
    return max(0, min(stop_a, stop_b) - max(start_a, start_b))


def union_1d(
    start_a: int, stop_a: int, start_b: int, stop_b: int, intersection: int
) -> int:
    return (stop_a - start_a) + (stop_b - start_b) - intersection


def iou_1d(start_a: int, stop_a: int, start_b: int, stop_b: int) -> float:
    intersection = intersection_1d(start_a, stop_a, start_b, stop_b)
    union = union_1d(start_a, stop_a, start_b, stop_b, intersection)
    return intersection / union


def create_union(folder: Path):
    diarization_path = folder / "diarization.txt"
    transcription_path = folder / (folder.stem + ".tsv")
    result = []

    with open(diarization_path) as f:
        diarization = process_diarization(f.readlines())

    with open(transcription_path) as f:
        transcription = process_transcription(f.readlines()[1:])

    for start_t, stop_t, text in transcription:
        speakers = set()
        for start_d, stop_d, speaker in diarization:
            if intersection_1d(start_t, stop_t, start_d, stop_d) > 0:
                speakers.add(speaker)

        if not len(speakers):
            speakers.add("unknown")

        result.append((speakers, start_t, stop_t, text))

    return result


if __name__ == "__main__":
    root1 = Path("transcricoes/guaxaverso")
    root2 = Path("transcricoes/rpguaxa")

    for folder in chain(root1.iterdir(), root2.iterdir()):
        output: Path = folder / "union.txt"
        if output.exists():
            continue

        print(folder)

        result = create_union(folder)
        with open(output, "w") as f:
            for speakers, start, stop, text in result:
                f.write(f"{start} {stop} ({', '.join(speakers)}) {text}\n")
