import time
import numpy as np


class TwoByTwoShareXPlot:
    """Plot for SR865A data streaming
    """
    def __init__(self, fig, data_rate=1.0):
        self.figure = fig

        self.data_rate = data_rate
        if self.data_rate < 1e-6:
            self.data_rate = 1e-6

        self.update_rate = 10  # Hz
        if self.update_rate > 25:
            self.update_rate = 25

        self.update_period = 1.0 / self.update_rate
        self.max_points_in_plot = 10000
        self._data_buffer_size = 10000000

        self.data_points = 0
        self.data_time = np.zeros(self._data_buffer_size)
        self.data_x = np.zeros(self._data_buffer_size)
        self.data_y = np.zeros(self._data_buffer_size)
        self.data_r = np.zeros(self._data_buffer_size)
        self.data_th = np.zeros(self._data_buffer_size)

        self.ax = self.figure.subplots(nrows=2, ncols=2, sharex=True)
        li00, = self.ax[0][0].plot(self.data_time[:2], self.data_x[:2], color='#00d000')
        li01, = self.ax[0][1].plot(self.data_time[:2], self.data_y[:2], color='#00e0e0')
        li10, = self.ax[1][0].plot(self.data_time[:2], self.data_r[:2], color='#e0e000')
        li11, = self.ax[1][1].plot(self.data_time[:2], self.data_th[:2], color='orange')
        self.line = [li00, li01, li10, li11]

        self.xlim_min = 0.0
        self.xlim_max = 10000 / self.data_rate
        self.ax[0][0].set_xlim(self.xlim_min, self.xlim_max)
        self.ax[0][0].set_ylim(-5, 5)
        self.ax[0][1].set_ylim(-5, 5)
        self.ax[1][0].set_ylim(-5, 5)
        self.ax[1][1].set_ylim(-5, 5)

        self.ax[0][0].set_title('X')
        self.ax[0][1].set_title('Y')
        self.ax[1][0].set_title('R')
        self.ax[1][1].set_title('Theta')

        self.index_min = 0
        self.index_max = 1
        self.index_step = 1

        self.ax[0][0].callbacks.connect('xlim_changed', self.on_xlim_changed)
        self.ax[0][1].callbacks.connect('xlim_changed', self.on_xlim_changed)
        self.ax[1][0].callbacks.connect('xlim_changed', self.on_xlim_changed)
        self.ax[1][1].callbacks.connect('xlim_changed', self.on_xlim_changed)

        self.init_time = time.time()
        self.last_time = self.init_time

    def on_xlim_changed(self, event_ax):
        x_min, x_max = event_ax.get_xlim()
        self.xlim_min = int(x_min)
        self.xlim_max = int(x_max) + 1

        self.index_step = (self.xlim_max - self.xlim_min) // self.max_points_in_plot
        if self.index_step < 1:
            self.index_step = 1

        self.index_min = self.xlim_min if self.xlim_min > 0 else 0
        self.index_max = self.xlim_max if self.xlim_max < self.data_points else self.data_points

    def set_buffer_size(self, size=10000000):
        self._data_buffer_size = size

        self.data_points = 0
        self.data_time = np.zeros(self._data_buffer_size)
        self.data_x = np.zeros(self._data_buffer_size)
        self.data_y = np.zeros(self._data_buffer_size)
        self.data_r = np.zeros(self._data_buffer_size)
        self.data_th = np.zeros(self._data_buffer_size)

    def get_buffer_size(self):
        return self._data_buffer_size

    def add_data_block(self, x, y, r, th):
        size = r.size
        init = self.data_points

        final = init + size
        if final > self._data_buffer_size:
            raise IndexError('Data reached the data buffer size.')

        ti = np.arange(init, final)
        self.data_time[init: final] = ti
        self.data_x[init: final] = x
        self.data_y[init: final] = y
        self.data_r[init: final] = r
        self.data_th[init: final] = th
        self.data_points = final

    def request_plot_update(self):
        current_time = time.time()
        if current_time - self.last_time < self.update_period:
            return False

        if self.data_points < self.xlim_max:
            self.index_max = self.data_points

        s = slice(self.index_min, self.index_max, self.index_step)
        ti = self.data_time[s]
        self.line[0].set_data(ti, self.data_x[s])
        self.line[1].set_data(ti, self.data_y[s])
        self.line[2].set_data(ti, self.data_r[s])
        self.line[3].set_data(ti, self.data_th[s])

        self.last_time = current_time
        return True

    def init_data_save(self, task):
        """
        Prepare to save streaming data to the file from the task
        """
        if not (hasattr(task, 'session_handler') and task.session_handler):
            raise ValueError('task has no session_handler')

        self.last_data_point = 0
        self.data_table_name = 'Stream Data'
        # Create a table to dave data
        task.create_table_in_file(self.data_table_name,
                                  'Time', 'X', 'Y')

    def save_data(self, task):
        """
        Save streaming data to file
        """
        data_index = self.last_data_point
        while data_index < self.data_points:
            task.add_to_table_in_file('Stream Data',
                self.data_time[data_index],
                self.data_x[data_index],
                self.data_y[data_index])
            data_index += 1
        self.last_data_point = self.data_points
