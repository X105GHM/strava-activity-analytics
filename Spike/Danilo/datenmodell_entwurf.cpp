/*
=====================================================
  Autor:                 Danilo
  Erstellungsdatum:      03.11.2026
  Zuletzt bearbeitet:    04.11.2026
  Beschreibung:          C++-Entwurf des Strava-Datenmodells mit Vererbung und Messpunkten.
  Datei:                 datenmodell_entwurf.cpp
=====================================================
*/


#pragma once

#include <chrono>
#include <cstdint>
#include <memory>
#include <optional>
#include <string>
#include <vector>


// ==========================================
// Messpunkte
// ==========================================

struct Messpunkt 
{
    std::int64_t activity_id{};
    int point_index{};
    std::chrono::system_clock::time_point time{};
    int elapsed_seconds{};
    double distance_m{};
    std::optional<int> heartrate_bpm;
    double speed_m_s{};
    double velocity_smooth_m_s{};
    bool moving{};

    virtual ~Messpunkt() = default;
};

struct LandMesspunkt : Messpunkt 
{
    double grade_percent{};
    std::optional<double> altitude_m;
    std::optional<double> latitude;
    std::optional<double> longitude;
    std::optional<int> watts;
    std::optional<int> watts_calc;
};

struct RadMesspunkt : LandMesspunkt 
{
    std::optional<int> cadence;
    std::optional<int> temperature_c;
};

struct LaufMesspunkt : LandMesspunkt {};

struct SchwimmMesspunkt : Messpunkt {};


// ==========================================
// Aktivitäten
// ==========================================

struct Aktivitaet 
{
    std::int64_t activity_id{};
    std::int64_t athlete_id{};
    std::string name;
    std::string sport_type;
    std::chrono::system_clock::time_point start_date{};
    std::string timezone;

    double distance_m{};
    int moving_time_s{};
    int elapsed_time_s{};
    double total_elevation_gain_m{};

    double average_speed_m_s{};
    double max_speed_m_s{};
    std::optional<double> average_heartrate_bpm;
    std::optional<double> max_heartrate_bpm;
    std::optional<double> calories;

    std::vector<std::unique_ptr<Messpunkt>> messpunkte;

    virtual ~Aktivitaet() = default;
};

struct LandAktivitaet : Aktivitaet 
{
    std::optional<double> elev_high_m;
    std::optional<double> elev_low_m;

    std::optional<double> average_watts;
    std::optional<double> max_watts;
    std::optional<double> weighted_average_watts;
    std::optional<double> kilojoules;
};

struct RadAktivitaet : LandAktivitaet 
{
    std::optional<double> average_cadence;
    std::optional<double> average_temp_c;
};

struct LaufAktivitaet : LandAktivitaet {};

struct SchwimmAktivitaet : Aktivitaet {};
