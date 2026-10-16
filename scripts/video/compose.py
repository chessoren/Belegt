"""Assemble the demo video from the real recorded frames, cards and Oren's voice.

    python scripts/video/compose.py FRAMES_DIR VO_DIR CARDS_DIR OUT.mp4

Rules: app footage is never altered; waiting time of the local model is
time-lapsed with a visible "accéléré ×N" badge (measured latency is reported separately).
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FR, VO, CARDS, OUT = map(Path, sys.argv[1:5])
TMP = OUT.parent / "_build"
TMP.mkdir(parents=True, exist_ok=True)
W, H, FPS = 1920, 1080, 30
FONT = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
SCRIPT = json.loads((ROOT / "docs" / "video" / "script.json").read_text())
LINES = {l["id"]: l for l in SCRIPT["lines"]}


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(" ".join(map(str, cmd))[:600]); print(r.stderr[-2000:]); raise SystemExit(1)
    return r.stdout


def dur(p):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]).strip())


def scene(name):
    d = json.loads((FR / name / "frames.json").read_text())
    marks = {}
    for m in d["marks"]:
        marks.setdefault(m["label"], m["t"])
    return d["frames"], marks


def frames_between(name, a, b):
    frames, marks = scene(name)
    ta = marks[a] if isinstance(a, str) else a
    tb = marks[b] if isinstance(b, str) else b
    # wall-clock marks vs screencast timestamps: both are epoch seconds
    sel = [f for f in frames if ta <= f["t"] <= tb]
    before = [f for f in frames if f["t"] < ta]
    if before:
        sel = [{**before[-1], "t": ta}] + sel
    return sel, ta, tb


# ---------------------------------------------------------------- segments
# Each segment: VO lines, then visual parts. part = ("card", png) | ("scene", name, from, to, mode)
SEGMENTS = [
    (["l01", "l02"], [("card", "problem.png")]),
    (["l03"], [("scene", "a_landing", "start", "scroll", "fit")]),
    (["l04"], [("scene", "b_fr", "type", "submit", "1x"), ("scene", "b_fr", "submit", "result", "fit"), ("hold", "b_fr", "result", 1.2)]),
    (["l05"], [("scene", "b_fr", "result", "end", "fit")]),
    (["l06"], [("scene", "c_rm", "type", "submit", "1x"), ("scene", "c_rm", "submit", "result", "fit"), ("scene", "c_rm", "result", "end", "1x")]),
    (["l07"], [("card", "terminal.png", 3.5), ("scene", "d_net", "open-net", "type", "1x"), ("scene", "d_net", "submit", "result", "fit"), ("hold", "d_net", "result", 1.5)]),
    (["l08"], [("scene", "e_trap", "type", "submit", "1x"), ("scene", "e_trap", "submit", "result", "fit"), ("scene", "e_trap", "result", "receipt", "1x")]),
    (["l09"], [("scene", "e_trap", "receipt", "end", "fit")]),
    (["l10"], [("scene", "f_numbers", "start", "end", "fit")]),
    (["l11"], [("card", "end.png")]),
]
GAP = 0.7  # silence after each segment's voice


def render_frames(frames, t_from, t_to, factor, out, badge=None):
    lst = TMP / (out.stem + ".txt")
    lines = []
    for i, f in enumerate(frames):
        t_next = frames[i + 1]["t"] if i + 1 < len(frames) else t_to
        d = max(0.0, (t_next - f["t"]) * factor)
        lines.append(f"file '{(FR / out.stem.split('__')[0] / f['file']).resolve()}'\nduration {d:.4f}")
    lines.append(f"file '{(FR / out.stem.split('__')[0] / frames[-1]['file']).resolve()}'")
    lst.write_text("\n".join(lines) + "\n")
    vf = f"scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:white,fps={FPS},format=yuv420p"
    if badge:
        vf += (f",drawbox=x=w-330:y=36:w=290:h=64:color=0x1c0204@0.86:t=fill,"
               f"drawtext=fontfile={FONT}:text='{badge}':x=w-305:y=56:fontsize=27:fontcolor=white")
    total = (t_to - t_from) * factor
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-vf", vf,
         "-t", f"{total:.3f}", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-an", str(out)])


def render_still(png, seconds, out, zoom=True):
    vf = f"scale={W}:{H},format=yuv420p"
    if zoom:
        n = int(seconds * FPS)
        vf = (f"scale={W*2}:{H*2},zoompan=z='1+0.035*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps={FPS},format=yuv420p")
    run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", str(png), "-vf", vf, "-t", f"{seconds:.3f}",
         "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-an", str(out)])


def main():
    clips, events, t = [], [], 0.0
    for si, (line_ids, parts) in enumerate(SEGMENTS):
        vo = sum(dur(VO / f"{l}.mp3") for l in line_ids) + 0.25 * (len(line_ids) - 1)
        target = vo + 0.35 + GAP
        fixed, fit = 0.0, []
        prepared = []
        for p in parts:
            if p[0] == "card":
                d = p[2] if len(p) > 2 else None
                prepared.append(["card", p[1], d]); fixed += d or 0
                if d is None:
                    fit.append(len(prepared) - 1)
            elif p[0] == "hold":
                frames, marks = scene(p[1])
                prepared.append(["hold", p[1], marks[p[2]], p[3]]); fixed += p[3]
            else:
                fr, ta, tb = frames_between(p[1], p[2], p[3])
                prepared.append(["scene", p[1], fr, ta, tb, p[4]])
                if p[4] == "1x":
                    fixed += tb - ta
                else:
                    fit.append(len(prepared) - 1)
        remaining = max(target - fixed, 1.8 * max(1, len(fit)))
        seg_len = fixed + (remaining if fit else 0)
        if not fit:
            seg_len = max(seg_len, target)
        # fit parts share the remaining time proportionally to their real length (cards get equal weight)
        weights = []
        for i in fit:
            q = prepared[i]
            weights.append((q[4] - q[3]) if q[0] == "scene" else 1.0)
        wsum = sum(weights) or 1
        for k, i in enumerate(fit):
            prepared[i].append(remaining * weights[k] / wsum)
        for pi, q in enumerate(prepared):
            out = TMP / f"{q[1].replace('.png', '') if q[0] == 'card' else q[1]}__{si:02d}_{pi}.mp4"
            if q[0] == "card":
                secs = q[2] if q[2] is not None else q[3]
                render_still(CARDS / q[1], secs, out)
            elif q[0] == "hold":
                frames, _ = scene(q[1])
                last = [f for f in frames if f["t"] <= q[2] + 0.4][-1]
                render_still(FR / q[1] / last["file"], q[3], out, zoom=False)
            else:
                _, name, fr, ta, tb, mode = q[:6]
                if mode == "1x":
                    factor = 1.0
                else:
                    factor = q[6] / max(0.01, tb - ta)
                badge = None
                if factor < 0.6:
                    badge = f"accéléré ×{round(1 / factor)}"
                render_frames(fr, ta, tb, factor, out, badge)
            clips.append(out)
        events.append({"start": t + 0.35, "lines": line_ids})
        t += sum(dur(c) for c in clips[len(clips) - len(prepared):])
    total = t

    # concat video
    cl = TMP / "clips.txt"
    cl.write_text("".join(f"file '{c.resolve()}'\n" for c in clips))
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(cl), "-c", "copy", str(TMP / "video.mp4")])

    # audio: place each line
    inputs, filters, k = [], [], 0
    for ev in events:
        st = ev["start"]
        for lid in ev["lines"]:
            inputs += ["-i", str(VO / f"{lid}.mp3")]
            filters.append(f"[{k}:a]aresample=48000,adelay={int(st * 1000)}|{int(st * 1000)}[a{k}]")
            ev.setdefault("timing", []).append((lid, st, st + dur(VO / f"{lid}.mp3")))
            st += dur(VO / f"{lid}.mp3") + 0.25
            k += 1
    mix = "".join(f"[a{i}]" for i in range(k)) + f"amix=inputs={k}:normalize=0,apad,atrim=0:{total:.3f},loudnorm=I=-16:TP=-1.5[aout]"
    run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(filters) + ";" + mix,
         "-map", "[aout]", "-c:a", "aac", "-b:a", "192k", str(TMP / "audio.m4a")])

    # subtitles (FR + EN), burned in, and an .srt next to the video
    def ts(x):
        h, m, s = int(x // 3600), int(x % 3600 // 60), x % 60
        return f"{h}:{m:02d}:{s:05.2f}"

    def srt_ts(x):
        return f"{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{int(x % 60):02d},{int(x * 1000 % 1000):03d}"

    ass = ["[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}", "WrapStyle: 0", "",
           "[V4+ Styles]",
           "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
           "Style: Sub,Inter,38,&H00FFFFFF,&H00FFFFFF,&HD01C0204,&H401C0204,0,0,0,0,100,100,0,0,3,14,0,2,220,220,46,1",
           "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    srt, n = [], 1
    for ev in events:
        for lid, a, b in ev["timing"]:
            L = LINES[lid]
            txt = L["sub_fr"] + r"\N{\fs31\c&HC8D8FF&\i1}" + L["sub_en"]
            ass.append(f"Dialogue: 0,{ts(a)},{ts(b + 0.2)},Sub,,0,0,0,,{txt}")
            srt.append(f"{n}\n{srt_ts(a)} --> {srt_ts(b + 0.2)}\n{L['sub_fr']}\n{L['sub_en']}\n"); n += 1
    (TMP / "subs.ass").write_text("\n".join(ass) + "\n")
    OUT.with_suffix(".srt").write_text("\n".join(srt))

    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(TMP / "video.mp4"), "-i", str(TMP / "audio.m4a"),
         "-vf", f"ass={TMP / 'subs.ass'}", "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-pix_fmt", "yuv420p",
         "-c:a", "copy", "-movflags", "+faststart", "-shortest", str(OUT)])
    print("video", OUT, round(dur(OUT), 1), "s")
    (OUT.parent / "timeline.json").write_text(json.dumps(events, indent=1))


if __name__ == "__main__":
    main()
