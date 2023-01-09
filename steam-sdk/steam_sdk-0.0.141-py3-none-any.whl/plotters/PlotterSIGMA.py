import matplotlib.lines as lines
import matplotlib.patches as patches
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from steam_sdk.plotters.PlotterRoxie import plotEdges

def plot_multiple_areas(ax, areas, color=None):
    """
    Functions takes in a list of area objects and plot them on axis ax.
    :param ax: Axis to create plots.
    :param areas: list of SIGMA area objects.
    :param color: Color of the object
    :return:
    """
    for area in areas:
        if color:
            plot_area(ax, area, color)
        else:
            plot_area(ax, area)

def plot_area(ax, area, color=None):
    """
    Plots one SIGMA area object on axis ax
    :param ax: Axis to create plots.
    :param area: SIGMA area object.
    :param color: Color of the object
    :return:
    """
    if not color:
        color = 'black'
    points = []
    hls = area.getHyperLines()
    for hl in hls:
        last_dot_index = hl.toString().rfind('.')
        at_index = hl.toString().find('@')
        class_name = hl.toString()[last_dot_index + 1:at_index]
        if class_name == 'Line':
            points.append([hl.getKp1().getX(), hl.getKp1().getY()])
            points.append([hl.getKp2().getX(), hl.getKp2().getY()])
        elif class_name == 'Arc':
            start_angle = np.arctan2(hl.getKp1().getY() - hl.getKpc().getY(),
                                     hl.getKp1().getX() - hl.getKpc().getX()) * 180 / np.pi
            end_angle = start_angle + hl.getDTheta() * 180 / np.pi
            r = np.sqrt((hl.getKp1().getY() - hl.getKpc().getY()) ** 2 + (hl.getKp1().getX() - hl.getKpc().getX()) ** 2)
            ax.add_patch(patches.Arc([hl.getKpc().getX(), hl.getKpc().getY()], 2 * r, 2 * r, 0,
                                     min(start_angle, end_angle), max(start_angle, end_angle), color=color))
        elif class_name == 'Circumference':
            r = hl.getRadius()
            ax.add_patch(patches.Arc([hl.getCenter().getX(), hl.getCenter().getY()], 2 * r, 2 * r, 0, 0, 360))
        else:
            raise ValueError('Not supported Hyperline object!')

    ax.add_line(lines.Line2D([points[0][0], points[3][0]], [points[0][1], points[3][1]], color=color))
    ax.add_line(lines.Line2D([points[1][0], points[2][0]], [points[1][1], points[2][1]], color=color))


def plot_Bmod(df, map2d_name1, map2d_name2, fig, ax, cmap='plasma'):
    fig.suptitle(f" Bmod: {map2d_name1} and {map2d_name2} (mT)")
    f11 = ax[0, 0].scatter(df["x"], df['y'], c=abs(df["Bmod1"]) * 1000, cmap=cmap)
    ax[0, 0].set_title(f"Bmod: {map2d_name1} (mT)")
    ax[0, 0].set_xlabel('x-coordinate/mm')
    ax[0, 0].set_ylabel('y-coordinate/mm')
    f12 = ax[0, 1].scatter(df["x"], df['y'], c=abs(df["Bmod2"]) * 1000, cmap=cmap)
    ax[0, 1].set_title(f"Bmod: {map2d_name2} (mT)")
    ax[0, 1].set_xlabel('x-coordinate/mm')
    ax[0, 1].set_ylabel('y-coordinate/mm')
    ax[1, 0].plot(df["Bmod1"] * 1000, '.')
    ax[1, 0].set_title(f"Bmod scatter: {map2d_name1} (mT)")
    ax[1, 0].set_xlabel('Strand number')
    ax[1, 0].set_ylabel(f'Bmod scatter: {map2d_name1} (mT)')
    ax[1, 1].plot(df["Bmod2"] * 1000, '.')
    ax[1, 1].set_xlabel('Strand number')
    ax[1, 1].set_ylabel('Scatter Bmod (mT)')
    ax[1, 1].set_title(f"Bmod scatter: {map2d_name2} (mT)")

    fig.colorbar(f11, ax=ax[0, 0])
    fig.colorbar(f12, ax=ax[0, 1])


def plot_B_mod_error(df, map2d_name1, map2d_name2, fig, ax, cmap='plasma'):
    fig.suptitle(f"Bmod error: {map2d_name1} and {map2d_name2} (mT)")

    ax[0].set_aspect("equal")
    #ax[1].set_aspect("equal")

    f11 = ax[0].scatter(df["x"], df['y'], c=df["Bmod_error"] * 1000, cmap=cmap)
    ax[0].set_title(f"Bmod error (mT)")
    ax[0].set_xlabel('x-coordinate/mm')
    ax[0].set_ylabel('y-coordinate/mm')

    ax[1].set_title(f"Bmod error scatter (mT)")
    ax[1].set_xlabel('Strand')
    ax[1].set_ylabel('Bmod error (mT)')
    ax[1].plot(df["Bmod_error"]*1000, '.')
    fig.colorbar(f11, ax=ax[0])

def plot_relative_error_x_y(df, map2d_name1, map2d_name2, fig, ax, cmap='plasma'):
    fig.suptitle(f"Relative error: {map2d_name1} and {map2d_name2} (T)")
    f31 = ax[0, 0].scatter(df["x"], df['y'], c=df["rel_err_x"] * 100, cmap=cmap)
    ax[0, 0].set_title(f"Relative error Bx %")
    ax[0, 0].set_xlabel('x-coordinate/mm')
    ax[0, 0].set_ylabel('y-coordinate/mm')
    f32 = ax[0, 1].scatter(df["x"], df['y'], c=df["rel_err_y"] * 100, cmap=cmap)
    ax[0, 1].set_title(f"Relative error By %")
    ax[0, 1].set_xlabel('x-coordinate/mm')
    ax[0, 1].set_ylabel('y-coordinate/mm')

    ax[1, 0].plot(df["rel_err_x"] * 100, '.')
    ax[1, 0].set_title(f"Scatter Relative error  Bx %")
    ax[1, 0].set_xlabel('Strand number')
    ax[1, 0].set_ylabel('Relative error Bx %')
    ax[1, 1].plot(df["rel_err_y"] * 100, '.')
    ax[1, 1].set_xlabel('Strand number')
    ax[1, 1].set_ylabel('Relative error By %')
    ax[1, 1].set_title(f"Scatter Relative error  By %")

    fig.colorbar(f31, ax=ax[0, 0])
    fig.colorbar(f32, ax=ax[0, 1])


def plot_Bx_By(df, map2d_name1, map2d_name2, fig, ax, cmap='plasma'):
    fig.suptitle(f"Bx and By field: {map2d_name1} and {map2d_name2} (mT)")
    f41 = ax[0, 0].scatter(df["x"], df['y'], c=df["Bx1"] * 1000, cmap=cmap)

    ax[0, 0].set_title(f"Bx {map2d_name1} (mT)")
    ax[0, 0].set_xlabel('x-coordinate/mm')
    ax[0, 0].set_ylabel('y-coordinate/mm')
    f42 = ax[0, 1].scatter(df["x"], df['y'], c=df["By1"] * 1000, cmap=cmap)

    ax[0, 1].set_title(f"By {map2d_name1} (mT)")
    ax[0, 1].set_xlabel('x-coordinate/mm')
    ax[0, 1].set_ylabel('y-coordinate/mm')

    f43 = ax[1, 0].scatter(df["x"], df['y'], c=df["Bx2"] * 1000, cmap=cmap)

    ax[1, 0].set_title(f"Bx {map2d_name2} (mT)")
    ax[1, 0].set_xlabel('x-coordinate/mm')
    ax[1, 0].set_ylabel('y-coordinate/mm')
    f44 = ax[1, 1].scatter(df["x"], df['y'], c=df["By2"] * 1000, cmap=cmap)

    ax[1, 1].set_title(f"By {map2d_name2} (mT)")
    ax[1, 1].set_xlabel('x-coordinate/mm')
    ax[1, 1].set_ylabel('y-coordinate/mm')
    fig.colorbar(f41, ax=ax[0, 0])
    fig.colorbar(f42, ax=ax[0, 1])
    fig.colorbar(f43, ax=ax[1, 0])
    fig.colorbar(f44, ax=ax[1, 1])
    ax[2, 0].set_title(f"Bx scatter (mT)")
    ax[2, 0].plot(df["Bx1"] * 1000, '.', color='b', label=f"{map2d_name1}")
    ax[2, 0].plot(df["Bx2"] * 1000, '.', color='r', label=f"{map2d_name2}")
    ax[2, 1].set_title(f"By scatter (mT)")
    ax[2, 1].plot(df["By1"] * 1000, '.', color='b', label=f"{map2d_name1}")
    ax[2, 1].plot(df["By2"] * 1000, '.', color='r', label=f"{map2d_name2}")
    ax[2, 0].legend()
    ax[2, 1].legend()
def plot_abs_difference_Bx_By(df, map2d_name1, map2d_name2, fig, ax, cmap='plasma'):
    fig.suptitle(f" Absolute Difference: {map2d_name1} and {map2d_name2} (mT)")
    f11 = ax[0, 0].scatter(df["x"], df['y'], c=abs(df["diff_x"]) * 1000, cmap=cmap)
    ax[0, 0].set_title(f"Absolut difference Bx (mT)")
    ax[0, 0].set_xlabel('x-coordinate/mm')
    ax[0, 0].set_ylabel('y-coordinate/mm')
    f12 = ax[0, 1].scatter(df["x"], df['y'], c=abs(df["diff_y"]) * 1000, cmap=cmap)
    ax[0, 1].set_title(f"Absolut difference By (mT)")
    ax[0, 1].set_xlabel('x-coordinate/mm')
    ax[0, 1].set_ylabel('y-coordinate/mm')
    ax[1, 0].plot(df["diff_x"] * 1000, '.')
    ax[1, 0].set_title(f"Scatter difference Bx (mT)")
    ax[1, 0].set_xlabel('Strand number')
    ax[1, 0].set_ylabel('Difference Bx (mT)')
    ax[1, 1].plot(df["diff_y"] * 1000, '.')
    ax[1, 1].set_xlabel('Strand number')
    ax[1, 1].set_ylabel('Scatter difference By (mT)')
    ax[1, 1].set_title(f"Scatter difference By (mT)")

    fig.colorbar(f11, ax=ax[0, 0])
    fig.colorbar(f12, ax=ax[0, 1])


def generate_report_from_map2d(map2d_file_path1, map2d_name1, map2d_file_path2, map2d_name2):
    """
    Generate plots for comparing two map2d files. Method generates the following plots:
    Bmod fields, Bmod error, relative error Bx/By, Bx/By field, Bx/By error, absolut difference Bx/By
    :param map2d_file_path1: Path to map2d file nr 1
    :param map2d_name1: String name of map2d nr 1 (e.g SIGMA/ROXIE)
    :param map2d_file_path2: Path to map2d file nr 2
    :param map2d_name2: String name of map2d nr 1 (e.g SIGMA/ROXIE)
    :return: 
    """

    df1 = pd.read_csv(map2d_file_path1, delim_whitespace=True)
    df2 = pd.read_csv(map2d_file_path2, delim_whitespace=True)
    df = pd.DataFrame()
    df['x'] = df1["X-POS/MM"]
    df['y'] = df1["Y-POS/MM"]
    df["Bx1"] = df1["BX/T"]
    df["By1"] = df1["BY/T"]
    df["Bx2"] = df2["BX/T"]
    df["By2"] = df2["BY/T"]
    df["diff_x"] = df["Bx1"] - df["Bx2"]
    df["diff_y"] = df["By1"] - df["By2"]
    df["rel_err_x"] = abs((df["Bx1"] - df["Bx2"]) / df["Bx2"])
    df["rel_err_y"] = abs((df["By1"] - df["By2"]) / df["By2"])
    df["abs_err_x"] = abs(df["Bx1"] - df["Bx2"])
    df["abs_err_y"] = abs(df["By1"] - df["By2"])
    df["Bmod1"] = np.sqrt(df["Bx1"] ** 2 + df["By1"] ** 2)
    df["Bmod2"] = np.sqrt(df["Bx2"] ** 2 + df["By2"] ** 2)
    df["Bmod_error"] = abs(df["Bmod1"] - df["Bmod2"])
    fig1, ax1 = plt.subplots(2, 2, figsize=(12, 12))
    fig2, ax2 = plt.subplots(1, 2, figsize=(12, 12))
    fig3, ax3 = plt.subplots(3, 2, figsize=(12, 12))
    fig4, ax4 = plt.subplots(2, 2, figsize=(12, 12))
    fig5, ax5 = plt.subplots(2, 2, figsize=(12, 12))

    plot_Bmod(df, map2d_name1, map2d_name2, fig1, ax1)
    plot_B_mod_error(df,map2d_name1, map2d_name2, fig2, ax2)
    plot_Bx_By(df, map2d_name1, map2d_name2, fig3, ax3)
    try:
        plot_relative_error_x_y(df, map2d_name1, map2d_name2, fig4, ax4 )
    except:
        print("Couldn't generate relative error plots.")
    plot_abs_difference_Bx_By(df, map2d_name1, map2d_name2, fig5, ax5)
    plt.show()

def plot_roxie_coil(roxie_data):
    selectedFont = {'fontname': 'DejaVu Sans', 'size': 14}
    xPos = []
    yPos = []
    xBarePos = []
    yBarePos = []
    iPos = []
    for coil_nr, coil in roxie_data.coil.coils.items():
        for pole_nr, pole in coil.poles.items():
            for layer_nr, layer in pole.layers.items():
                for winding_key, winding in layer.windings.items():
                    for block_key, block in winding.blocks.items():
                        for halfTurn_nr, halfTurn in block.half_turns.items():
                            insu = halfTurn.corners.insulated
                            bare = halfTurn.corners.bare
                            xPos.append([insu.iL.x, insu.oL.x, insu.oR.x, insu.iR.x])
                            yPos.append([insu.iL.y, insu.oL.y, insu.oR.y, insu.iR.y])
                            xBarePos.append([bare.iL.x, bare.oL.x, bare.oR.x, bare.iR.x])
                            yBarePos.append([bare.iL.y, bare.oL.y, bare.oR.y, bare.iR.y])
                            iPos.append(block.current_sign)
    plotEdges(xPos, yPos, xBarePos, yBarePos, iPos, selectedFont)
    plt.show()
