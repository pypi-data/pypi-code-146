import matplotlib as mpl
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D


def get_grid_dims(size):
    if size <= 0:
        return 0, 0

    sq = np.sqrt(size)
    rows = np.floor(sq)
    cols = rows + 1

    if (rows * cols) < size:
        rows = cols

    while ((cols - 1) * rows) >= size:
        cols -= 1
        print(cols)

    return int(rows), int(cols)


def _draw_hist(data, plot_params):
    plt.hist(data, **plot_params)


def summary_plot(
        data_df, group_key=None,
        figure_params=None, plot_params=None,
        grid=True, logy=False, logx=False,
        split_windows='None', show=True,
):
    """

    Args:
        data_df: pdf DataFrame
        group_key: column name, for grouping
        figure_params: dict used to initialize pyplot.Figure
        plot_params: dict used to affect plot params.
        grid: bool,
        logy: bool, Y axis log scaling
        logx: bool, X axis log scaling
        split_windows: string
            group - new window for each category
            column - new window for each column
            category - same as column
        show: bool, flag which calls `pyplot.show`


    Returns:

    """
    data_df = data_df.copy()
    total_columns = data_df.shape[1]

    "Check or initialize passed arguments"
    if figure_params is None:
        figure_params = dict()
    else:
        assert isinstance(
                figure_params,
                dict), f"Figure params must be dict type! but got: {type(figure_params)}"

    if 'figsize' not in figure_params:
        figure_params['figsize'] = 10, 7
    if 'dpi' not in figure_params:
        figure_params['dpi'] = 100

    if plot_params is None:
        plot_params = dict()
    else:
        assert isinstance(
                plot_params,
                dict), f"Plot params must be dict type! but got: {type(plot_params)}"

    """
    SPLIT
        Split by group
        Split by category/column
    """
    if split_windows in ['column', 'category']:
        if group_key is not None:
            figure_list = [plt.figure(**figure_params) for _ in range(total_columns - 1)]
        else:
            figure_list = [plt.figure(**figure_params) for _ in range(total_columns)]

    elif split_windows in ['group']:
        figure_list = []

    else:
        plt.figure(**figure_params)
        figure_list = None

    if group_key is not None:
        "Group data"
        group_dict = _grouping_plot(data_df, group_key=group_key)

        if split_windows in ['column', 'category']:
            plot_rows, plot_cols = get_grid_dims(len(group_dict))
        else:
            plot_rows, plot_cols = get_grid_dims(total_columns)

        for ind, (key, value) in enumerate(group_dict.items()):
            "Plot given selection matching to criteria"

            plot_params['label'] = key

            if split_windows == "group":
                fig = plt.figure(**figure_params)
                figure_list.append(fig)
                figures_for_column = None
                title = None

            elif split_windows in ['column', 'category']:
                title = key
                figures_for_column = figure_list
            else:
                title = None
                figures_for_column = None

            _column_iter_draw(
                    value, plot_rows, plot_cols,
                    grid=grid, plot_params=plot_params,
                    logy=logy, logx=logx,
                    figure_list=figures_for_column,
                    subplot_ind=ind + 1,
                    title=title,
            )

            if split_windows in ['column', 'category']:
                pass
                # _create_legend(list(group_dict.keys()))
                # plt.suptitle(f"{key}")

            elif split_windows == 'group':
                # _create_legend(list(group_dict.keys()))
                plt.suptitle(f"{key}")

            else:
                plt.subplot(plot_rows, plot_cols, total_columns)
                _create_legend(list(group_dict.keys()))
                plt.axis('off')
                plt.tight_layout()

        if figure_list:
            for ind, figure in enumerate(figure_list):
                columns = data_df.columns
                if split_windows in ['column', 'category']:
                    plt.figure(figure.number)
                    plt.suptitle(columns[ind])

    else:
        plot_rows, plot_cols = get_grid_dims(total_columns)
        _column_iter_draw(
                data_df, plot_rows, plot_cols, grid, plot_params,
                logy=logy, logx=logx, figure_list=figure_list,
        )

    if figure_list:
        for figi in figure_list:
            plt.figure(figi.number)
            plt.tight_layout()
            plt.subplots_adjust(hspace=0.3)

    if show:
        plt.show()


def _create_legend(names_list):
    color_cycler = mpl.rcParams['axes.prop_cycle']

    actors = []
    for name, style_dict in zip(names_list, color_cycler):
        line = Line2D([0, 0], [0, 0], linewidth=5, **style_dict)
        actors.append(line)

    plt.legend(actors, names_list)
    # plt.axis('off')


def _column_iter_draw(
        data_df, plot_rows, plot_cols, grid, plot_params, logx=False, logy=False,
        figure_list=None, subplot_ind=None, title=None,
):
    if figure_list is not None:
        assert len(figure_list) == data_df.shape[1], f"{len(figure_list)}, {data_df.shape[1]}"

    for col_ind, (name, value) in enumerate(data_df.items()):
        if figure_list is not None:
            plt.figure(figure_list[col_ind].number)
            if subplot_ind:
                plt.subplot(plot_rows, plot_cols, subplot_ind)
        else:
            plt.subplot(plot_rows, plot_cols, col_ind + 1)

        _draw_hist(value, plot_params)
        plt.xticks(rotation=30)
        if title:
            plt.title(title)
        else:
            plt.title(name)

        if grid:
            plt.grid(True)

        if logy and logx:
            plt.loglog()
        elif logy:
            plt.semilogy()
        elif logx:
            plt.semilogx()

        # plt.tight_layout()


def _grouping_plot(data_df, group_key):
    filter_column = data_df.pop(group_key)
    # print("DATA DF columns:")
    # print(data_df.columns)
    output_dict = dict()

    unique_vals = filter_column.unique()
    unique_vals.sort()

    for unq_val in unique_vals:
        mask = filter_column == unq_val
        minidf = data_df.loc[mask, :]
        key = f"{group_key}={unq_val}"
        output_dict[key] = minidf

    return output_dict


def _draw_plot(data, plot_params):
    plt.plot(data, **plot_params)
