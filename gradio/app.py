import gradio as gr
from pathlib import Path
from natsort import natsorted


class ProcessData:
    def __init__(self) -> None:
        root = Path("a__espera_rpguaxa_153")

        self.fragments = natsorted(root.glob("fragments/*.mp3"))
        self.texts_revision = root / "revision.txt"

        with open(root / "union.txt", "r") as f:
            self.texts = [t.strip() for t in f.readlines()]

        try:
            with open(self.texts_revision, "r") as f:
                last_line = f.readlines()[-1]
                first_item = last_line.split(";")[0]
                self.idx = int(first_item) + 2
        except Exception as e:
            print(e)
            self.idx = 0

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

        print(f"loop:{self.idx}, text:{text}, prev:{prev_text}")

        audio = self.fragments[self.idx]
        self.idx += 1
        return text, audio


if __name__ == "__main__":
    process_data = ProcessData()
    inp = gr.Textbox()
    audio = gr.Audio(autoplay=True)
    demo = gr.Interface(
        process_data.loop, [inp, audio], [inp, audio], submit_btn="Next"
    )
    demo.launch()
