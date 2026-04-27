#!/usr/bin/env bash
# find-influencer skill - dependency check
# Run: bash setup_check.sh

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

pass=0
warn=0
fail=0

check_cmd() {
    local name="$1" install_hint="$2"
    if command -v "$name" &>/dev/null; then
        echo -e "  ${GREEN}[OK]${NC} $name ($(command -v "$name"))"
        pass=$((pass + 1))
    else
        echo -e "  ${RED}[MISSING]${NC} $name"
        echo -e "       Install: $install_hint"
        fail=$((fail + 1))
    fi
}

check_python_pkg() {
    local pkg="$1" import_name="$2" install_hint="$3"
    if python3 -c "import $import_name" 2>/dev/null; then
        echo -e "  ${GREEN}[OK]${NC} $pkg"
        pass=$((pass + 1))
    else
        echo -e "  ${RED}[MISSING]${NC} $pkg"
        echo -e "       Install: $install_hint"
        fail=$((fail + 1))
    fi
}

check_optional() {
    local name="$1" desc="$2" install_hint="$3"
    if command -v "$name" &>/dev/null; then
        echo -e "  ${GREEN}[OK]${NC} $name ($(command -v "$name"))"
        pass=$((pass + 1))
    else
        echo -e "  ${YELLOW}[OPTIONAL]${NC} $name - $desc"
        echo -e "       Install: $install_hint"
        warn=$((warn + 1))
    fi
}

echo "======================================"
echo " find-influencer Skill Setup Check"
echo "======================================"
echo ""

# --- Python ---
echo "Python:"
check_cmd "python3" "https://www.python.org/downloads/ or brew install python"
if command -v python3 &>/dev/null; then
    ver=$(python3 --version 2>&1)
    echo -e "       Version: $ver"
fi
echo ""

# --- Required tools ---
echo "Required tools:"
check_cmd "ffmpeg" "brew install ffmpeg (macOS) / apt install ffmpeg (Linux) / choco install ffmpeg (Windows)"
check_cmd "curl" "Usually pre-installed. brew install curl / apt install curl"
echo ""

# --- Python packages ---
echo "Python packages:"
if command -v python3 &>/dev/null; then
    check_python_pkg "openai-whisper" "whisper" "pip install openai-whisper"
else
    echo -e "  ${RED}[SKIP]${NC} Cannot check Python packages - python3 not found"
    ((fail++))
fi
echo ""

# --- Optional tools ---
echo "Optional tools:"
check_optional "opencli" "Primary search tool for Xiaohongshu/Bilibili/YouTube" "See https://github.com/nicepkg/opencli or pip install opencli"
echo ""

# --- Claude Code / Playwright MCP ---
echo "Claude Code environment:"
if [ -n "${CLAUDE_SKILL_DIR:-}" ]; then
    echo -e "  ${GREEN}[OK]${NC} Running inside Claude Code skill context"
else
    echo -e "  ${YELLOW}[INFO]${NC} Not running inside Claude Code (CLAUDE_SKILL_DIR not set)"
fi
echo -e "  ${YELLOW}[NOTE]${NC} Playwright MCP server must be configured in Claude Code"
echo -e "       This is used for browser automation (Douyin, fallback for other platforms)"
echo ""

# --- Summary ---
echo "======================================"
echo " Summary: ${GREEN}$pass passed${NC}, ${YELLOW}$warn optional${NC}, ${RED}$fail missing${NC}"
echo "======================================"
if [ "$fail" -gt 0 ]; then
    echo ""
    echo -e "${RED}Please install missing dependencies before using this skill.${NC}"
    exit 1
else
    echo ""
    echo -e "${GREEN}All required dependencies are installed!${NC}"
    exit 0
fi
