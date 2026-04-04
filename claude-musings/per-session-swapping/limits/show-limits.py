#!/usr/bin/env python3
"""Fetch and display Claude + z.ai rate limits with colored bars."""

import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from configparser import ConfigParser
from datetime import datetime, timezone
from pathlib import Path


# ── ANSI colors ─────────────────────────────────────────
BLUE = "\033[38;2;0;153;255m"
ORANGE = "\033[38;2;255;176;85m"
GREEN = "\033[38;2;0;175;80m"
CYAN = "\033[38;2;86;182;194m"
RED = "\033[38;2;255;85;85m"
YELLOW = "\033[38;2;230;200;0m"
WHITE = "\033[38;2;220;220;220m"
DIM = "\033[2m"
RESET = "\033[0m"


def color_for_pct(pct: int) -> str:
    if pct >= 90:
        return RED
    elif pct >= 70:
        return YELLOW
    elif pct >= 50:
        return ORANGE
    return GREEN


def build_bar(pct: int, width: int = 10) -> str:
    pct = max(0, min(100, pct))
    filled = pct * width // 100
    empty = width - filled
    c = color_for_pct(pct)
    return f"{c}{'●' * filled}{DIM}{'○' * empty}{RESET}"


def visible_len(s: str) -> int:
    """Terminal display width, accounting for wide Unicode characters."""
    import unicodedata
    stripped = re.sub(r"\033\[[0-9;]*m", "", s)
    width = 0
    for c in stripped:
        eaw = unicodedata.east_asian_width(c)
        width += 2 if eaw in ("W", "F") else 1
    return width


def pad(s: str, width: int) -> str:
    return s + " " * max(0, width - visible_len(s))


def fmt_time(iso: str) -> str:
    try:
        dt = datetime.fromisoformat(iso).astimezone()
        return dt.strftime("%-I:%M%p").lower()
    except Exception:
        return "?"


def fmt_datetime(iso: str) -> str:
    try:
        dt = datetime.fromisoformat(iso).astimezone()
        return dt.strftime("%b %-d, %-I:%M%p").lower()
    except Exception:
        return "?"


def fmt_epoch_ms_time(ms: int) -> str:
    try:
        dt = datetime.fromtimestamp(ms / 1000, tz=timezone.utc).astimezone()
        return dt.strftime("%-I:%M%p").lower()
    except Exception:
        return "?"


def fmt_epoch_ms_datetime(ms: int) -> str:
    try:
        dt = datetime.fromtimestamp(ms / 1000, tz=timezone.utc).astimezone()
        return dt.strftime("%b %-d, %-I:%M%p").lower()
    except Exception:
        return "?"


# ── Token resolution ────────────────────────────────────
def get_claude_token() -> str | None:
    try:
        blob = subprocess.check_output(
            ["security", "find-generic-password", "-s", "Claude Code-credentials", "-w"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        data = json.loads(blob)
        token = data.get("claudeAiOauth", {}).get("accessToken")
        if token:
            return token
    except Exception:
        pass
    creds = Path.home() / ".claude" / ".credentials.json"
    if creds.exists():
        try:
            data = json.loads(creds.read_text())
            token = data.get("claudeAiOauth", {}).get("accessToken")
            if token:
                return token
        except Exception:
            pass
    return None


def get_zai_token() -> str | None:
    providers = Path.home() / ".ai-providers"
    if not providers.exists():
        return None
    cp = ConfigParser()
    cp.read(str(providers))
    return cp.get("zai", "ANTHROPIC_AUTH_TOKEN", fallback=None)


# ── Fetchers ────────────────────────────────────────────
def fetch_claude() -> dict | None:
    token = get_claude_token()
    if not token:
        return None
    try:
        r = subprocess.check_output(
            [
                "curl", "-s", "--max-time", "5",
                "-H", "Accept: application/json",
                "-H", f"Authorization: Bearer {token}",
                "-H", "anthropic-beta: oauth-2025-04-20",
                "https://api.anthropic.com/api/oauth/usage",
            ],
            stderr=subprocess.DEVNULL,
            text=True,
        )
        data = json.loads(r)
        if "five_hour" in data:
            return data
    except Exception:
        pass
    return None


def fetch_zai() -> dict | None:
    token = get_zai_token()
    if not token:
        return None
    try:
        r = subprocess.check_output(
            [
                "curl", "-s", "--max-time", "5",
                "-H", "Accept: application/json",
                "-H", f"Authorization: {token}",
                "-H", "Accept-Language: en-US,en",
                "https://api.z.ai/api/monitor/usage/quota/limit",
            ],
            stderr=subprocess.DEVNULL,
            text=True,
        )
        data = json.loads(r)
        if data.get("data", {}).get("limits"):
            return data
    except Exception:
        pass
    return None


def load_from_cache() -> tuple[dict | None, dict | None]:
    """Load data from statusline cache files."""
    claude_data = None
    zai_data = None
    claude_cache = Path("/tmp/claude/statusline-usage-cache.json")
    zai_cache = Path("/tmp/claude/statusline-zai-usage-cache.json")
    if claude_cache.exists():
        try:
            claude_data = json.loads(claude_cache.read_text())
            if "five_hour" not in claude_data:
                claude_data = None
        except Exception:
            pass
    if zai_cache.exists():
        try:
            zai_data = json.loads(zai_cache.read_text())
        except Exception:
            pass
    return claude_data, zai_data


def normalize_zai(raw: dict) -> dict | None:
    """Convert raw z.ai API response to normalized format, or pass through if already normalized."""
    if "data" in raw and "limits" in raw.get("data", {}):
        return raw  # Raw API format
    if "five_hour" in raw:
        return raw  # Already normalized by statusline cache
    return None


# ── Build row ───────────────────────────────────────────
def build_row(label: str, pct: int, reset_str: str) -> str:
    bar = build_bar(pct)
    pc = color_for_pct(pct)
    return f"{WHITE}{label}{RESET} {bar} {pc}{pct:3d}%{RESET} {DIM}⟳{RESET} {WHITE}{reset_str}{RESET}"


def zai_limit(data: dict, unit: int, number: int) -> dict | None:
    """Extract a limit from z.ai data, handling both raw and normalized formats."""
    if "data" in data:
        # Raw API format
        return next(
            (l for l in data["data"]["limits"]
             if l["type"] == "TOKENS_LIMIT" and l["unit"] == unit and l["number"] == number),
            None,
        )
    # Normalized format (from statusline cache)
    if unit == 3 and number == 5:
        return data.get("five_hour")
    if unit == 6 and number == 1:
        return data.get("seven_day")
    return None


def zai_pct_and_reset(lim: dict, fmt_fn) -> tuple[int, str]:
    """Get pct and formatted reset from a z.ai limit (raw or normalized)."""
    if "percentage" in lim:
        # Raw format
        return lim["percentage"], fmt_fn(lim["nextResetTime"])
    # Normalized format
    pct = int(round(lim.get("utilization", 0)))
    return pct, fmt_time(lim["resets_at"]) if fmt_fn == fmt_epoch_ms_time else fmt_datetime(lim["resets_at"])


# ── Display ─────────────────────────────────────────────
def display(claude_data: dict | None, zai_data: dict | None):
    COL_W = 40
    SEP = f"  {DIM}┊{RESET}  "

    # Header — "cur " is 4 chars + 1 space in build_row = 5 char indent
    left = pad(f"{WHITE}    {RESET} {BLUE}Claude{RESET}", COL_W)
    print(f"{left}{SEP}{CYAN}z.ai{RESET}")

    # Current (5h)
    if claude_data:
        pct = int(round(claude_data["five_hour"]["utilization"]))
        reset = fmt_time(claude_data["five_hour"]["resets_at"])
        left = pad(build_row("cur ", pct, reset), COL_W)
    else:
        left = pad(f"{DIM}cur  unavailable{RESET}", COL_W)

    if zai_data:
        lim = zai_limit(zai_data, 3, 5)
        if lim:
            if "percentage" in lim:
                right = build_row("cur ", lim["percentage"], fmt_epoch_ms_time(lim["nextResetTime"]))
            else:
                right = build_row("cur ", int(round(lim.get("utilization", 0))), fmt_time(lim["resets_at"]))
        else:
            right = f"{DIM}cur  n/a{RESET}"
    else:
        right = f"{DIM}cur  unavailable{RESET}"
    print(f"{left}{SEP}{right}")

    # Weekly
    if claude_data:
        pct = int(round(claude_data["seven_day"]["utilization"]))
        reset = fmt_datetime(claude_data["seven_day"]["resets_at"])
        left = pad(build_row("wk  ", pct, reset), COL_W)
    else:
        left = pad(f"{DIM}wk   unavailable{RESET}", COL_W)

    if zai_data:
        lim = zai_limit(zai_data, 6, 1)
        if lim:
            if "percentage" in lim:
                right = build_row("wk  ", lim["percentage"], fmt_epoch_ms_datetime(lim["nextResetTime"]))
            else:
                right = build_row("wk  ", int(round(lim.get("utilization", 0))), fmt_datetime(lim["resets_at"]))
        else:
            right = f"{DIM}wk   n/a{RESET}"
    else:
        right = f"{DIM}wk   unavailable{RESET}"
    print(f"{left}{SEP}{right}")

    # Extra row (Claude only)
    if claude_data:
        ex = claude_data.get("extra_usage", {})
        if ex.get("is_enabled"):
            used = ex.get("used_credits", 0) / 100
            limit = ex.get("monthly_limit", 0) / 100
            bar = build_bar(int(round(used / limit * 100)) if limit else 0)
            left = pad(f"{WHITE}ex  {RESET} {bar} {GREEN}${used:.2f}{DIM}/{RESET}{WHITE}${limit:.2f}{RESET}", COL_W)
            print(f"{left}{SEP}")


def main():
    from_cache = "--from-cache" in sys.argv

    if from_cache:
        claude_data, zai_data = load_from_cache()
    else:
        claude_data = None
        zai_data = None
        with ThreadPoolExecutor(max_workers=2) as pool:
            futures = {pool.submit(fetch_claude): "claude", pool.submit(fetch_zai): "zai"}
            for f in as_completed(futures):
                if futures[f] == "claude":
                    claude_data = f.result()
                else:
                    zai_data = f.result()

    if not claude_data and not zai_data:
        sys.exit(0)

    display(claude_data, zai_data)


if __name__ == "__main__":
    main()
