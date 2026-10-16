"""Regenerate voice lines until a local whisper transcription matches the script.
    FISH_API_KEY=... python scripts/video/tts_check.py SCRIPT.json VO_DIR l01,l04 [tries]"""
import difflib, json, re, shutil, subprocess, sys, unicodedata
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import tts  # noqa: E402

WHISPER = "/home/user/models/whisper.cpp/build/bin/whisper-cli"
MODEL = "/home/user/models/ggml-small.bin"
import os
LANG = os.environ.get("WHISPER_LANG", "fr")


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = s.replace("belekt", "belegt").replace("belect", "belegt").replace("beleg ", "belegt ").replace("belig", "belegt").replace("beleckt", "belegt").replace("apertus", "apertus")
    return re.sub(r"[^a-z0-9 ]+", " ", s).split()


def transcribe(mp3):
    wav = mp3.with_suffix(".wav")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(mp3), "-ar", "16000", "-ac", "1", str(wav)], check=True)
    out = subprocess.run([WHISPER, "-m", MODEL, "-l", LANG, "-t", "2", "-nt", "-f", str(wav)], capture_output=True, text=True).stdout
    return " ".join(out.split())


script = json.loads(Path(sys.argv[1]).read_text())
vo = Path(sys.argv[2]); ids = sys.argv[3].split(","); tries = int(sys.argv[4]) if len(sys.argv) > 4 else 4
for line in script["lines"]:
    if line["id"] not in ids:
        continue
    text = line.get("text") or line["fr"]
    target = norm(text.replace("Bélèkt", "Belegt"))
    best = (-1, None)
    for k in range(tries):
        cand = vo / f"{line['id']}.try{k}.mp3"
        tts.tts(text, cand)
        heard = transcribe(cand)
        score = difflib.SequenceMatcher(None, target, norm(heard)).ratio()
        print(line["id"], k, round(score, 2), heard)
        if score > best[0]:
            best = (score, cand)
        if score >= 0.85:
            break
    shutil.copy(best[1], vo / f"{line['id']}.mp3")
    print("->", line["id"], "kept score", round(best[0], 2))
