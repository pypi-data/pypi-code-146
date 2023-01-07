def deg_to_direction(degree):
    position = 0
    directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    if degree > 330 or degree <= 30:
        position = 0
    elif degree > 30 or degree <= 60:
        position = 1
    elif degree > 60 or degree <= 120:
        position = 2
    elif degree > 120 or degree <= 150:
        position = 3
    elif degree > 150 or degree <= 210:
        position = 4
    elif degree > 210 or degree <= 240:
        position = 5
    elif degree > 240 or degree <= 300:
        position = 6
    elif degree > 300 or degree <= 330:
        position = 7
    return directions[position]


def moon_phase_to_string(phase):
    position = 0
    phases = ['New', 'Wax C', '1 Q H',
              'Wax G', 'Full', 'Wan G',
              'L Q H', 'Wan C']
    if phase == 0 or phase == 1:
        position = 0
    elif phase < .25:
        position = 1
    elif phase < .35:
        position = 2
    elif phase < .5:
        position = 3
    elif phase == .5:
        position = 4
    elif phase < .63:
        position = 5
    elif phase == .75:
        position = 6
    elif phase < 1:
        position = 7
    return phases[position]
