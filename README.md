# GetDataFromHA

Holt Daten vom Homeassistant über die API. Es wird ein API-Token benötigt.

## Virtuelle Umgebung
Erstellung der virtuellen Umgebung mit

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Erstellen der Configuration

Als Basis können die Dateien `config-example.json` nach `config.json` und `entities-example.json` nach `entities.json` kopiert werden. Die Einträge müssen entsprechend angepasst werden.

## Starten

Ausführen mit 

```bash
python src/main.py
```