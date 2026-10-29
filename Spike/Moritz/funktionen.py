
def hallo_strava():
    """Gibt eine kurze Begrüßung für das Strava-Projekt zurück."""
    return "Willkommen beim Strava Activity Analytics Projekt!"



def mittlere_distanz(aktivitaeten):
    """Berechnet die mittlere Distanz aller Aktivitäten."""
    summe = 0

    for aktivitaet in aktivitaeten:
        summe += aktivitaet["distanz_km"]

    return summe / len(aktivitaeten)