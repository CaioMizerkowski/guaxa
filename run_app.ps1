# powershell version of run_app.sh
# Usage: ./run_app.ps1

# run pip install from requirements.txt
pip install -r app_requirements.txt

python scripts/download.py
python scripts/union.py
python scripts/fragment_audio.py
python scripts/txt2csv.py
python scripts/csv2json.py

python gradio/app.py
