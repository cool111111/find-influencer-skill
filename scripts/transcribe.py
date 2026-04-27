#!/usr/bin/env python3
"""Video speech-to-text transcription using OpenAI Whisper.

Usage:
    python3 transcribe.py <video_url_or_path> [--model base] [--language zh] [--output json|text|srt]

Examples:
    python3 transcribe.py https://example.com/video.mp4
    python3 transcribe.py /path/to/local/video.mp4 --language en
    python3 transcribe.py video.mp4 --output srt --model small
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def check_dependencies():
    """Check if ffmpeg and whisper are installed."""
    missing = []
    if not shutil.which("ffmpeg"):
        missing.append("ffmpeg (install: brew install ffmpeg)")
    try:
        import whisper  # noqa: F401
    except ImportError:
        missing.append("openai-whisper (install: pip install openai-whisper)")
    if missing:
        print("Missing dependencies:", file=sys.stderr)
        for m in missing:
            print(f"  - {m}", file=sys.stderr)
        sys.exit(1)


def download_video(url: str, output_path: str) -> str:
    """Download video from URL using curl."""
    print(f"Downloading video from {url}...", file=sys.stderr)
    result = subprocess.run(
        ["curl", "-L", "-o", output_path, "-s", "--max-time", "120", url],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"Download failed: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
        print("Downloaded file is empty or missing", file=sys.stderr)
        sys.exit(1)
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"Downloaded: {size_mb:.1f} MB", file=sys.stderr)
    return output_path


def extract_audio(video_path: str, audio_path: str) -> str:
    """Extract audio from video using ffmpeg."""
    print("Extracting audio...", file=sys.stderr)
    result = subprocess.run(
        [
            "ffmpeg", "-i", video_path,
            "-vn", "-acodec", "pcm_s16le",
            "-ar", "16000", "-ac", "1",
            "-y", audio_path,
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"Audio extraction failed: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return audio_path


def transcribe(audio_path: str, model_name: str = "base", language: str | None = None) -> dict:
    """Run whisper transcription."""
    import whisper

    print(f"Loading whisper model '{model_name}'...", file=sys.stderr)
    model = whisper.load_model(model_name)

    print("Transcribing...", file=sys.stderr)
    options = {}
    if language:
        options["language"] = language

    result = model.transcribe(audio_path, **options)
    return result


def format_timestamp(seconds: float) -> str:
    """Convert seconds to HH:MM:SS,mmm format."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def output_json(result: dict):
    """Output transcription as JSON."""
    segments = []
    for seg in result.get("segments", []):
        segments.append({
            "start": round(seg["start"], 2),
            "end": round(seg["end"], 2),
            "text": seg["text"].strip(),
        })
    output = {
        "language": result.get("language", "unknown"),
        "text": result.get("text", "").strip(),
        "segments": segments,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def output_text(result: dict):
    """Output transcription as plain text with timestamps."""
    for seg in result.get("segments", []):
        start = format_timestamp(seg["start"])
        text = seg["text"].strip()
        if text:
            print(f"[{start}] {text}")


def output_srt(result: dict):
    """Output transcription as SRT subtitle format."""
    for i, seg in enumerate(result.get("segments", []), 1):
        start = format_timestamp(seg["start"])
        end = format_timestamp(seg["end"])
        text = seg["text"].strip()
        if text:
            print(f"{i}")
            print(f"{start} --> {end}")
            print(text)
            print()


def main():
    parser = argparse.ArgumentParser(description="Transcribe video speech to text using Whisper")
    parser.add_argument("source", help="Video URL or local file path")
    parser.add_argument("--model", default="base", choices=["tiny", "base", "small", "medium", "large"],
                        help="Whisper model size (default: base)")
    parser.add_argument("--language", default=None, help="Language code, e.g., zh, en, ja (auto-detect if omitted)")
    parser.add_argument("--output", default="json", choices=["json", "text", "srt"],
                        help="Output format (default: json)")
    args = parser.parse_args()

    check_dependencies()

    tmpdir = tempfile.mkdtemp(prefix="transcribe_")
    try:
        # Determine if source is URL or local file
        source = args.source
        if source.startswith("http://") or source.startswith("https://"):
            video_path = os.path.join(tmpdir, "video.mp4")
            download_video(source, video_path)
        else:
            video_path = os.path.abspath(source)
            if not os.path.exists(video_path):
                print(f"File not found: {video_path}", file=sys.stderr)
                sys.exit(1)

        # Extract audio
        audio_path = os.path.join(tmpdir, "audio.wav")
        extract_audio(video_path, audio_path)

        # Transcribe
        result = transcribe(audio_path, model_name=args.model, language=args.language)

        # Output
        formatters = {"json": output_json, "text": output_text, "srt": output_srt}
        formatters[args.output](result)

    finally:
        # Cleanup
        shutil.rmtree(tmpdir, ignore_errors=True)


if __name__ == "__main__":
    main()
