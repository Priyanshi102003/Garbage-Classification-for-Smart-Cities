"""Load and persist SmartWaste JSON state."""
from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
USERS_FILE = APP_DIR / "smartwaste_users.json"
STATE_FILE = APP_DIR / "smartwaste_state.json"

DEFAULT_STATE = {
    "locations": [],
    "history": [],
    "bins": [],
    "routes": [],
    "alerts": [],
}


def load_json(path: Path, default):
    if path.is_file():
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return deepcopy(default)


def save_json(path: Path, data) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_users() -> dict:
    return load_json(USERS_FILE, {})


def load_state() -> dict:
    state = load_json(STATE_FILE, DEFAULT_STATE)
    for key in DEFAULT_STATE:
        state.setdefault(key, [])
    return state


def save_state(state: dict) -> None:
    save_json(STATE_FILE, state)
