# Copilot prompt:

```text
Ich brauche ein Python Programm, was bestimmte Entitäten von Homeassistant abfragt. Das soll über die API von Homeassistant geschehen.  Der dazu benötigte API-Token steht in der Datei config.json. Dort steht auch die IP und der Port von Homeassistant. In der Datei entities.json stehen die abzufragenden Entitäten. Die Ausgabe soll in eine JSON-Datei erfolgen mit dem Namen data.json und soll nur den Namen (entity) und den Wert (state) enthalten. Das Python Programm soll nur aus der Datei src/main.py bestehen.
```

Ergebnis ist ein voll funktionsfähes Programm.

```text
Ich habe die Datei config.json geändert und erweitert. Ich benötige zwei weitere funktionen für die Ausgabe: influxdb in der Version 2 und mqtt. Die benötigten Informationen stehen bereits in der Datei config.json. Es muss jetzt nicht mehr nur eine Datei (main.py) sein. Erstelle eine entsprechende Verzeichnisstruktur mit modulen.
```

```text
Sehr gut! MQTT funktioniert prima. Bei der Influx implementierung bekomme ich eine Fehlermeldung: `InfluxDB-V2-Write fehlgeschlagen (422): {"code":"unprocessable entity","message":"failure writing points to database: partial write: field type conflict: input field \"value\" on measurement \"homeassistant\" is type integer, already exists as type float dropped=8"}` . Kannst Du das noch beheben?
```

```text
Jetzt lautet die Fehlermeldung `nfluxDB-V2-Write fehlgeschlagen (422): {"code":"unprocessable entity","message":"failure writing points to database: partial write: field type conflict: input field \"value\" on measurement \"homeassistant\" is type string, already exists as type float dropped=3"}`.
```

```text
Das sieht schon besser aus. Jetzt kommt nur noch die Fehlermeldung `InfluxDB-Ausgabe fehlgeschlagen: name 'build_line_protocol' is not defined`.
```

Alle Fehler sind behoben.

```text
Füge noch eine datei "develop.md" im Verzeichnis "docs" hinzu. Dort soll beschrieben sein, was nach einem frischen auschecken mit git alles zu tun ist, um das Projekt zu kompillieren und zu starten.
```
