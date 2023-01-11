import time


def calculate_critical_threshold(racers_type):
    monaco_lap_distance = 3337  # meters
    if racers_type == "AIRCRAFT_FIGHTER":
        max_fighter_speed = 3000  # km/hour
        critical_threshold = calculate_minimal_theoretical_time_of_lap(max_fighter_speed, monaco_lap_distance)
    else:
        max_bolid_speed = 350  # km/hour
        critical_threshold = calculate_minimal_theoretical_time_of_lap(max_bolid_speed, monaco_lap_distance)
    return critical_threshold


def calculate_minimal_theoretical_time_of_lap(max_speed, distance):
    speed_m_sec = (max_speed * 1000) / 3600
    min_time = distance / speed_m_sec
    return min_time
