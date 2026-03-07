"""Reproducibility metadata for experiment runs."""

import datetime
import json
import platform
import subprocess
import sys
from pathlib import Path


def capture() -> dict:
    """Capture current environment metadata for reproducibility."""
    meta = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "python_version": sys.version,
        "platform": platform.platform(),
        "hostname": platform.node(),
    }

    # Try to capture git commit
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            meta["git_commit"] = result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        meta["git_commit"] = "unknown"

    return meta


def save(metadata: dict, results: dict, experiment_id: str) -> Path:
    """Save experiment results with metadata to the results directory."""
    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)

    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")
    filename = f"{experiment_id}_{timestamp}.json"
    filepath = results_dir / filename

    output = {
        "experiment_id": experiment_id,
        "metadata": metadata,
        "results": results,
    }

    filepath.write_text(json.dumps(output, indent=2, default=str))
    return filepath
