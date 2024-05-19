from itertools import chain
from pathlib import Path
from dotenv import dotenv_values
from natsort import natsorted

import gradio as gr

root = Path()
speakers_names = {}


class ProcessData:
    def __init__(self) -> None:
        pass

    def init(self, root: Path):
        self.fragments = natsorted(root.glob("fragments/*.mp3"))
        self.texts_revision = root / "revision.txt"

        with open(root / "union.csv", "r") as f:
            self.texts = [t.strip() for t in f.readlines()]

        self.idx = 0
        if self.texts_revision.exists() and self.texts_revision.stat().st_size > 0:
            with open(self.texts_revision, "r") as f:
                last_line = f.readlines()[-1]
                first_item = last_line.split(";")[0]
                self.idx = int(first_item) + 2
        else:
            self.texts_revision.touch()

    def save_prev(self, prev_text: str):
        prev_idx = self.idx - 1

        if prev_idx < 0:
            return

        if prev_text == "":
            self.idx -= 1
            return

        prev_time = ";".join(self.texts[prev_idx].split(";")[:2])

        with open(self.texts_revision, "a") as f:
            f.write(f"{prev_idx};{prev_time};{prev_text}\n")

        return

    def loop(self, prev_text: str, a: Path):
        self.save_prev(prev_text)
        speakers, text = self.texts[self.idx].split(";")[2:]

        if speakers_names:
            speakers = speakers.replace('"', "").replace(" ", "").split(",")
            for i, speaker in enumerate(speakers):
                speakers[i] = speakers_names.get(speaker, speaker)
            speakers = ", ".join(speakers)

        text = f"{speakers};{text}"

        audio = self.fragments[self.idx]
        self.idx += 1
        return text, audio


class ProcessDataSpeakers:
    def __init__(self) -> None:
        pass

    def init(self, root: Path):
        self.fragments = natsorted(root.glob("fragments/*.mp3"))

        with open(root / "union.csv", "r") as f:
            self.texts = [t.strip() for t in f.readlines()]

        self.speakers_names: dict[str, str] = {}
        self.speakers_fragments: dict[str, Path] = {}
        self.prev_speaker = None

        self.create_speakers()

    def create_speakers(self):
        for text, fragment in zip(self.texts, self.fragments):
            id_speaker = text.split(";")[2].replace('"', "")

            if not id_speaker.isdecimal():
                continue

            if fragment.stat().st_size < 5000:
                continue

            if not (id_speaker in self.speakers_fragments):
                self.speakers_fragments[id_speaker] = fragment

    def loop_speaker(self, speaker_name: str, a: Path):
        if self.prev_speaker and speaker_name != "Fim":
            self.speakers_names[self.prev_speaker] = speaker_name

        if not self.speakers_fragments:
            global speakers_names
            speakers_names = self.speakers_names
            print(speakers_names)
            return "Fim", None

        new_speaker, audio = self.speakers_fragments.popitem()
        self.prev_speaker = new_speaker
        return new_speaker, audio


def selecao(episodio: Path):
    global root, speakers_names
    speakers_names = {}
    root = Path(episodio)
    process_data.init(root)
    process_speaker.init(root)


if __name__ == "__main__":
    process_data = ProcessData()
    process_speaker = ProcessDataSpeakers()

    categories = dotenv_values(".env")["CATEGORIES"].split(",")
    iterdirs = [(Path("transcricoes") / cat).iterdir() for cat in categories]

    chain_root = chain(*iterdirs)

    episode_list = list(chain_root)
    dropdown = gr.Dropdown(episode_list, label="Escolher episodio")
    choice = gr.Interface(selecao, dropdown, None)

    inp = gr.Textbox()
    audio = gr.Audio(autoplay=True)
    episode = gr.Interface(
        process_data.loop,
        [inp, audio],
        [inp, audio],
        submit_btn="Next",
        allow_flagging="never",
    )

    name = gr.Textbox()
    audio_speaker = gr.Audio(autoplay=True)
    speaker = gr.Interface(
        process_speaker.loop_speaker, [name, audio_speaker], [name, audio_speaker]
    )

    gr.TabbedInterface(
        [choice, episode, speaker], ["Seleção", "Episodio", "Personagem"]
    ).launch()
