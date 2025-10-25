import subprocess
from pathlib import Path
from datetime import datetime, timezone

# --- CONFIG ---
URL = "https://www.youtube.com/watch?v=ydYDqZQpim8"
OUTPUT_DIR = "data"
FORMAT = "best[height<=720]"
# ----------------

def get_snapshot():
    """Download a single snapshot from the livestream."""
    now = datetime.now(timezone.utc)

    # Create directory structure: data/yyyy-mm-dd/
    date_str = now.strftime("%Y-%m-%d")
    # time_str = now.strftime("%H_%M_%S")
    time_str = now.strftime("%H_00_00")

    date_dir = Path(OUTPUT_DIR) / date_str
    date_dir.mkdir(parents=True, exist_ok=True)

    out = date_dir / f"{time_str}.png"

    print(f"📸 Capturing snapshot at {now.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"📁 Saving to: {out}")

    # Get the direct stream URL using yt-dlp
    print("🔍 Getting stream URL...")
    cmd = [
        "yt-dlp",
        "-f", FORMAT,
        "--get-url",
        URL,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Failed to get URL: {result.stderr}")
        return

    stream_url = result.stdout.strip()
    if not stream_url:
        print("❌ No stream URL found")
        return

    print("📸 Capturing frame from stream...")
    # Use ffmpeg to grab a single frame directly from the stream
    ffmpeg_cmd = [
        "ffmpeg",
        "-i", stream_url,
        "-frames:v", "1",
        "-q:v", "2",
        "-y",
        str(out),
    ]

    result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, timeout=30)
    if result.returncode != 0:
        print(f"❌ Failed to capture frame: {result.stderr}")
    else:
        print(f"✅ Snapshot saved to {out}")

if __name__ == "__main__":
    get_snapshot()
