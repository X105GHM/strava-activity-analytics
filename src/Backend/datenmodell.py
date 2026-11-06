# =====================================================
#   Autor:                 Danilo
#   Erstellungsdatum:      03.11.2026
#   Zuletzt bearbeitet:    06.11.2026
#   Beschreibung:          Datenmodell fuer Strava-Aktivitaeten mit Vererbung und Messpunkten.
#   Datei:                 datenmodell.py
# =====================================================

# Die Einschätzung ob ein member optional ist oder nicht, basiert auf einer Analyse der Testdaten von ChatGPT.
# Sensordaten können je nach Sportart, Aufnahmegeraet und Import fehlen.

from dataclasses import dataclass, field
from datetime import datetime


# ==========================================
# Messpunkte
# ==========================================

@dataclass(kw_only=True)                # kw_only=True damit die Attribute nur als Schlüsselwortargumente übergeben werden können
class Messpunkt:                       
    activity_id: int
    point_index: int
    time: datetime
    elapsed_seconds: int
    distance_m: float
    heartrate_bpm: int | None
    speed_m_s: float
    velocity_smooth_m_s: float
    moving: bool
    latitude: float | None = None
    longitude: float | None = None
    temperature_c: int | None = None


@dataclass(kw_only=True)
class LandMesspunkt(Messpunkt):
    grade_percent: float | None = None
    altitude_m: float | None
    watts: int | None
    watts_calc: int | None
    cadence: int | None = None


@dataclass(kw_only=True)
class RadMesspunkt(LandMesspunkt):
    pass


@dataclass(kw_only=True)
class LaufMesspunkt(LandMesspunkt):
    pass


@dataclass(kw_only=True)
class SchwimmMesspunkt(Messpunkt):
    pass


# ==========================================
# Aktivitäten
# ==========================================

@dataclass(kw_only=True)
class Aktivitaet:
    activity_id: int
    athlete_id: int
    name: str
    sport_type: str
    start_date: datetime
    timezone: str

    distance_m: float
    moving_time_s: int
    elapsed_time_s: int
    total_elevation_gain_m: float

    average_speed_m_s: float
    max_speed_m_s: float
    average_heartrate_bpm: float | None
    max_heartrate_bpm: float | None
    calories: float | None
    average_temp_c: float | None = None

    messpunkte: list[Messpunkt] = field(
        default_factory=list                    # Mit default_factory=list wird für jedes neu erzeugte Aktivitätsobjekt
    )                                           # eine separate Liste erstellt.


@dataclass(kw_only=True)
class LandAktivitaet(Aktivitaet):
    elev_high_m: float | None
    elev_low_m: float | None

    average_cadence: float | None = None
    average_watts: float | None = None
    max_watts: float | None = None
    weighted_average_watts: float | None = None
    kilojoules: float | None = None
    device_watts: bool | None = None


@dataclass(kw_only=True)
class RadAktivitaet(LandAktivitaet):
    pass


@dataclass(kw_only=True)
class LaufAktivitaet(LandAktivitaet):
    pass


@dataclass(kw_only=True)
class SchwimmAktivitaet(Aktivitaet):
    pass
