# Entwicklung und Start nach frischem Checkout

## 1. Repository auschecken

```bash
git clone <repository-url>
cd GetDataFromHA
```

## 2. Virtuelle Python-Umgebung erstellen

```bash
python3 -m venv .venv
```

## 3. Virtuelle Umgebung aktivieren

```bash
source .venv/bin/activate
```

## 4. Abhängigkeiten installieren

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 5. Konfigurationsdateien prüfen

- `config.json` für Home Assistant, MQTT und InfluxDB
- `entitys.json` für die abgefragten Entitäten

> Falls noch keine `config.json` vorhanden ist, kann `config-example.json` als Vorlage genutzt werden.

## 6. Programm starten

```bash
python3 main.py
```

## 7. Ergebnis prüfen

- `data.json` wird im Projektverzeichnis erstellt
- MQTT-Ausgabe erfolgt, wenn `mqtt` in `config.json` konfiguriert ist
- InfluxDB v2-Ausgabe erfolgt, wenn `influx2` in `config.json` konfiguriert ist

## 8. Optional: Fehlerdiagnose

- Wenn `main.py` Syntaxfehler meldet:

```bash
python3 -m py_compile main.py src/main.py src/config.py src/homeassistant.py src/outputs/file_output.py src/outputs/mqtt_output.py src/outputs/influxdb_output.py
```

- Wenn Abhängigkeiten fehlen:

```bash
pip install -r requirements.txt
```
