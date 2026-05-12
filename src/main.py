from pathlib import Path
import sys

from .config import PROJECT_ROOT, load_config
from .homeassistant import HomeAssistantError, collect_entity_states
from .outputs import publish_mqtt_states, send_influx_points, write_json_file

OUTPUT_FILE = PROJECT_ROOT / "data.json"


def main() -> None:
    try:
        config, entities = load_config()
        entries = collect_entity_states(config, entities)
    except (FileNotFoundError, ValueError, HomeAssistantError) as exc:
        sys.stderr.write(f"{exc}\n")
        sys.exit(1)

    if not entries:
        print("Keine Einträge gefunden oder keine Zustände abgerufen.")
        return

    write_json_file(entries, OUTPUT_FILE)
    print(f"Ergebnis in {OUTPUT_FILE} geschrieben ({len(entries)} Einträge).")

    try:
        publish_mqtt_states(config, entries)
    except Exception as exc:
        print(f"MQTT-Ausgabe fehlgeschlagen: {exc}")

    try:
        send_influx_points(config, entries)
    except Exception as exc:
        print(f"InfluxDB-Ausgabe fehlgeschlagen: {exc}")


if __name__ == "__main__":
    main()
