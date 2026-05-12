import time
from typing import Any, Dict, List

import requests


def escape_tag_value(value: str) -> str:
    return (
        str(value)
        .replace("\\", "\\\\")
        .replace(" ", "\\ ")
        .replace(",", "\\,")
        .replace("=", "\\=")
    )


def escape_string_field(value: str) -> str:
    return '"' + str(value).replace("\\", "\\\\").replace('"', '\\"') + '"'


def format_field_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"

    if value is None:
        return escape_string_field("")

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        # Treat all numeric values as floats to avoid type conflicts
        return str(float(value))

    text = str(value)
    try:
        # Try to parse as float first for consistency
        float_value = float(text)
        return str(float_value)
    except ValueError:
        return escape_string_field(text)


def determine_field_name(value: Any, base_field: str) -> str:
    """Determine the field name based on the value type to avoid type conflicts."""
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return f"{base_field}_float"
    elif isinstance(value, str):
        try:
            float(value)
            return f"{base_field}_float"
        except ValueError:
            return f"{base_field}_string"
    else:
        return f"{base_field}_string"


def build_line_protocol(
    measurement: str,
    tag_key: str,
    tag_value: str,
    field_key: str,
    field_value: Any,
) -> str:
    tag_value_escaped = escape_tag_value(tag_value)
    field_text = format_field_value(field_value)
    measurement_escaped = escape_tag_value(measurement)
    return f"{measurement_escaped},{tag_key}={tag_value_escaped} {field_key}={field_text}"


def send_influx_points(config: Dict[str, Any], entries: List[Dict[str, Any]]) -> None:
    influx_config = config.get("influx2")
    if not isinstance(influx_config, dict):
        return

    url = influx_config.get("influx2-url")
    token = influx_config.get("influx2-token")
    org = influx_config.get("influx2-org")
    bucket = influx_config.get("influx2-bucket")
    measurement = influx_config.get("influx2-measurement", "homeassistant")
    tag_name = influx_config.get("influx2-tag", "entity")
    field_name = influx_config.get("influx2-field", "value")
    max_retries = int(influx_config.get("influx2-max-retries", 3))
    retry_interval = int(influx_config.get("influx2-retry-interval", 5))

    if not (url and token and org and bucket):
        print("InfluxDB v2-Konfiguration unvollständig, Influx-Ausgabe wird übersprungen.")
        return

    lines = []
    for entry in entries:
        field_name_dynamic = determine_field_name(entry["state"], field_name)
        lines.append(
            build_line_protocol(
                measurement=measurement,
                tag_key=tag_name,
                tag_value=entry["entity"],
                field_key=field_name_dynamic,
                field_value=entry["state"],
            )
        )

    if not lines:
        return

    endpoint = f"{url.rstrip('/')}/api/v2/write"
    params = {"org": org, "bucket": bucket, "precision": "ns"}
    headers = {"Authorization": f"Token {token}", "Content-Type": "text/plain; charset=utf-8"}
    payload = "\n".join(lines)

    for attempt in range(1, max_retries + 1):
        response = requests.post(endpoint, params=params, headers=headers, data=payload, timeout=15)
        if response.ok:
            return

        print(
            f"InfluxDB-V2-Write fehlgeschlagen ({response.status_code}): {response.text}. Versuch {attempt} von {max_retries}."
        )
        if attempt < max_retries:
            time.sleep(retry_interval)
