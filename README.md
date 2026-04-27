# find-influencer Skill

Multi-platform creator discovery and analysis tool for Claude Code. Finds high-potential content creators on Xiaohongshu, Douyin, Bilibili, YouTube, etc.

## Quick Start

```bash
# 1. Check dependencies
bash scripts/setup_check.sh

# 2. Install any missing items (see below)

# 3. Use in Claude Code
#    Type: /find-influencer or describe your need (e.g., "帮我找小红书上的AI博主")
```

## Dependencies

### Required

| Dependency | Purpose | Install |
|-----------|---------|---------|
| **Python 3** | Run transcription script | `brew install python` (macOS) / `apt install python3` (Linux) / [python.org](https://www.python.org/downloads/) |
| **ffmpeg** | Extract audio from video | `brew install ffmpeg` (macOS) / `apt install ffmpeg` (Linux) / `choco install ffmpeg` (Windows) |
| **openai-whisper** | Speech-to-text transcription | `pip install openai-whisper` |

### Optional

| Dependency | Purpose | Install | Fallback |
|-----------|---------|---------|----------|
| **opencli** | Search Xiaohongshu, Bilibili, YouTube via CLI | `pip install opencli` or see [opencli repo](https://github.com/nicepkg/opencli) | Playwright browser automation |

### Claude Code Environment

| Requirement | Purpose | Setup |
|------------|---------|-------|
| **Claude Code** | Skill runtime | [claude.ai/code](https://claude.ai/code) |
| **Playwright MCP Server** | Browser automation for Douyin, profile visits, content analysis | Configure in Claude Code settings |

## Install All at Once

macOS:
```bash
brew install python ffmpeg
pip install openai-whisper
```

Linux (Debian/Ubuntu):
```bash
sudo apt install python3 python3-pip ffmpeg
pip install openai-whisper
```

## Notes

- **Whisper model download**: First run will download the `base` model (~140MB). Larger models (`small`, `medium`, `large`) give better accuracy but are slower and larger.
- **Platform login**: Xiaohongshu, Bilibili, etc. require you to be logged in via Chrome for opencli or Playwright to access data. Log in manually in Chrome before using this skill.
- **Transcription is optional**: If a post already contains a text transcript, the video transcription step is skipped automatically.
