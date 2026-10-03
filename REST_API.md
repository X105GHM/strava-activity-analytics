# Strava Data API

> **Hinweis zur KI-Unterstützung:** Diese API und ihre Dokumentation wurden mit Unterstützung von KI entwickelt. Code und Dokumentation können Fehler enthalten und sollten vor dem produktiven Einsatz geprüft werden.

REST-Schnittstelle für Athleten, Aktivitäten und zeitaufgelöste Trainingsdaten.
Die API liefert gespeicherte Daten als JSON. Aktualisierungen werden separat
angefordert und im Hintergrund verarbeitet.

**Basis-URL:** `https://sport.x105ghm.com/api/v1`  
**Version:** `v1`

Die IDs und Messwerte in den folgenden JSON-Beispielen sind Beispieldaten.
Für Abfragen die IDs aus der eigenen Athleten- und Aktivitätenliste verwenden.

## Schnellstart

Alle Datenendpunkte benötigen einen API-Token im Header:

```http
Authorization: Bearer <API_TOKEN>
```

Für Windows CMD:

```cmd
set "BASE=https://sport.x105ghm.com"
set "TOKEN=DEIN_API_TOKEN"

curl.exe -sS -H "Authorization: Bearer %TOKEN%" "%BASE%/api/v1/athletes" | python -m json.tool
```

Mit einer zurückgegebenen Athleten-ID die Aktivitäten abfragen:

```cmd
set "ATHLETE_ID=12345"

curl.exe -sS -H "Authorization: Bearer %TOKEN%" "%BASE%/api/v1/athletes/%ATHLETE_ID%/activities?limit=10" | python -m json.tool
```

Mit einer Aktivitäts-ID die Messpunkte lesen:

```cmd
set "ACTIVITY_ID=67890"

curl.exe -sS -H "Authorization: Bearer %TOKEN%" "%BASE%/api/v1/activities/%ACTIVITY_ID%/streams?types=time,power,cadence" | python -m json.tool
```

Unter Linux und macOS entsprechend:

```bash
export BASE="https://sport.x105ghm.com"
# TOKEN im eigenen Terminal setzen, nicht im Repository hinterlegen.
curl -sS -H "Authorization: Bearer $TOKEN" "$BASE/api/v1/athletes"
```

Ein Token kann auf einen Athleten beschränkt sein oder Zugriff auf mehrere
gespeicherte Athleten erlauben. Ein API-Token ist keine Strava-Anmeldung.
Tokens gehören nicht in URLs, Quellcode oder veröffentlichte Beispielausgaben.

## Endpunkte

Alle Pfade in dieser Tabelle beginnen mit `/api/v1`.

| Methode | Pfad | Beschreibung |
| --- | --- | --- |
| GET | `/athletes` | Zugängliche Athleten |
| GET | `/athletes/{athlete_id}` | Einzelner Athlet |
| GET | `/athletes/{athlete_id}/activities` | Aktivitäten mit Filtern und Pagination |
| GET | `/activities/{activity_id}` | Aktivitätsdetails und Sensor-Zusammenfassungen |
| GET | `/activities/{activity_id}/streams` | Messpunkt-Zeitreihen |
| GET | `/activities/{activity_id}/segments` | Segmentdurchfahrten |
| GET | `/activities/{activity_id}/laps` | Runden |
| GET | `/activities/{activity_id}/analytics` | Auswertungen gespeicherter Streams |
| GET | `/athletes/{athlete_id}/analytics` | Wochenübersicht je Sportart |
| POST | `/athletes/{athlete_id}/sync` | Aktivitätenkatalog aktualisieren |
| POST | `/activities/{activity_id}/refresh` | Aktivität und zugehörige Daten aktualisieren |
| GET | `/sync/jobs/{job_id}` | Status eines Aktualisierungsauftrags |

Ein GET löst keinen Strava-Abruf aus. Auch fehlende oder veraltete Daten werden
nicht während der Abfrage nachgeladen.

## Athleten und Aktivitäten

`GET /athletes` liefert ein Objekt mit dem Array `athletes`. Ein Athlet enthält
`id`, `name`, `timezone`, `history_complete` und `meta`.

### Aktivitätenliste

```http
GET /api/v1/athletes/12345/activities?from=2026-09-01&to=2026-09-30&sport_type=ride&limit=50&offset=0
```

| Parameter | Format | Standard | Bedeutung |
| --- | --- | --- | --- |
| `from` | `YYYY-MM-DD` | kein Filter | Erster Tag, einschließlich |
| `to` | `YYYY-MM-DD` | kein Filter | Letzter Tag, einschließlich |
| `sport_type` | String | alle | Exakter normalisierter Sportname, z. B. `ride`, `run`, `swim` |
| `limit` | Integer, 1–500 | 50 | Maximale Anzahl pro Antwort |
| `offset` | Integer, ab 0 | 0 | Anzahl übersprungener Einträge |

Datumsfilter beziehen sich auf die Startzeit in UTC. Aktivitäten ohne bekannte
Startzeit erscheinen nicht in einer nach Datum gefilterten Liste. Die Sortierung
erfolgt nach Startzeit absteigend, bei gleichem Zeitpunkt nach ID.

Die Antwort enthält:

| Feld | Bedeutung |
| --- | --- |
| `athlete_id` | Zugehöriger Athlet |
| `activities` | Array von Aktivitätsobjekten |
| `total` | Anzahl gespeicherter Aktivitäten, die den Filtern entsprechen |
| `limit`, `offset` | Verwendete Pagination |
| `history_complete` | Ob eine vollständige Historie nachgewiesen ist |

`total` ist nicht die Anzahl aller Aktivitäten bei Strava.
`history_complete: false` bedeutet, dass ältere Aktivitäten im Katalog fehlen können.

### Aktivitätsdetails

Die Liste und `GET /activities/{activity_id}` verwenden dasselbe Aktivitätsmodell.
Ein Katalogeintrag kann bereits vorhanden sein, obwohl seine Detailseite noch
nicht abgefragt wurde. Das zeigt `availability.details: "not_checked"`.

| Felder | Inhalt / Einheit |
| --- | --- |
| `id`, `athlete_id` | IDs als Strings |
| `title`, `description` | Titel und Beschreibung |
| `sport_type`, `original_sport_type` | Normalisierte und ursprüngliche Sportbezeichnung |
| `start_time`, `timezone` | Startzeit mit Zeitzone; zusätzliche Zeitzonenangabe, sofern vorhanden |
| `distance_m`, `elevation_gain_m` | Distanz und Höhengewinn in Metern |
| `moving_time_s`, `elapsed_time_s` | Bewegungszeit und Gesamtzeit in Sekunden |
| `speed`, `pace`, `heart_rate`, `cadence`, `power`, `temperature` | Sensor-Zusammenfassungen |
| `work_kj`, `calories_kcal` | Arbeit in kJ und Kalorien in kcal |
| `device`, `gear` | Aufzeichnungsgerät und Ausrüstung |
| `virtual`, `commute`, `workout`, `workout_type` | Aktivitätsmerkmale, soweit bekannt |
| `visibility`, `is_owner` | Sichtbarkeit und Eigentümerstatus aus Sicht der Datenquelle |
| `availability` | Verfügbarkeit von Details, Streams, Segmenten und Runden |
| `meta` | Herkunft und Aktualisierungsstatus |

Sensor-Zusammenfassungen verwenden diese Struktur:

```json
{
  "status": "available",
  "average": 199.0,
  "maximum": 798.0,
  "weighted_average": 210.0,
  "displayed_value": null,
  "unit": "W",
  "source": "activity_summary"
}
```

Die Einheit gilt für alle Zahlen dieses Objekts. Je nach Sensor sind nur einzelne
Felder gefüllt. Ein angezeigter Temperaturwert kann beispielsweise unter
`displayed_value` stehen; daraus wird kein Temperaturmittel erfunden.
`weighted_average` bezeichnet den von der Quelle übernommenen Wert.

## Streams

Ein Stream ist eine Messreihe. Die Antwort enthält die Reihen unter `streams`,
den Gesamtstatus unter `status` und Informationen zum letzten Abruf unter `meta`.

### Auswahl und Zeitfilter

```http
GET /api/v1/activities/67890/streams?types=time,power,cadence&from_time_s=42&to_time_s=46
```

| Parameter | Bedeutung |
| --- | --- |
| `types` | Durch Kommas getrennte API-Namen, z. B. `time,heart_rate,power`. Ohne Auswahl werden alle gespeicherten Streams geliefert. |
| `from_time_s` | Untere Zeitgrenze in Sekunden, einschließlich; mindestens 0 |
| `to_time_s` | Obere Zeitgrenze in Sekunden, einschließlich; mindestens 0 |

Zeitgrenzen gelten für die tatsächlichen Werte der Zeitachse. Es gibt keine
automatische Verschiebung auf Sekunde 0 und keine Begrenzung der Samplezahl.
Für Analysen `time` zusammen mit den gewünschten Kanälen abfragen.

### Beispielantwort

```json
{
  "activity_id": "67890",
  "status": "available",
  "streams": {
    "time": {
      "raw_name": "time",
      "status": "available",
      "unit": "s",
      "source": "strava_web",
      "points": 3,
      "data": [42, 43, 51],
      "null_count": 0,
      "time_alignment": "shared_time",
      "time_s": null
    },
    "power": {
      "raw_name": "watts",
      "status": "available",
      "unit": "W",
      "source": "measured",
      "points": 3,
      "data": [0, null, 200],
      "null_count": 1,
      "time_alignment": "shared_time",
      "time_s": null
    }
  },
  "time_axis": "time",
  "warnings": [],
  "meta": {
    "source": "strava_web",
    "schema_version": 1,
    "fetched_at": "2026-10-03T12:00:00Z",
    "last_attempt_at": "2026-10-03T12:00:00Z",
    "last_attempt_status": "available",
    "upstream_status": 200,
    "stale": false
  }
}
```

Hier wurden bei Sekunde 42 genau 0 W gemessen. Bei Sekunde 43 fehlt der
Leistungswert. Der nächste Punkt liegt bei Sekunde 51. Für die Lücke werden
keine Messwerte ergänzt.

### Namen und Einheiten

| API-Name | Strava-Name (`raw_name`) | Einheit / Datenform |
| --- | --- | --- |
| `time` | `time` | `s`, Sekunden seit Aktivitätsstart |
| `timer_time` | `timer_time` | `s`, separate Timerwerte der Quelle |
| `distance` | `distance` | `m` |
| `gps` | `latlng` | `degrees`, Paare `[latitude, longitude]` |
| `altitude` | `altitude` | `m` |
| `heart_rate` | `heartrate` | `bpm` |
| `cadence` | `cadence` | `rpm` |
| `power` | `watts` | `W`, `source: measured` |
| `calculated_power` | `watts_calc` | `W`, `source: calculated` |
| `speed` | `velocity_smooth` | `m/s` |
| `grade` | `grade_smooth` | `percent` |
| `temperature` | `temp` | `C`, Grad Celsius |
| `moving` | `moving` | `boolean` |
| `resting` | `resting` | `boolean` |
| `outlier` | `outlier` | `boolean` |
| `grade_adjusted_distance` | `grade_adjusted_distance` | `m` |
| `privacy` | `privacy` | Einheit und weitere Semantik nicht festgelegt |

Zusätzliche Reihen bleiben unter ihrem ursprünglichen Namen erhalten.
`unit: null` bedeutet, dass keine bestätigte Einheit hinterlegt ist. Das gilt
derzeit unter anderem für zusätzliche `pace`- und `grade_adjusted_pace`-Streams.
Sie dürfen nicht allein anhand ihres Namens als Sekunden pro Kilometer interpretiert werden.

### Zeitliche Zuordnung

| `time_alignment` | Verwendung |
| --- | --- |
| `shared_time` | Die Reihe verwendet die gemeinsame `time`-Achse. |
| `own_time` | Die Reihe besitzt eine eigene Achse unter `time_s`. |
| `length_mismatch` | Die Länge passt nicht zur gemeinsamen Achse. |
| `unverified` | Die zeitliche Zuordnung ist nicht bestätigt. |

Nur bei `shared_time` dürfen die Werte direkt mit dem gemeinsamen Zeitarray
punktweise zusammengeführt werden. `time_s: null` ist in diesem Fall normal.
Ein Arrayindex ist keine Sekunde. Gleiche Arraylängen allein beweisen bei
unbekannten Kanälen keine Synchronisierung.

Ein Zeitfilter auf eine verfügbare Reihe ohne bestätigte Zeitachse führt zu
`409 unaligned_streams`. In diesem Fall mit `types` nur bestätigte Reihen
auswählen oder die ungefilterten Daten prüfen.

`points` und `null_count` beziehen sich nach einer Zeitfilterung auf den
gelieferten Ausschnitt. `warnings` können weiterhin andere Reihen des
gespeicherten Datensatzes betreffen, auch wenn diese nicht ausgewählt wurden.

## Verfügbarkeit und fehlende Werte

| Status | Bedeutung |
| --- | --- |
| `available` | Daten sind vorhanden. |
| `not_present` | Bei einer erfolgreichen Prüfung nicht enthalten; Ursache unbekannt. |
| `not_recorded` | Fehlende Aufzeichnung ist ausdrücklich nachgewiesen. |
| `not_visible` | Einschränkung der Sichtbarkeit ist ausdrücklich nachgewiesen. |
| `access_denied` | Die Datenquelle hat den Zugriff verweigert. |
| `not_checked` | Noch nicht geprüft oder abgefragt. |
| `fetch_failed` | Abruf oder Verarbeitung fehlgeschlagen. |
| `unknown` | Zustand nicht eindeutig zugeordnet. |

Diese Fälle sind verschieden:

| Darstellung | Bedeutung |
| --- | --- |
| `data: [0, 100]` | Zwei reale Messwerte, darunter ein Nullwert |
| `data: [null, 100]` | Ein fehlender Messwert, ein vorhandener Wert |
| `data: null`, `points: null` | Keine verfügbare Messreihe |
| `data: []`, `points: 0` | Verfügbare Reihe mit leerem Ergebnis, etwa nach Zeitfilterung |

Fehlende Herzfrequenz oder Leistung wird nicht durch Nullen ersetzt.
Ein unter `types` angeforderter, bislang nicht gespeicherter Kanal kann
`not_checked` liefern. Die Auswahl löst keinen zusätzlichen Abruf aus.

### HTTP 200 trotz fehlender Streams

Wenn die Aktivität bekannt ist, kann `/streams` HTTP 200 liefern, obwohl
die Messreihen nicht verfügbar sind:

```json
{
  "activity_id": "67890",
  "status": "access_denied",
  "streams": {},
  "time_axis": "time",
  "warnings": [],
  "meta": {
    "source": "strava_web",
    "schema_version": 1,
    "fetched_at": null,
    "last_attempt_at": "2026-10-03T12:00:00Z",
    "last_attempt_status": "access_denied",
    "upstream_status": 403,
    "stale": true
  }
}
```

HTTP 200 bestätigt hier die erfolgreiche Abfrage der API-Ressource.
Für die Verfügbarkeit zusätzlich `status` und die einzelnen Streamstatus prüfen.
`meta.upstream_status` gehört zur Datenquelle, nicht zum HTTP-Status der API.

## Segmente und Runden

`GET /activities/{activity_id}/segments` und `/laps` liefern dieselbe Hülle:
`activity_id`, `status`, `items` und `meta`.

Ein Eintrag in `items` kann folgende Felder enthalten:

| Felder | Inhalt |
| --- | --- |
| `effort_id`, `segment_id`, `name` | Kennung und Bezeichnung |
| `distance_m` | Distanz in Metern |
| `elapsed_time_s`, `moving_time_s` | Zeiten in Sekunden |
| `start_index`, `end_index` | Originalindizes der Quelle |
| `average_speed_mps`, `max_speed_mps` | Geschwindigkeit |
| `average_cadence_rpm`, `max_cadence_rpm` | Kadenz |
| `average_power_w` | Durchschnittliche Leistung |
| `average_heart_rate_bpm`, `max_heart_rate_bpm` | Herzfrequenz |
| `elevation_gain_m`, `elevation_difference_m` | Höhenangaben |
| `achievements`, `ranking` | Vorhandene Erfolge und Ranginformationen |

Nicht vorhandene Werte bleiben `null`; Erfolge und Rankings können leere Objekte sein.
Die Originalindizes sind nicht automatisch Indizes der ausgelieferten Streamarrays.
Anfangsoffsets oder reduzierte Web-Zeitreihen können die Zuordnung verändern.
Runden sind keine allgemein bestätigte Quelle für alle sportabhängigen Splits.

## Analytics

### Aktivität

`GET /activities/{activity_id}/analytics` wertet die gespeicherten Streams aus.
Die Antwort enthält `status`, `metrics`, `summary_metrics`, `warnings` und `meta`.

Unter `metrics` stehen je Reihe Samplezahl, Anzahl fehlender Werte und Einheit.
Für numerische Werte werden zusätzlich `minimum`, `maximum` und `sample_average`
berechnet. Nullwerte werden beim Mittel ausgelassen; echte Nullen werden mitgerechnet.

`sample_average` ist das arithmetische Mittel der vorhandenen Samples, kein
zeitgewichtetes Mittel. `summary_metrics` enthält separat die Werte aus der
Aktivitätszusammenfassung. Beide Quellen können unterschiedliche Ergebnisse liefern.

Die Zeit-Auswertung `metrics.time_range` enthält `start_s`, `end_s`, `span_s`,
`minimum_interval_s` und `maximum_interval_s`. Falls vorhanden, wird
`moving_time_from_stream` aus beobachteten Intervallen berechnet. Größere Lücken
werden ausgeschlossen und unter `excluded_gap_s` ausgewiesen.

Die Auswertung verwendet den gespeicherten Datensatz. Sie übernimmt keine
Zeit- oder Streamfilter einer zuvor ausgeführten `/streams`-Abfrage.

### Athlet

`GET /athletes/{athlete_id}/analytics` liefert derzeit eine Wochenübersicht:

| Feld | Bedeutung |
| --- | --- |
| `schema_version` | Modellversion |
| `generated_at`, `data_age_seconds`, `stale` | Alter der Zusammenfassung |
| `week` | ISO-Jahr, ISO-Woche sowie Start- und Enddatum |
| `baseline_weeks` | Anzahl der Wochen für den Durchschnitt |
| `sports.swim`, `sports.run`, `sports.ride` | Werte je Sportart |
| `source` | Herkunft der Zusammenfassung |

Jede Sportart enthält `current_m` für die aktuelle Woche und `average_week_m`
für den Wochenmittelwert über die angegebene Basis. Alle Distanzen sind Meter.
Der Endpunkt ist keine frei filterbare Langzeit-Trainingsanalyse.

## Aktualisierung

1. Athleten mit `GET /athletes` abfragen.
2. Mit `POST /athletes/{athlete_id}/sync` den Aktivitätenkatalog aktualisieren.
3. Den Auftrag über `GET /sync/jobs/{job_id}` verfolgen.
4. Aktivitätenliste lesen und gewünschte Aktivitäten auswählen.
5. Mit `POST /activities/{activity_id}/refresh` deren Details und Teilressourcen laden.
6. Nach Abschluss Streams und Analytics abfragen.

Ein Athleten-Sync lädt den sichtbaren Profilkatalog, nicht automatisch alle
Detailseiten oder die vollständige Historie. Für einen Activity-Refresh muss
die Aktivität bereits im Repository bekannt sein.

Die beiden POST-Endpunkte benötigen keinen Request-Body und antworten mit
HTTP 202 sowie einem Auftrag:

```json
{
  "id": "2bbdb2a9f7d948869c5ec1cc9d971bfb",
  "resource_type": "activity",
  "resource_id": "67890",
  "state": "queued",
  "created_at": "2026-10-03T12:00:00Z",
  "updated_at": "2026-10-03T12:00:00Z",
  "results": {}
}
```

| `state` | Bedeutung |
| --- | --- |
| `queued` | Auftrag wartet auf Verarbeitung. |
| `running` | Verarbeitung läuft. |
| `success` | Alle gemeldeten Teilabrufe erfolgreich. |
| `partial` | Ein Teil der Abrufe war erfolgreich. |
| `failed` | Kein gemeldeter Teilabruf erfolgreich. |

Nach der Verarbeitung enthält `results` die Verfügbarkeit der einzelnen Teile,
beispielsweise `details`, `segments`, `laps` und `streams`.
HTTP 202 bedeutet Annahme des Auftrags, nicht erfolgreichen Datenabruf.

Wiederholte Anfragen während `queued` oder `running` liefern denselben Auftrag.
Nach dessen Abschluss gilt ein Cooldown von 60 Sekunden je Ressource; zu frühe
erneute Anfragen erhalten `409 sync_cooldown`. Ein Workerlauf erfolgt im üblichen
Betrieb etwa jede Minute. Die tatsächliche Wartezeit hängt auch von der Queue ab.

## Aktualität und Herkunft

Die Metadaten gehören jeweils zur abgefragten Ressource:

| Feld | Bedeutung |
| --- | --- |
| `source` | Datenquelle, z. B. `strava_web` oder `authorized_json_import` |
| `schema_version` | Version des gespeicherten Modells |
| `fetched_at` | Zeitpunkt des letzten erfolgreichen Abrufs; sonst `null` |
| `last_attempt_at` | Zeitpunkt des letzten Abrufversuchs |
| `last_attempt_status` | Ergebnis dieses Versuchs |
| `upstream_status` | HTTP-Status der Datenquelle, sofern bekannt |
| `stale` | Daten sind nach Altersgrenze oder fehlgeschlagenem Refresh veraltet. |

Ein fehlgeschlagener Refresh löscht keine vorhandenen Messpunkte.
Eine Ressource kann deshalb `status: available` und zugleich `meta.stale: true`
sowie `last_attempt_status: access_denied` melden. Das sind weiterhin die Daten
des letzten erfolgreichen Abrufs.

Die Metadaten eines Katalogeintrags belegen nicht, dass alle Teilressourcen
geprüft sind. Dafür `availability` und die Metadaten der jeweiligen Teilressource lesen.

## Fehler und HTTP-Status

Fehler der Anwendung verwenden dieses Format:

```json
{
  "error": {
    "code": "activity_not_found",
    "message": "Activity not found; synchronize its athlete or refresh explicitly.",
    "details": {}
  }
}
```

| HTTP | Typischer Code / Bedeutung |
| --- | --- |
| 200 | Ressource geliefert; Datenverfügbarkeit zusätzlich prüfen |
| 202 | Aktualisierungsauftrag angenommen |
| 401 | `request_failed`: Token fehlt oder ist ungültig |
| 403 | `athlete_not_permitted`: Token erlaubt diesen Athleten nicht |
| 404 | `athlete_not_found`, `activity_not_found`, `job_not_found` oder `summary_not_found` |
| 409 | `sync_cooldown`, `source_not_enabled` oder `unaligned_streams` |
| 422 | `invalid_request`, `invalid_range` oder `invalid_stream_types` |
| 429 | Request-Limit des vorgeschalteten Proxys erreicht |
| 500 | `internal_error` |
| 503 | `configuration_unavailable` oder `summary_unavailable` |

Der öffentliche Proxy erlaubt GET und POST. Andere Methoden können HTTP 405
erhalten. Fehler des Proxys, etwa 429 oder 405, können ein anderes Antwortformat
haben. Clients sollten zuerst den HTTP-Status prüfen und erst danach JSON auswerten.

Der öffentliche Zugriff ist derzeit auf 60 Requests pro Minute je Client-IP
mit einem Burst von 20 begrenzt. Große JSON-Antworten werden bei entsprechender
Clientunterstützung gzip-komprimiert. Die Antworten verwenden
`Cache-Control: no-store`; das interne Repository bleibt davon unabhängig.
