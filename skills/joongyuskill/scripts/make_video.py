"""Scenes HTML (<section class="scene" id="sN">) -> mp4. Usage: make_video.py scenes.html out.mp4 [--seconds 4]"""
import argparse, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

BROWSERS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "google-chrome", "chromium", "chromium-browser", "msedge",
]


def find_browser():
    for b in BROWSERS:
        if os.path.isfile(b) or shutil.which(b):
            return b
    sys.exit("Chrome/Edge가 없습니다. 하나를 설치하십시오.")


def scene_ids(html):
    return re.findall(r'<section[^>]*class="scene"[^>]*id="([^"]+)"', html) or \
           re.findall(r'<section[^>]*id="([^"]+)"[^>]*class="scene"', html)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("scenes")
    ap.add_argument("out")
    ap.add_argument("--seconds", type=float, default=4)
    a = ap.parse_args()

    try:
        import imageio_ffmpeg
    except ImportError:
        sys.exit("imageio-ffmpeg가 없습니다. 'pip install imageio-ffmpeg'를 실행하십시오.")

    src = Path(a.scenes).resolve()
    ids = scene_ids(src.read_text(encoding="utf-8"))
    assert ids, 'scene이 없습니다. <section class="scene" id="s1"> 형식을 쓰십시오.'
    browser = find_browser()

    with tempfile.TemporaryDirectory() as tmp:
        for i, sid in enumerate(ids):
            png = Path(tmp) / f"f{i:03d}.png"
            subprocess.run([browser, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                            f"--user-data-dir={tmp}/profile", "--window-size=1280,720",
                            f"--screenshot={png}", f"{src.as_uri()}#{sid}"],
                           check=True, capture_output=True, timeout=60)
            assert png.exists(), f"{sid} 캡처 실패"
        # tpad: the fps filter drops the last image, so clone it once first
        subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error",
                        "-framerate", f"1/{a.seconds}", "-i", f"{tmp}/f%03d.png",
                        "-vf", "tpad=stop_mode=clone:stop=1,scale=1280:720,fps=30",
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", a.out],
                       check=True)
    print(f"{a.out}: 장면 {len(ids)}개, {len(ids) * a.seconds:g}초")


if __name__ == "__main__":
    main()
