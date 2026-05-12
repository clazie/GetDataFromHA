import json
from pathlib import Path
from typing import Any, Dict, Tuple

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def load_json_file(path: Path) -> Dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Datei nicht gefunden: {path}")
    except json.JSONDecodeError as exc:
        raise ValueError(f"Ungültiges JSON in {path}: {exc}")


def load_config(
    config_path: str = "config.json", entities_path: str = "entitys.json"
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    config = load_json_file(PROJECT_ROOT / config_path)
    entities = load_json_file(PROJECT_ROOT / entities_path)
    return config, entities
