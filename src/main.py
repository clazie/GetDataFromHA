import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

CONFIG_FILE = "config.json"
ENTITIES_FILE = "entitys.json"
OUTPUT_FILE = "data.json"


def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        sys.stderr.write(f"Datei nicht gefunden: {path}\n")
        sys.exit(1)
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"Fehler beim Lesen von {path}: {exc}\n")
        sys.exit(1)


def build_base_url(config):
    host = config.get("ha-api-ip")
    port = config.get("ha-api-port")
    if not host or not port:
        sys.stderr.write("config.json muss ha-api-ip und ha-api-port enthalten.\n")
        sys.exit(1)
    scheme = "http"
    return f"{scheme}://{host}:{port}"


def request_state(base_url, token, entity_id):
    endpoint = f"{base_url}/api/states/{urllib.parse.quote(entity_id, safe='')}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    req = urllib.request.Request(endpoint, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            if response.status != 200:
                raise urllib.error.HTTPError(
                    endpoint, response.status, response.reason, response.headers, None
                )
            data = response.read().decode("utf-8")
            return json.loads(data)
    except urllib.error.HTTPError as exc:
        sys.stderr.write(
            f"HTTP-Fehler für {entity_id}: {exc.code} {exc.reason}\n"
        )
    except urllib.error.URLError as exc:
        sys.stderr.write(f"Verbindungsfehler für {entity_id}: {exc.reason}\n")
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"Ungültige JSON-Antwort für {entity_id}: {exc}\n")
    return None


def main():
    config = load_json(CONFIG_FILE)
    entities_data = load_json(ENTITIES_FILE)
    devices = entities_data.get("device")
    if not isinstance(devices, list):
        sys.stderr.write("entitys.json muss ein Feld 'device' mit einer Liste enthalten.\n")
        sys.exit(1)

    token = config.get("ha-api-token")
    if not token:
        sys.stderr.write("config.json muss ha-api-token enthalten.\n")
        sys.exit(1)

    base_url = build_base_url(config)
    result = []

    for device in devices:
        entity_name = device.get("entity")
        entity_id = device.get("entity-id")
        if not entity_id:
            continue

        state_data = request_state(base_url, token, entity_id)
        if state_data is None:
            continue

        result.append(
            {
                "entity": entity_name if entity_name else entity_id,
                "state": state_data.get("state"),
            }
        )

    with open(OUTPUT_FILE, "w", encoding="utf-8") as output_file:
        json.dump(result, output_file, ensure_ascii=False, indent=2)

    print(f"Ergebnis in {OUTPUT_FILE} geschrieben ({len(result)} Einträge).")


if __name__ == "__main__":
    main()
