from datetime import date


class Activity:
    def __init__(self, name, datum, sportart, distanz, dauer):
        self.name = name
        self.datum = datum
        self.sportart = sportart
        self.distanz = distanz
        self.dauer = dauer



    def Monatskilometer_run_09(self, aktivitaeten):
        month_km_run_09 = 0
        for aktivity in aktivitaeten:
            if aktivity.datum.month == 9:
                if aktivity.sportart == "Laufen":
                    month_km_run_09 = month_km_run_09 + aktivity.distanz

        return month_km_run_09        


    def Monatskilometer_bike_09(self, aktivitaeten):
        month_km_bike_09 = 0
        for aktivity in aktivitaeten:
            if aktivity.datum.month == 9:
                if aktivity.sportart == "Radfahren":
                    month_km_bike_09 = month_km_bike_09 + aktivity.distanz

        return month_km_bike_09   



aktivitaeten = [
Activity("Morgenlauf", date(2026, 9, 2), "Laufen", 8.5, 40.6),
Activity("Feierabendrunde", date(2026, 9, 3), "Radfahren", 32.4, 78.5),
Activity("Lockerer Dauerlauf", date(2026, 9, 5), "Laufen", 6.2, 34.2),
Activity("Sonntagswanderung", date(2026, 9, 6), "Schwimmen", 1.8, 45.0),
Activity("Tempolauf", date(2026, 9, 8), "Laufen", 10.1, 48.3),
Activity("Radtour am Abend", date(2026, 9, 10), "Radfahren", 41.7, 96.4),
Activity("Regenerationslauf", date(2026, 9, 12), "Laufen", 5.4, 31.8),
Activity("Lange Radtour", date(2026, 9, 13), "Radfahren", 65.3, 152.7),
Activity("Morgenlauf", date(2026, 9, 16), "Laufen", 7.8, 38.9),
Activity("Bergwanderung", date(2026, 9, 19), "Schwimmen", 2.6, 41.9),
Activity("Intervalltraining", date(2026, 10, 1), "Laufen", 9.2, 43.5),
Activity("Feierabendrunde", date(2026, 10, 3), "Radfahren", 28.6, 69.2),
Activity("Lockerer Lauf", date(2026, 10, 5), "Laufen", 6.5, 35.1),
Activity("Herbstwanderung", date(2026, 10, 7), "Schwimmen", 2.4, 52.1),
Activity("Langer Lauf", date(2026, 10, 10), "Laufen", 14.3, 72.6),
Activity("Radtour am Wochenende", date(2026, 10, 11), "Radfahren", 52.8, 128.3),
Activity("Regenerationslauf", date(2026, 10, 14), "Laufen", 5.8, 32.4),
Activity("Tempoeinheit", date(2026, 10, 18), "Laufen", 11.6, 54.8),
Activity("Abendrunde", date(2026, 10, 23), "Radfahren", 36.2, 84.6),
Activity("Herbstlauf", date(2026, 10, 27), "Laufen", 8.7, 41.3)
]





print("Monatskilometer Laufen im September:", aktivitaeten[0].Monatskilometer_run_09(aktivitaeten))

print("Monatskilometer Radfahren im September:", aktivitaeten[0].Monatskilometer_bike_09(aktivitaeten))