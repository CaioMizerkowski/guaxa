. .venv/bin/activate
pip install -r app_requirements.txt
python scripts/download.py
python scripts/union.py
python scripts/fragment_audio.py
python scripts/txt2csv.py
python scripts/csv2json.py

python gradio/app.py
