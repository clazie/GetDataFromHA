import json
from pathlib import Path
from typing import Any, Dict, List


def write_json_file(entries: List[Dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as output_file:
        json.dump(entries, output_file, ensure_ascii=False, indent=2)
