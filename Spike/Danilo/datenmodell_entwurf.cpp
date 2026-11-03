/*
=====================================================
  Autor:                 Danilo
  Erstellungsdatum:      03.11.2026
  Zuletzt bearbeitet:    03.11.2026
  Beschreibung:          C++-Entwurf des Strava-Datenmodells mit Vererbung und Messpunkten.
  Datei:                 datenmodell_entwurf.cpp
=====================================================
*/

#include <cstdint>
#include <memory>
#include <optional>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

// C++17: Eine leere CSV-Zelle entspricht std::nullopt
// Feldnamen und Einheiten sind wie den Spalten der CSV-Dateien.
struct Messpunkt 
{
    std::int64_t activity_id;
    int point_index;
    std::string time;  // In Python ein datetime mit Zeitzone.
    int elapsed_seconds;
    std::optional<double> distance_m;
    std::optional<double> heartrate_bpm;
    std::optional<double> watts;
    std::optional<double> cadence;
    std::optional<double> speed_m_s;
    std::optional<double> grade_percent;
    std::optional<double> altitude_m;
    std::optional<double> latitude;
    std::optional<double> longitude;
    std::optional<double> temperature_c;
    std::optional<bool> moving;
    std::optional<double> velocity_smooth_m_s;
    std::optional<double> watts_calc;
};

class Aktivitaet 
{
public:
    std::int64_t activity_id;
    std::int64_t athlete_id;
    std::string name;
    std::string sport_type;  // Ride, Run, Swim, ...
    std::string start_date;
    std::string timezone;
    std::optional<double> distance_m;
    std::optional<int> moving_time_s;
    std::optional<int> elapsed_time_s;
    std::optional<double> total_elevation_gain_m;
    std::optional<double> elev_high_m;
    std::optional<double> elev_low_m;
    std::optional<double> average_speed_m_s;
    std::optional<double> max_speed_m_s;
    std::optional<double> average_heartrate_bpm;
    std::optional<double> max_heartrate_bpm;
    std::optional<double> average_watts;
    std::optional<double> max_watts;
    std::optional<double> weighted_average_watts;
    std::optional<double> kilojoules;
    std::optional<double> calories;
    std::optional<double> average_cadence;
    std::optional<double> average_temp_c;
    std::vector<Messpunkt> messpunkte;

    Aktivitaet(std::int64_t id, std::int64_t athlet_id, std::string bezeichnung, std::string sportart, std::string start, std::string zeitzone)
        : activity_id(id), athlete_id(athlet_id), name(std::move(bezeichnung)),
          sport_type(std::move(sportart)), start_date(std::move(start)),
          timezone(std::move(zeitzone)) {}

    virtual ~Aktivitaet() = default;

    void messpunkt_hinzufuegen(const Messpunkt& messpunkt) 
    {
        if (messpunkt.activity_id != activity_id) 
        {
            throw std::invalid_argument("Messpunkt gehoert zu einer anderen Aktivitaet.");
        }
        messpunkte.push_back(messpunkt);
    }
};

class Radfahrt : public Aktivitaet 
{
public:
    Radfahrt(std::int64_t id, std::int64_t athlet_id, std::string bezeichnung, std::string start, std::string zeitzone)
        : Aktivitaet(id, athlet_id, std::move(bezeichnung), "Ride", std::move(start), std::move(zeitzone)) {}
};

class Lauf : public Aktivitaet 
{
public:
    Lauf(std::int64_t id, std::int64_t athlet_id, std::string bezeichnung, std::string start, std::string zeitzone)
        : Aktivitaet(id, athlet_id, std::move(bezeichnung), "Run", std::move(start), std::move(zeitzone)) {}
};

class Schwimmen : public Aktivitaet 
{
public:
    Schwimmen(std::int64_t id, std::int64_t athlet_id, std::string bezeichnung, std::string start, std::string zeitzone)
        : Aktivitaet(id, athlet_id, std::move(bezeichnung), "Swim", std::move(start), std::move(zeitzone)) {}
};

class Aktivitaetensammlung 
{
public:
    // Zeiger erhalten die Unterklassen; Speicherung als Wert wuerde sie abschneiden.
    std::unordered_map<std::int64_t, std::unique_ptr<Aktivitaet>> aktivitaeten;

    void hinzufuegen(std::unique_ptr<Aktivitaet> aktivitaet) 
    {
        if (!aktivitaet) 
        {
            throw std::invalid_argument("Aktivitaet darf nicht leer sein.");
        }
        const auto id = aktivitaet->activity_id;
        if (aktivitaeten.count(id) != 0) 
        {
            throw std::invalid_argument("Aktivitaets-ID ist bereits vorhanden.");
        }
        aktivitaeten.emplace(id, std::move(aktivitaet));
    }

    Aktivitaet* finden(std::int64_t activity_id) 
    {
        auto eintrag = aktivitaeten.find(activity_id);
        if (eintrag == aktivitaeten.end()) 
        {
            return nullptr;
        }
        return eintrag->second.get();
    }

    const Aktivitaet* finden(std::int64_t activity_id) const 
    {
        auto eintrag = aktivitaeten.find(activity_id);
        if (eintrag == aktivitaeten.end()) 
        {
            return nullptr;
        }
        return eintrag->second.get();
    }

    std::vector<const Aktivitaet*> filtern(std::optional<std::string> sportart = std::nullopt, std::optional<std::int64_t> athlet_id = std::nullopt) const 
    {
        std::vector<const Aktivitaet*> ergebnis;
        for (const auto& eintrag : aktivitaeten) 
        {
            const auto& aktivitaet = *eintrag.second;
            if (sportart.has_value() && aktivitaet.sport_type != *sportart) 
            {
                continue;
            }
            if (athlet_id.has_value() && aktivitaet.athlete_id != *athlet_id) 
            {
                continue;
            }
            ergebnis.push_back(&aktivitaet);
        }
        return ergebnis;
    }
};

// Die activity_id ordnet jeden Messpunkt genau einer Aktivitaet zu.
