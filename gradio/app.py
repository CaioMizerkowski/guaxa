from itertools import chain
from pathlib import Path

from natsort import natsorted

import gradio as gr

root = Path()


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

        print(f"idx:{self.idx}")

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

        text = ";".join(self.texts[self.idx].split(";")[2:])

        audio = self.fragments[self.idx]
        self.idx += 1
        return text, audio


def selecao(episodio: Path):
    global root
    root = Path(episodio)
    process_data.init(root)


if __name__ == "__main__":
    process_data = ProcessData()

    root1 = Path("transcricoes/guaxaverso")
    root2 = Path("transcricoes/rpguaxa")
    chain_root = chain(root1.iterdir(), root2.iterdir())
    episode_list = list(chain_root)
    dropdown = gr.Dropdown(episode_list, label="Escolher episodio")
    choice = gr.Interface(selecao, dropdown, None)

    inp = gr.Textbox()
    audio = gr.Audio(autoplay=True)
    episode = gr.Interface(
        process_data.loop, [inp, audio], [inp, audio], submit_btn="Next"
    )

    gr.TabbedInterface([choice, episode], ["Seleção", "Episodio"]).launch()
