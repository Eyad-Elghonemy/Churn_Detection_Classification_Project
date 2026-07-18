"""
Very small file-based usage tracker.

Every successful prediction call appends a timestamp under its model name to
usage_log.json (stored at the project root). This is intentionally simple:
no database, just a JSON file guarded by a lock so concurrent requests don't
corrupt it. Good enough for a portfolio project's "who's using this" chart.

Note: on Hugging Face Spaces (free tier) this file persists while the Space
is running or asleep, but resets whenever the Space is rebuilt (new push).
"""

import json
import os
import threading
from datetime import datetime, timezone

_LOCK = threading.Lock()
_LOG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "usage_log.json"
)
_MAX_TIMESTAMPS_PER_MODEL = 1000

_DEFAULT = {
    "forest": {"count": 0, "timestamps": []},
    "xgboost": {"count": 0, "timestamps": []},
}


def _load() -> dict:
    if not os.path.exists(_LOG_PATH):
        return {k: {"count": 0, "timestamps": []} for k in _DEFAULT}
    try:
        with open(_LOG_PATH, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        data = {}
    for k in _DEFAULT:
        data.setdefault(k, {"count": 0, "timestamps": []})
    return data


def _save(data: dict) -> None:
    with open(_LOG_PATH, "w") as f:
        json.dump(data, f)


def log_usage(model_name: str) -> None:
    """Record one successful prediction call for the given model."""
    with _LOCK:
        data = _load()
        if model_name not in data:
            data[model_name] = {"count": 0, "timestamps": []}
        data[model_name]["count"] += 1
        data[model_name]["timestamps"].append(datetime.now(timezone.utc).isoformat())
        data[model_name]["timestamps"] = data[model_name]["timestamps"][-_MAX_TIMESTAMPS_PER_MODEL:]
        _save(data)


def get_stats() -> dict:
    """Return the current usage counts and timestamps for every model."""
    with _LOCK:
        return _load()
