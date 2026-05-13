import requests
from typing import Any, Dict, List


class HomeAssistantError(Exception):
    pass


def build_base_url(ha_config: Dict[str, Any]) -> str:
    host = ha_config.get("ha-api-ip")
    port = ha_config.get("ha-api-port")
    if not host or not port:
        raise HomeAssistantError(
            "config.json muss im Abschnitt 'homeassistant' ha-api-ip und ha-api-port enthalten."
        )
    scheme = ha_config.get("ha-api-scheme", "http")
    return f"{scheme}://{host}:{port}"


def request_state(base_url: str, token: str, entity_id: str) -> Dict[str, Any]:
    url = f"{base_url}/api/states/{entity_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
    return response.json()


def collect_entity_states(config: Dict[str, Any], entities: Dict[str, Any]) -> List[Dict[str, Any]]:
    ha_config = config.get("homeassistant")
    if not isinstance(ha_config, dict):
        raise HomeAssistantError("config.json muss einen Abschnitt 'homeassistant' enthalten.")

    devices = entities.get("entities")
    if not isinstance(devices, list):
        raise HomeAssistantError("entities.json muss ein Feld 'entities' mit einer Liste enthalten.")

    token = ha_config.get("ha-api-token")
    if not token:
        raise HomeAssistantError("config.json muss im Abschnitt 'homeassistant' den Schlüssel 'ha-api-token' enthalten.")

    aera = entities.get("aera")
    base_url = build_base_url(ha_config)
    result: List[Dict[str, Any]] = []

    for device in devices:
        entity_name = device.get("entity")
        entity_id = device.get("entity-id")
        field_name = device.get("field")
        if not entity_id:
            continue

        state_data = request_state(base_url, token, entity_id)
        result.append(
            {
                "entity": entity_name or entity_id,
                "entity_id": entity_id,
                "state": state_data.get("state"),
                "field": field_name,
                "aera": aera,
            }
        )

    return result
