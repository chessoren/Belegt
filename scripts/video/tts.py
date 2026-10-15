"""Voice-over with Fish Audio (model s2.1-pro-free).

    FISH_API_KEY=... FISH_VOICE_ID=... python scripts/video/tts.py docs/video/script.json OUT_DIR

The key is read from the environment and never written to disk.
"""
import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

KEY = os.environ["FISH_API_KEY"]
VOICE = os.environ.get("FISH_VOICE_ID", "0cf175dc256e4b938efe9e6612933823")
MODEL = os.environ.get("FISH_MODEL", "s2.1-pro-free")


def tts(text: str, out: Path):
    body = json.dumps({"text": text, "reference_id": VOICE, "format": "mp3", "mp3_bitrate": 192,
                       "normalize": True, "latency": "normal"}).encode()
    req = urllib.request.Request("https://api.fish.audio/v1/tts", data=body, headers={
        "Authorization": f"Bearer {KEY}", "Content-Type": "application/json", "model": MODEL})
    with urllib.request.urlopen(req, timeout=180) as r:
        out.write_bytes(r.read())


def duration(p: Path) -> float:
    o = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                       capture_output=True, text=True)
    return float(o.stdout.strip())


def main():
    script = json.loads(Path(sys.argv[1]).read_text())
    out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    only = set(sys.argv[3].split(",")) if len(sys.argv) > 3 else None
    for line in script["lines"]:
        if only and line["id"] not in only:
            continue
        mp3 = out / f"{line['id']}.mp3"
        tts(line["fr"], mp3)
        line["duration"] = round(duration(mp3), 2)
        print(line["id"], line["duration"], "s")
    (out / "durations.json").write_text(json.dumps({l["id"]: l.get("duration") for l in script["lines"]}, indent=1))


if __name__ == "__main__":
    main()
