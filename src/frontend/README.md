# Frontend (Streamlit)

Oberfläche der Strava Activity Analytics. Zeigt eine Aktivitäts-Übersicht und ein Diagramm mit auswählbaren Datenkanälen.

## Voraussetzungen
- Pakete aus der `requirements.txt` (u. a. `streamlit`, `pandas`)

```bash
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## App starten

Im Hauptverzeichnis des Repositorys:

```bash
streamlit run src/frontend/app.py
```

Danach öffnet sich die App unter `http://localhost:8501`.

## Struktur

| Datei/Ordner | Inhalt |
|---|---|
| `app.py` | Startdatei, setzt die Seite zusammen |
| `components/overview.py` | Aktivitäts-Übersicht (in Arbeit) |
| `components/chart.py` | Diagramm mit Kanalauswahl (in Arbeit) |



=> Mit Hilfe von KI, den Inhalt der README.md erstellt.