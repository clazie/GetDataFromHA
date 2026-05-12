import json
import ssl
import time
from typing import Any, Dict, List

import paho.mqtt.client as mqtt


def build_publish_topic(topic_template: str, entity_id: str) -> str:
    if "#" in topic_template:
        return topic_template.replace("#", entity_id)
    if topic_template.endswith("/"):
        return f"{topic_template}{entity_id}"
    return topic_template


def publish_mqtt_states(config: Dict[str, Any], entries: List[Dict[str, Any]]) -> None:
    mqtt_config = config.get("mqtt")
    if not isinstance(mqtt_config, dict):
        return

    host = mqtt_config.get("mqtt-ip")
    port = mqtt_config.get("mqtt-port", 1883)
    username = mqtt_config.get("mqtt-username")
    password = mqtt_config.get("mqtt-password")
    topic_template = mqtt_config.get("mqtt-topic")
    qos = int(mqtt_config.get("mqtt-qos", 0))
    retain = bool(mqtt_config.get("mqtt-retain", False))
    client_id = mqtt_config.get("mqtt-client-id")
    clean_session = bool(mqtt_config.get("mqtt-clean-session", True))
    keepalive = int(mqtt_config.get("mqtt-keep-alive", 60))
    ssl_enabled = bool(mqtt_config.get("mqtt-ssl", False))
    ssl_insecure = bool(mqtt_config.get("mqtt-ssl-insecure", False))

    if not host or not topic_template:
        print("MQTT-Konfiguration unvollständig, MQTT-Ausgabe wird übersprungen.")
        return

    client = mqtt.Client(client_id=str(client_id) if client_id else None, clean_session=clean_session)
    if username:
        client.username_pw_set(username, password or "")

    if ssl_enabled:
        ca_cert = mqtt_config.get("mqtt-ssl-ca-cert") or None
        certfile = mqtt_config.get("mqtt-ssl-certfile") or None
        keyfile = mqtt_config.get("mqtt-ssl-keyfile") or None
        client.tls_set(ca_certs=ca_cert, certfile=certfile, keyfile=keyfile, tls_version=ssl.PROTOCOL_TLS)
        client.tls_insecure_set(ssl_insecure)

    client.connect(host, port, keepalive)
    client.loop_start()

    try:
        for entry in entries:
            topic = build_publish_topic(topic_template, entry["entity_id"])
            payload = json.dumps({"entity": entry["entity"], "state": entry["state"]}, ensure_ascii=False)
            message = client.publish(topic, payload, qos=qos, retain=retain)
            message.wait_for_publish()
            time.sleep(0.01)
    finally:
        client.loop_stop()
        client.disconnect()
