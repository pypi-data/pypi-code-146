import os
import time
import numpy as np

shading = '.,-~:;=!*#$@'

r_t = 5
r_c = 4

vertical_offset = 10.
vertical_step_size = -.5

horizontal_offset = -10.
horizontal_step_size = .2

for beta in np.linspace(0, np.pi, 100):
    light_angle = np.array([np.cos(beta), 0., np.sin(beta)])
    donut = ''
    for i in range(40):
        p_y = vertical_offset + i * vertical_step_size
        for j in range(100):
            p_x = horizontal_offset + j * horizontal_step_size
            p_x_y_distance = np.sqrt(p_x ** 2 + p_y ** 2)

            if p_x_y_distance < (r_t - r_c) or p_x_y_distance > (r_t + r_c):
                donut += ' '
                continue

            p_z = -np.sqrt(r_c ** 2 - (p_x_y_distance - r_t) ** 2)

            c_x = r_t / p_x_y_distance * p_x
            c_y = r_t / p_x_y_distance * p_y
            c_z = 0.

            s = np.array([p_x - c_x, p_y - c_y, p_z - c_z])
            s_norm = s / np.sqrt(np.square(s).sum())
            luminance = -np.dot(light_angle, s_norm)
            donut += shading[int(round((len(shading) - 1) * luminance))]

        donut += '\n'

    os.system('cls')
    print(donut, end='')
    time.sleep(.1)
