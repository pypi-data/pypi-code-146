import numpy as np
import scipy as sc
import spiceypy
from pudb import set_trace as bp


def Occ_Plane_Conversion(N_data, pos_MEX, vel_MEX, pos_GS, vel_GS):

    gamma = np.zeros((N_data,))

    for i in range(N_data):

        vsep = spiceypy.spiceypy.vsep(pos_MEX[i], pos_GS[i])

        gamma[i] = vsep - (sc.pi / 2.0)

    r_MEX = np.zeros((N_data,))

    z_MEX = np.zeros((N_data,))

    z_GS = np.zeros((N_data,))

    for i in range(N_data):

        r_MEX[i] = np.linalg.norm(pos_MEX[i]) * np.cos(gamma[i])

        z_MEX[i] = np.linalg.norm(pos_MEX[i]) * np.sin(gamma[i])

        z_GS[i] = -np.linalg.norm(pos_GS[i])

    minus_pos_GS = np.full(
        (N_data, 3), np.nan
    )  # np.array([[np.nan for j in range(3)] for i in range(N_data)], dtype = float)

    for i in range(N_data):

        minus_pos_GS[i] = -pos_GS[i]

    vr_MEX = np.zeros((N_data,))

    vz_MEX = np.zeros((N_data,))

    vr_GS = np.zeros((N_data,))

    vz_GS = np.zeros((N_data,))

    for i in range(N_data):

        n_vec = np.cross(pos_GS[i], pos_MEX[i])

        r_vec = np.cross(minus_pos_GS[i], n_vec)

        M = 3

        B = np.array(
            [
                [n_vec[0], r_vec[0], minus_pos_GS[i][0], 1, 0, 0],
                [n_vec[1], r_vec[1], minus_pos_GS[i][1], 0, 1, 0],
                [n_vec[2], r_vec[2], minus_pos_GS[i][2], 0, 0, 1],
            ],
            dtype=float,
        )

        G = -1

        while G < M - 1:

            G += 1

            B[G, :] = B[G, :] / B[G, G]

            for J in range(M):

                if J == G:

                    K = G

                else:

                    if K == M - 1:

                        K = 0

                    else:

                        K += 1

                    B[K, :] = B[K, :] - B[K, G] * B[G, :]

        P = B[:, 3:6]

        beta_MEX = (
            vel_MEX[i][0] * P[1, 0] + vel_MEX[i][1] * P[1, 1] + vel_MEX[i][2] * P[1, 2]
        )

        gamma_MEX = (
            vel_MEX[i][0] * P[2, 0] + vel_MEX[i][1] * P[2, 1] + vel_MEX[i][2] * P[2, 2]
        )

        vr_MEX[i] = -np.sqrt(
            (beta_MEX * r_vec[0]) ** 2
            + (beta_MEX * r_vec[1]) ** 2
            + (beta_MEX * r_vec[2]) ** 2
        )

        vz_MEX[i] = np.sqrt(
            (gamma_MEX * minus_pos_GS[i][0]) ** 2
            + (gamma_MEX * minus_pos_GS[i][1]) ** 2
            + (gamma_MEX * minus_pos_GS[i][2]) ** 2
        )

        beta_GS = (
            vel_GS[i][0] * P[1, 0] + vel_GS[i][1] * P[1, 1] + vel_GS[i][2] * P[1, 2]
        )

        gamma_GS = (
            vel_GS[i][0] * P[2, 0] + vel_GS[i][1] * P[2, 1] + vel_GS[i][2] * P[2, 2]
        )

        vr_GS[i] = np.sqrt(
            (beta_GS * r_vec[0]) ** 2
            + (beta_GS * r_vec[1]) ** 2
            + (beta_GS * r_vec[2]) ** 2
        )

        vz_GS[i] = np.sqrt(
            (gamma_GS * minus_pos_GS[i][0]) ** 2
            + (gamma_GS * minus_pos_GS[i][1]) ** 2
            + (gamma_GS * minus_pos_GS[i][2]) ** 2
        )

        delta_s = np.zeros((N_data,))

        beta_e = np.zeros((N_data,))

    for i in range(N_data):

        a = np.array([r_MEX[i], z_MEX[i]], dtype=float)

        b = np.array([0, z_GS[i]], dtype=float)

        diff_vec = a - b

        delta_s[i] = np.arccos(
            np.dot(-b, diff_vec) / np.linalg.norm(-z_GS[i]) / np.linalg.norm(diff_vec)
        )

        beta_e[i] = (np.pi / 2.0) - np.arccos(
            np.dot(-b, diff_vec) / np.linalg.norm(-z_GS[i]) / np.linalg.norm(diff_vec)
        )

    # print('\tR7: Done')
    # print('gamma[3000]:',gamma[3000], 'beta_e[3000]:', beta_e[3000], 'delta_s[3000]:', delta_s[3000])
    return r_MEX, z_MEX, z_GS, vr_MEX, vz_MEX, vr_GS, vz_GS, gamma, beta_e, delta_s


def Occ_Plane_Conversion_2(N_data, pos_MEX, vel_MEX, pos_GS, vel_GS):

    z_vec = np.full(
        (N_data, 3), np.nan
    )  # np.array([[np.nan for j in range(3)] for i in range(N_data)], dtype = float)

    n_vec = np.full(
        (N_data, 3), np.nan
    )  # np.array([[np.nan for j in range(3)] for i in range(N_data)], dtype = float)

    r_vec = np.full(
        (N_data, 3), np.nan
    )  # np.array([[np.nan for j in range(3)] for i in range(N_data)], dtype = float)

    pos_MEX_new = np.full(
        (N_data, 3), np.nan
    )  # np.array([[np.nan for j in range(3)] for i in range(N_data)], dtype = float)

    vel_MEX_new = np.full(
        (N_data, 3), np.nan
    )  # np.array([[np.nan for j in range(3)] for i in range(N_data)], dtype = float)

    pos_GS_new = np.full(
        (N_data, 3), np.nan
    )  # np.array([[np.nan for j in range(3)] for i in range(N_data)], dtype = float)

    vel_GS_new = np.full(
        (N_data, 3), np.nan
    )  # np.array([[np.nan for j in range(3)] for i in range(N_data)], dtype = float)

    r_MEX = np.zeros((N_data,))

    z_MEX = np.zeros((N_data,))

    z_GS = np.zeros((N_data,))

    vr_MEX = np.zeros((N_data,))

    vz_MEX = np.zeros((N_data,))

    vr_GS = np.zeros((N_data,))

    vz_GS = np.zeros((N_data,))

    gamma = np.zeros((N_data,))

    for i in range(N_data):

        vsep = spiceypy.spiceypy.vsep(pos_MEX[i], pos_GS[i])

        gamma[i] = vsep - (sc.pi / 2.0)

        z_vec[i] = -pos_GS[i] / np.linalg.norm(pos_GS[i])

        n_vec[i] = np.cross(pos_MEX[i] / np.linalg.norm(pos_MEX[i]), z_vec[i]) / np.sin(
            (sc.pi / 2.0) - gamma[i]
        )

        r_vec[i] = np.cross(z_vec[i], n_vec[i])

        H_old_to_new = np.array([z_vec[i][:], n_vec[i][:], r_vec[i][:]], dtype=float)

        pos_MEX_new[i] = np.dot(H_old_to_new, pos_MEX[i])

        pos_GS_new[i] = np.dot(H_old_to_new, pos_GS[i])

        vel_MEX_new[i] = np.dot(H_old_to_new, vel_MEX[i])

        vel_GS_new[i] = np.dot(H_old_to_new, vel_GS[i])

        r_MEX[i] = pos_MEX_new[i][2]

        z_MEX[i] = pos_MEX_new[i][0]

        z_GS[i] = pos_GS_new[i][0]

        vr_MEX[i] = vel_MEX_new[i][2]

        vz_MEX[i] = vel_MEX_new[i][0]

        vr_GS[i] = vel_GS_new[i][2]

        vz_GS[i] = vel_GS_new[i][0]

    # print('')
    # print('')
    # print('\tR7: Done')
    # print('')
    # print('')

    return r_MEX, z_MEX, z_GS, vr_MEX, vz_MEX, vr_GS, vz_GS
