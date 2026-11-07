# =====================================================
#   Autor:                 Danilo
#   Erstellungsdatum:      03.11.2026
#   Zuletzt bearbeitet:    04.11.2026
#   Beschreibung:          Verwendet die Backend-Klassen anhand einer Beispielaktivitaet.
#   Datei:                 app.py
# =====================================================

import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path


projekt_ordner = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(projekt_ordner))

from src.Backend.datenmodell import RadAktivitaet, RadMesspunkt


def main():

    start = datetime(2026, 11, 4, 10, 0, tzinfo=timezone.utc)

    radfahrt = RadAktivitaet(
        activity_id=1,
        athlete_id=1,
        name="Testrunde",
        sport_type="Ride",
        start_date=start,
        timezone="Europe/Berlin",
        distance_m=10000.0,
        moving_time_s=1800,
        elapsed_time_s=1900,
        total_elevation_gain_m=100.0,
        average_speed_m_s=5.56,
        max_speed_m_s=10.0,
        average_heartrate_bpm=130.0,
        max_heartrate_bpm=160.0,
        calories=None,
        elev_high_m=650.0,
        elev_low_m=600.0,
        average_watts=None,
        max_watts=None,
        weighted_average_watts=None,
        kilojoules=None,
        average_cadence=None,
        average_temp_c=8.0,
    )

    messpunkt_1 = RadMesspunkt(
        activity_id=radfahrt.activity_id,
        point_index=0,
        time=start,
        elapsed_seconds=0,
        distance_m=0.0,
        heartrate_bpm=100,
        speed_m_s=0.0,
        velocity_smooth_m_s=0.0,
        moving=False,
        grade_percent=0.0,
        altitude_m=600.0,
        latitude=None,
        longitude=None,
        watts=None,
        watts_calc=None,
        cadence=None,
        temperature_c=8,
    )

    messpunkt_2 = RadMesspunkt(
        activity_id=radfahrt.activity_id,
        point_index=1,
        time=start + timedelta(seconds=1),
        elapsed_seconds=1,
        distance_m=10.0,
        heartrate_bpm=130,
        speed_m_s=10.0,
        velocity_smooth_m_s=10.0,
        moving=True,
        grade_percent=2.0,
        altitude_m=600.3,
        latitude=None,
        longitude=None,
        watts=260,
        watts_calc=None,
        cadence=92,
        temperature_c=8,
    )

    radfahrt.messpunkte.append(messpunkt_1)
    radfahrt.messpunkte.append(messpunkt_2)

    print("Aktivitaet:", radfahrt.name)
    print("Sportart:", radfahrt.sport_type)
    print("Anzahl Messpunkte:", len(radfahrt.messpunkte))
    print("Herzfrequenz am ersten Messpunkt:", radfahrt.messpunkte[0].heartrate_bpm)
    print("Herzfrequenz am zweiten Messpunkt:", radfahrt.messpunkte[1].heartrate_bpm)


if __name__ == "__main__":
    main()
