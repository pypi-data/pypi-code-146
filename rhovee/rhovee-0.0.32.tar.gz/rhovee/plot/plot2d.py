import numpy as np
import matplotlib.pyplot as plt

def init_ax_equal_axis(ax, xlim, ylim):
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)


def draw_vector_2d(ax, vec, origin, color='black'):
    ax.arrow(origin[0], origin[1], vec[0], vec[1], head_width=0.1, head_length=0.1, color=color)

def draw_coord_sys_2d(ax, x_vec, y_vec, orig, size=1.0, label="", color=None):
    if color is None:
        x_color = 'red'
        y_color = 'green'
    else:
        x_color = color
        y_color = color
    draw_vector_2d(ax, x_vec, orig, color=x_color)
    draw_vector_2d(ax, y_vec, orig, color=y_color)
    text_pos = np.array(orig)-0.25*(np.array(x_vec)+np.array(y_vec))-0.2
    plt.text(text_pos[0],text_pos[1],label)

def draw_arrowhead(ax, vec, origin, color='black', label=""):
    label_pos = np.array(origin) - 0.35*np.array([vec[1], vec[0]])-0.2
    ax.arrow(origin[0], origin[1], vec[0]*0.0001, vec[1]*0.0001, head_width=0.3, head_length=0.5, edgecolor=color, facecolor='white')
    plt.text(label_pos[0],label_pos[1],label)






if __name__ == '__main__':
    fig,ax = plt.subplots()
    vec = [1,0]
    draw_vector_2d(ax, vec)
    plt.show()


