import numpy as np
import pandas as pd
import h5py
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.patches as mpatches
import matplotlib.cm as cm
import matplotlib.animation as anm
import matplotlib.collections as clt
import os
import json
from steam_nb_api.resources.ResourceReader import read_yaml

#quit()
# import matplotlib as mpl
# mpl.rcParams['animation.ffmpeg_path'] = r"C:\ffmpeg-4.3.2-2021-02-27-essentials_build\bin\ffmpeg.exe"

class UpdatablePatchCollection(clt.PatchCollection):
    def __init__(self, patches, *args, **kwargs):
        self.patch_col = patches
        clt.PatchCollection.__init__(self, patches, *args, **kwargs)

    def get_paths(self):
        self.set_paths(self.patch_col)
        return self._paths

class Post_LEDET:
    def __init__(self, magnet_name, model_no, LEDET_folder, magnet_inputs_path=''):
        self.magnet_name = magnet_name
        self.model_no = model_no
        self.LEDET_folder = LEDET_folder
        self.magnet_inputs_path = magnet_inputs_path
        self.output_folder = os.path.join(self.LEDET_folder, 'LEDET', magnet_name)
        self.matlab_file_prefix = os.path.join(self.output_folder, "Output", "Mat Files", f"SimulationResults_LEDET_")
        self.data = h5py.File(f"{self.matlab_file_prefix}{self.model_no}.mat", 'r')
        self.lines = []
        self.lines_data = []
        self.lines_dict = []
        self.patches = []
        self.patches_dict = []
        self.patches_data = []
        self.t = np.array(self.data.get('time_vector')).T[0]
        self.E_unit_multip = 1e-3
        self.font_size = 12
        self.line_width = 0.7
        plt.rcParams["font.family"] = "Times New Roman"
        plt.rcParams.update({'font.size': self.font_size})
        plt.rcParams.update({'lines.linewidth': self.line_width})
        # print(plt.rcParams)

    def data_0D(self, var_name):
        return np.array(self.data.get(var_name))[0, 0]

    def data_1D(self, var_name, op='max'):
        data = np.array(self.data.get(var_name))
        if data.shape[0] == 1:
            return data[0]          # get first column
        elif data.shape[1] == 1:
            return data.T[0]        # transpose and get first column
        elif data.shape[0] == self.t.shape[0]:
            if op == 'min':
                return data.min(axis=1)
            elif op == 'max':
                return data.max(axis=1)
        elif data.shape[1] == self.t.shape[0]:
            if op == 'min':
                return data.min(axis=0)
            elif op == 'max':
                return data.max(axis=0)
            elif type(op) is dict:
                if 'c' in op.keys():
                    return data[op['c']]
                elif 'cs' in op.keys():
                    HalfTurnToCoilSection = np.where(np.array(self.data.get('HalfTurnToCoilSection')).T[0]==op['cs'])
                    if op['op'] == 'max':
                        return data[HalfTurnToCoilSection].max(axis=0)
                    elif op['op'] == 'min':
                        return data[HalfTurnToCoilSection].min(axis=0)
        else:
            raise Exception('Can not get such data')

    def data_2D(self, var_name):
        return np.array(self.data.get(var_name))

    def __save_plot_json(self):

        plt1D_var_arr_el = [
            {'1': {'data': 'Ia', 'l_l': 'I_coil', 'l_u': 'A', 'sig_scl': 1, 'op': 'max', 'c': 'red', 'kpl': False, 'ax2': False},
            '2': {'data': 'U_CoilSections', 'l_l': 'U_coil_term.', 'l_u': 'V', 'sig_scl': 1, 'op': 'max', 'c': 'green', 'kpl': False, 'ax2': True},
            '3': {'data': 'Uground_half_turns', 'l_l': 'U_gnd_max', 'l_u': 'V', 'sig_scl': 1, 'op': 'max', 'c': 'royalblue', 'kpl': True, 'ax2': True},
            '4': {'data': 'Uground_half_turns', 'l_l': 'U_gnd_min', 'l_u': 'V', 'sig_scl': 1, 'op': 'min', 'c': 'magenta', 'kpl': True, 'ax2': True}}]
        plt1D_var_arr_th = [
            {'1': {'data': 'T_ht', 'l_l': 'Temperature', 'l_u': 'K', 'sig_scl': 1, 'op': 'max', 'c': 'darkorange', 'kpl': False, 'ax2': False},
            '2': {'data': 'R_CoilSections', 'l_l': 'Resistance', 'l_u': 'Ohm', 'sig_scl': 1, 'op': 'max', 'c': 'black', 'kpl': False, 'ax2': True}}]
        plt2D_var_arr_th = [{'1': {'data': 'T_ht', 'l_l': 'T', 'l_u': 'K', 'sig_scl': 1}}]
        plt2D_var_arr_el = [{'1': {'data': 'Uground_half_turns', 'l_l': 'U_gnd', 'l_u': 'V', 'sig_scl': 1}}]
        plt1D_var_arr = plt1D_var_arr_el + plt1D_var_arr_th
        plt2D_var_arr = plt2D_var_arr_th + plt2D_var_arr_el
        with open('plot.1D_LEDET.json', 'w') as fp:
            json.dump(plt1D_var_arr, fp)
        with open('plot.2D_LEDET.json', 'w') as fp:
            json.dump(plt2D_var_arr, fp)

    def power_for_R(self, resistance):
        R_val = self.data_1D(resistance)
        current = self.data_1D('I_CoilSections')
        t_PC = self.data_1D('t_PC')
        tEE = self.data_0D('tEE')
        if resistance == 'R_CoilSections':
            Pif_tot = self.data_1D('Pif_tot')
            return Pif_tot + R_val * current ** 2
        elif resistance == 'R_crowbar':
            current[self.t < t_PC] = 0
            P_Ud = self.data_1D('Ud') * current
            return P_Ud + R_val * current ** 2
        elif resistance == 'R_circuit':
            current[self.t < t_PC] = 0
        elif resistance =='R_EE':
            current[self.t < tEE] = 0
        return R_val * current ** 2

    def get_dt(self):
        dt = np.diff(self.t)
        return np.append(dt, dt[-1])

    def energy_for_R(self, resistance):
        dt = self.get_dt()
        return np.cumsum(self.power_for_R(resistance) * dt) * self.E_unit_multip

    def __animate(self, frame):
        frame = frame*self.every_frame
        for i, (line, line_dict, ax) in enumerate(zip(self.lines, self.lines_dict, self.subaxs1D)):
            time_data = self.t[:frame]
            time = self.t[frame]
            var_data = self.lines_data[i][:frame]
            var = self.lines_data[i][frame]
            line[0].set_data(time_data, var_data)
            if line_dict['kpl'] == True:
                prev_lab = label + ", "
            else:
                prev_lab = ""
            label = f"{prev_lab}{line_dict['l_l']}: {var:.2f} {line_dict['l_u']}"
            ax.set_ylabel(f"{label}", size=self.font_size)
            ax.set_xlabel(f"time: {time:.3f} s", size=self.font_size)
        for i, (patch, patch_dict, ax) in enumerate(zip(self.patches, self.patches_dict, self.axs2D)):
            var_data = self.patches_data[i][:, frame]
            patch.set_array(var_data)
            patch.set_clim([np.min(var_data), np.max(var_data)])
            ax.set_title(f"{patch_dict['l_l']}$_{{min}}$: {np.min(var_data) :.0f} {patch_dict['l_u']}, {patch_dict['l_l']}$_{{max}}$: {np.max(var_data) :.0f} {patch_dict['l_u']}", size=self.font_size)#, y=0, pad=-65)

    def plot_U_CoilSections(self):
        fig, ax = plt.subplots()
        U_CoilSections = self.data_1D('U_CoilSections')
        t_PC = self.data_1D('t_PC')
        U_CoilSections[self.t > t_PC] = 0
        ax.set_xlim(np.min(self.t), t_PC)
        ax.set_ylim(0, np.max(U_CoilSections))
        ax.plot(self.t, U_CoilSections)
        plt.show()

    def plot_electrical_order(self, save=False):
        X_MAG = np.array(self.data.get('XY_MAG'))[0]
        Y_MAG = np.array(self.data.get('XY_MAG'))[1]
        hBare = np.array(self.data.get('hBare'))[0, 0]*1000
        wBare = np.array(self.data.get('wBare'))[0, 0]*1000
        X_MAG = np.array([x + wBare/2 for x in X_MAG])
        Y_MAG = np.array([y + hBare / 2 for y in Y_MAG])
        el_order_half_turns_Array = np.int_(list(self.data_1D('el_order_half_turns')))
        X_MAG = X_MAG[el_order_half_turns_Array - 1]
        Y_MAG = Y_MAG[el_order_half_turns_Array - 1]
        fig, ax = plt.subplots()
        ax.set_xlabel(f"Radial position (mm)")
        ax.set_ylabel(f"Axial position (mm)")
        ax.plot(X_MAG, Y_MAG, 'k')
        ax.set_title(f'Electrical order: {self.magnet_name}')
        plt.tight_layout()
        if save:
            fig.savefig(os.path.join(self.output_folder, f'{self.magnet_name}_{self.model_no}-el_order.png'))
        else:
            plt.show()

    def _e_b_l(self, elem_name):
        I_CoilSections = self.data_1D('I_CoilSections')
        L_mag_I = self.data_1D('L_mag_I')
        E = I_CoilSections * I_CoilSections * L_mag_I / 2
        E_tot = max(E) * self.E_unit_multip
        E_max_elem = np.max(self.energy_for_R(elem_name))
        return f"{E_max_elem:.1f}kJ, { E_max_elem/ E_tot * 100:.1f}%"

    def plot_energy_balance(self, save=False):
        fig, ax = plt.subplots()
        I_CoilSections = self.data_1D('I_CoilSections')
        L_mag_I = self.data_1D('L_mag_I')
        E = I_CoilSections * I_CoilSections * L_mag_I / 2
        E_tot = max(E) * self.E_unit_multip
        Q_CoilSections = self.energy_for_R('R_CoilSections')
        Q_EE = self.energy_for_R('R_EE') + Q_CoilSections
        Q_crowbar = self.energy_for_R('R_crowbar') + Q_EE
        Q_circuit = self.energy_for_R('R_circuit') + Q_crowbar
        ax.fill_between(self.t, Q_crowbar, Q_circuit, facecolor='red', label=f"{self._e_b_l('R_circuit')} - Warm")
        ax.fill_between(self.t, Q_EE, Q_crowbar, facecolor='green', label=f"{self._e_b_l('R_crowbar')} - Crowbar")
        if np.sum(self.energy_for_R('R_EE')) != 0:
            ax.fill_between(self.t, Q_CoilSections, Q_EE, facecolor='blue', label=f"{self._e_b_l('R_EE')} - EE")
        ax.fill_between(self.t, Q_CoilSections, facecolor='orange', label=f"{self._e_b_l('R_CoilSections')} - Coils")
        ax.plot((np.min(self.t), np.max(self.t)), (E_tot, E_tot), label=f'{E_tot:.1f}kJ, 100 % - Initial Energy')
        ax.legend(loc='lower right', facecolor='white')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Energy (kJ)')
        ax.set_xlim(np.min(self.t), np.max(self.t))
        bottom, top = ax.get_ylim()
        ax.set_ylim(0, top)
        ax2 = ax.twinx()
        ax2.set_ylabel('Energy (%)')
        ax2.set_ylim(0, top/E_tot*100)
        #ax2.yaxis.set_ticks(np.arange(0, top/E_tot*100, 10))
        ax.set_title(f'{self.magnet_name}')
        plt.tight_layout()
        if save:
            fig.savefig(os.path.join(self.output_folder, f'{self.magnet_name}_{self.model_no}-energy.jpg'))
        else:
            plt.show()

    def plot_temperature(self):
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(16, 8))
        X_MAG_strand_order = np.array(self.data.get('XY_MAG'))[1]
        Y_MAG_strand_order = np.array(self.data.get('XY_MAG'))[0]
        wBare = np.array(self.data.get('hBare'))[0, 0]*1000
        hBare = np.array(self.data.get('wBare'))[0, 0]*1000
        patch = [mpatches.FancyBboxPatch([x - wBare / 2, y - hBare / 2], wBare, hBare,
                                                           boxstyle=mpatches.BoxStyle("round", pad=0.0, rounding_size=0.3)) for
                        x, y in zip(X_MAG_strand_order, Y_MAG_strand_order)]

        patches = ax.add_collection(UpdatablePatchCollection(patch, cmap=cm.jet, alpha=1))
        var_val = self.data_2D('T_ht')
        patches.set_array(var_val[:, -1])
        #patches.set_clim([np.min(var_val), np.max(var_val)])
        cax = make_axes_locatable(ax).append_axes('right', size='5%', pad=0.05)
        cbar = fig.colorbar(patches, cax=cax, orientation='vertical')
        ax.set_xlim(np.min(X_MAG_strand_order) - wBare / 2, np.max(X_MAG_strand_order) + wBare / 2)
        ax.set_ylim(np.min(Y_MAG_strand_order) - hBare / 2, np.max(Y_MAG_strand_order) + hBare / 2)
        plt.show()

    def animation(self, plt1D_var_arr, plt2D_var_arr, postfix="", video=False, save=False):
        self.plt1D_var_arr = plt1D_var_arr
        fig, axs = plt.subplots(nrows=1, ncols=len(plt1D_var_arr + plt2D_var_arr), figsize=(18, 11))
        if len(plt1D_var_arr + plt2D_var_arr) == 1:
            self.axs=[self.axs]
        X_MAG_strand_order = np.array(self.data.get('XY_MAG'))[0]
        Y_MAG_strand_order = np.array(self.data.get('XY_MAG'))[1]
        el_order_half_turns_Array = np.int_(list(self.data_1D('el_order_half_turns')))
        X_MAG_electrical_order = X_MAG_strand_order[el_order_half_turns_Array - 1]
        Y_MAG_electrical_order = Y_MAG_strand_order[el_order_half_turns_Array - 1]
        hBare = np.array(self.data.get('hBare'))[0, 0]*1000
        wBare = np.array(self.data.get('wBare'))[0, 0]*1000
        self.patch_strand_order = [mpatches.FancyBboxPatch([x - wBare / 2, y - hBare / 2], wBare, hBare,
                                                           boxstyle=mpatches.BoxStyle("round", pad=0.0, rounding_size=0.3)) for
                        x, y in zip(X_MAG_strand_order, Y_MAG_strand_order)]
        self.patch_electrical_order = [mpatches.FancyBboxPatch([x - wBare / 2, y - hBare / 2], wBare, hBare,
                                                           boxstyle=mpatches.BoxStyle("round", pad=0.0, rounding_size=0.3)) for
                        x, y in zip(X_MAG_electrical_order, Y_MAG_electrical_order)]
        self.axs1D = axs[:len(plt1D_var_arr)]
        self.axs2D = axs[len(plt1D_var_arr):]
        self.subaxs1D = []
        for ax, var_def in zip(self.axs1D, plt1D_var_arr):
            ax2_exist = False
            for var_key, var_dict in var_def.items():
                #print(f"Name:{var_dict['data']}, OP:{var_dict['op']}, SC:{var_dict['sig_scl']}")
                var_data = self.data_1D(var_dict['data'], var_dict['op']) * var_dict['sig_scl']
                self.lines_data.append(var_data)
                self.lines_dict.append(var_dict)
                if var_dict['kpl'] == True:
                    prev_lab = label + ", "
                else:
                    prev_lab = ""
                label = f"{prev_lab}{var_dict['l_l']} ({var_dict['l_u']})"
                if var_dict['ax2']:
                    if ax2_exist == False:
                        ax2 = ax.twinx()
                        ax2_exist = True
                    line = ax2.plot(self.t, var_data, lw=self.line_width, color=var_dict['c'], label=var_dict['l_l'])
                    ax2.legend(loc='upper right', facecolor='white')
                    ax2.set_ylabel(f"{label}", size=self.font_size)
                    self.subaxs1D.append(ax2)
                else:
                    ax2_exist = False
                    line = ax.plot(self.t, var_data, lw=self.line_width, color=var_dict['c'], label=var_dict['l_l'])
                    ax.legend(loc='upper left', facecolor='white')
                    ax.set_ylabel(f"{label}", size=self.font_size)
                    self.subaxs1D.append(ax)
                self.lines.append(line)
            ax.set_xlabel('Time (s)', size=self.font_size)
            #ax.set_xlim(np.min(self.t), np.max(self.t))
            ax.set_xlim(-0.1, 5)
        ax.set_title(f'{self.magnet_name}')     # Last 2D axis to have title
        for ax, var_def in zip(self.axs2D, plt2D_var_arr):
            for var_key, var_dict in var_def.items():
                self.patches_dict.append(var_dict)
                var_val = self.data_2D(var_dict['data']) * var_dict['sig_scl']
                self.patches_data.append(var_val)
                if var_dict['data'] == 'Uground_half_turns':
                    patch = self.patch_electrical_order
                    ax.plot(X_MAG_electrical_order, Y_MAG_electrical_order, 'k', linewidth=0.8)
                else:
                    patch = self.patch_strand_order
                patches = ax.add_collection(UpdatablePatchCollection(patch, cmap=cm.CMRmap, alpha=1)) #cm.gnuplot
                self.patches.append(patches)
                cax = make_axes_locatable(ax).append_axes('right', size='5%', pad=0.05)
                cbar = fig.colorbar(patches, cax=cax, orientation='vertical')
                #cbar.set_label(f"{var_dict['l_n']} ({var_dict['l_u']})")
                ax.set_xlim(np.min(X_MAG_strand_order) - wBare / 2, np.max(X_MAG_strand_order) + wBare / 2)
                ax.set_ylim(np.min(Y_MAG_strand_order) - hBare / 2, np.max(Y_MAG_strand_order) + hBare / 2)
                ax.set_xlabel(f"Radial position (mm)", size=self.font_size)
                ax.set_ylabel(f"Axial position (mm)", size=self.font_size)
                ax.tick_params(labelsize=self.font_size)
                #ax.set_axis_off()
                diff = np.array([np.max(var_val[:, i]) + np.abs(np.min(var_val[:, i])) for i in range(np.shape(var_val)[1])])
                time_idx = int(np.where(diff == np.max(diff))[0][0])
                patches.set_array(var_val[:, time_idx])
                patches.set_clim([np.min(var_val[:, time_idx]), np.max(var_val[:, time_idx])])
                if var_dict['data'] == 'Uground_half_turns':
                    ax.set_title(f"{var_dict['l_l']}$_{{min}}$={np.min(var_val):.1f} {var_dict['l_u']}, {var_dict['l_l']}$_{{max}}$={np.max(var_val):.1f} {var_dict['l_u']} @ {self.t[time_idx]:.3f}s", size=self.font_size)
                else:
                    ax.set_title(f"{var_dict['l_l']}$_{{max}}$={np.max(var_val):.1f} {var_dict['l_u']} @ {self.t[time_idx]:.3f} s", size=self.font_size)
        self.every_frame = 10
        self.size = fig.get_size_inches() * fig.dpi  # get fig size in pixels
        plt.tight_layout()
        if save:
            fig.savefig(os.path.join(self.output_folder, f'{self.magnet_name}_{self.model_no}-{postfix}-2D.svg'))
            if video:
                anim = anm.FuncAnimation(fig, self.__animate, frames=int(len(self.t) / self.every_frame), interval=100, blit=False)
                writervideo = anm.FFMpegWriter(fps=10, extra_args=['-b:v', '300k'])  # this enables havc h.256 encoding: extra_args=['-vcodec', 'libx265'])
                anim.save(os.path.join(self.output_folder, f'{self.magnet_name}_{self.model_no}-{postfix}.mp4'),
                          writer=writervideo)
            # anim.save(os.path.join(self.output_folder, f'{self.magnet_name}_{self.model_no}-summary.gif'), fps=5, dpi=100, writer='imagemagick')

            # with open(os.path.join(self.output_folder, f"{self.magnet_name}_{self.model_no}-{postfix}.html"), "w") as f:
            #     print(anim.to_html5_video(), file=f)
        else:
            plt.show()

    def plot_results(self, video=False, save=False, _1D_var='plot.1D_LEDET.json',_2D_var='plot.2D_LEDET.json', **kwargs):
        print(f"Post processing {self.magnet_name} {self.model_no}")
        if 'json_path' in kwargs:
            json_path = kwargs['json_path']
            _1D_var = os.path.join(json_path, _1D_var)
            _2D_var = os.path.join(json_path, _2D_var)
        # p = Plot_results(self.magnet, self.number, self.LEDET_folder)
        # p = Plot_results(self)
        with open(_1D_var, 'r') as fp:
            plt1D_var_arr = json.load(fp)
        with open(_2D_var, 'r') as fp:
            plt2D_var_arr = json.load(fp)
        self.animation(plt1D_var_arr, plt2D_var_arr, postfix="summary", video=video, save=save)

    def calc_timing(self, print_timing=False):
        # d = Postpro_LEDET(self.magnet, self.number, self.LEDET_folder)
        initial_path = os.getcwd()
        if self.magnet_inputs_path != '':
            os.chdir(self.magnet_inputs_path)
        mag_dict = read_yaml('circuit', self.magnet_name)
        os.chdir(initial_path)
        self.det_thresh = mag_dict['det_thresh']
        self.det_time = mag_dict['det_time']
        # v_pt_ats = d.data_2D('Uturn_half_turns_resistive')   # voltage per turn at time steps
        vm_ats = np.sum(self.data_2D('Uturn_half_turns_resistive'), axis=0)                       # voltage magnet at time steps
        try:
            self.idx_V = next(x[0] for x in enumerate(vm_ats) if x[1] > self.det_thresh)      # index when threshold is exceeded
            self.t_th_ex = self.t[self.idx_V]   # time when threshold is exceeded
            self.v_t_th_ex = vm_ats[self.idx_V]  # voltage at time when threshold is exceeded
            self.t_PC_calc = self.t_th_ex + self.det_time  # time when PC is off
        except:
            self.t_PC_calc = mag_dict['t_pre_calc']
            print("Pre simulation was run for too short time and magnet has not developed enough voltage to trigger protection"
                  f"The pre simulation ime {mag_dict['t_pre_calc']}s is used instead!!!!")
        if print_timing:
            print(f'Detection threshold of {self.det_thresh} V was exceeded at {self.t_th_ex} s.\nDetermination time {self.det_time}s results in calculated t_PC of {self.t_PC_calc} s.')
        return self.t_PC_calc

    def plot_timing(self):
        self.calc_timing()
        fig, ax = plt.subplots()
        trim = next(x[0] for x in enumerate(self.t) if x[1] > self.data_1D('t_PC')*1.3)  # index when t_PC is exceeded by 130%
        t = self.t[:trim]
        i = self.data_1D('Ia')[:trim]
        V = np.sum(self.data_2D('Uturn_half_turns_resistive'), axis=0)[:trim]
        ax.plot(t, V, marker='d', label='Resistive voltage')
        idx_v_at_t_PC = next(x[0] for x in enumerate(self.t) if x[1] > self.data_1D('t_PC'))
        v_at_t_PC = V[idx_v_at_t_PC]
        ax.plot([np.min(t), np.max(t)], [self.det_thresh, self.det_thresh], label='Detection threshold')
        ax.plot([self.t_th_ex, self.t_th_ex], [np.min(V), np.max(V)], marker='', label='Threshold exceeded')
        ax.plot([self.t_PC_calc, self.t_PC_calc], [np.min(V), np.max(V)], marker='', label='t_PC calculated')
        ax2 = ax.twinx()
        ax2.plot(t, i, c='red', label='Current')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Voltage (V)')
        ax2.set_ylabel('Current (A)')
        ax.set_ylim(np.min(V), v_at_t_PC*1.3)
        lines, labels = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines + lines2, labels + labels2, loc='center left')
        plt.tight_layout()
        plt.show()

    def MIITs(self):
        I = self.data_1D('Ia')
        dt = self.get_dt()
        return np.sum(I*I*dt)

    def key_results(self):
        peak_T = np.max(self.data_2D('T_ht'))
        Uground_min = np.min(self.data_2D('Uground_half_turns'))
        Uground_max = np.max(self.data_2D('Uground_half_turns'))
        Utermin_min = np.min(self.data_2D('U_CoilSections'))
        Utermin_max = np.max(self.data_2D('U_CoilSections'))
        MIITs = self.MIITs()
        I_end = self.data_1D('Ia')[-1]
        L_mag0 = self.data_0D('L_mag0')
        R_EE_triggered = self.data_0D('R_EE_triggered')
        R_CoilSections = np.max(self.data_1D('R_CoilSections'))
        t_PC = self.data_0D('t_PC')
        Q_CoilSections = np.max(self.energy_for_R('R_CoilSections'))
        Q_EE = np.max(self.energy_for_R('R_EE'))
        Q_crowbar = np.max(self.energy_for_R('R_crowbar'))
        Q_circuit = np.max(self.energy_for_R('R_circuit'))
        Q_total = Q_CoilSections + Q_EE + Q_crowbar + Q_circuit
        wIns_inGroup_min = np.min(self.data_1D('wIns_inGroup'))
        wIns_inGroup_max = np.max(self.data_1D('wIns_inGroup'))
        hIns_inGroup_min = np.min(self.data_1D('hIns_inGroup'))
        hIns_inGroup_max = np.max(self.data_1D('hIns_inGroup'))
        return {'peak_T': peak_T,
                'Uground_min': Uground_min,
                'Uground_max': Uground_max,
                'Utermin_min': Utermin_min,
                'Utermin_max': Utermin_max,
                'MIITs': MIITs,
                'I_end': I_end,
                'L_mag0': L_mag0,
                'R_EE_triggered': R_EE_triggered,
                'R_CoilSections': R_CoilSections,
                't_PC': t_PC,
                'Q_CoilSections': Q_CoilSections,
                'Q_EE': Q_EE,
                'Q_crowbar': Q_crowbar,
                'Q_circuit': Q_circuit,
                'Q_total': Q_total,
                'wIns_inGroup_min': wIns_inGroup_min,
                'wIns_inGroup_max': wIns_inGroup_max,
                'hIns_inGroup_min': hIns_inGroup_min,
                'hIns_inGroup_max': hIns_inGroup_max}

    def save_key_vectors(self):
        df = pd.DataFrame({"Time (s)": self.t,
                           "I (A)": self.data_1D('Ia'),
                           "T_peak (K)": self.data_1D('T_ht'),
                           "U ground max (V)": self.data_1D('Uground_half_turns', op='max'),
                           "U ground min (V)": self.data_1D('Uground_half_turns', op='min'),
                           "U terminals (V)": self.data_1D('U_CoilSections'),
                           "U resistive (V)": np.sum(self.data_2D('Uturn_half_turns_resistive'), axis=0),
                           "R_CoilSections (Ohm)": self.data_1D('R_CoilSections')})
        precision = {"Time (s)": '%.6f',
                     "I (A)": '%.2f',
                     "T_peak (K)": '%.1f',
                     "U ground max (V)": '%.3f',
                     "U ground min (V)": '%.3f',
                     "U terminals (V)": '%.3f',
                     "U resistive (V)": '%.5f',
                     "R_CoilSections (Ohm)": '%.6f'}
        for column in df:
            df[column] = df[column].map(lambda x: precision[column] % x)
        df.to_csv(f'{self.magnet_name} {self.model_no}.dat', index=False, sep='\t')#, float_format='%.7f')

    def save_key_results(self):
        data = self.key_results()
        json.dump(data, open(os.path.join(self.output_folder, f'{self.magnet_name} {self.model_no}.json'), 'w'))
        print(f'Circuit: {self.magnet_name} {self.model_no} -> {data}')
        with open(os.path.join(self.output_folder, f'{self.magnet_name} {self.model_no}.json'), 'w+') as f:
            json.dump(data, f, indent=4)

    def delete_mat_file(self):
        self.data.close()
        mat_file_path = f"{self.matlab_file_prefix}{self.model_no}.mat"
        if os.path.exists(mat_file_path):
            os.remove(mat_file_path)
        print(f"Deleted {mat_file_path}")

if __name__ == "__main__":

    LEDET_folder_path= r"D:\LEDET\LEDET_v2_01_36"
    magnets = ['RLEA', 'RLEB', 'RLEC', 'RLEG', 'RLEM']#, 'RLEMnoEE']
    magnets = ['RLEM']
    #magnets = ['RLEMnoEE']
    # numbers = [1, 3395, 20437]
    numbers = [1]
    #
    for number in numbers:
        for magnet in magnets:
            print(f"Post processing {magnet} {number}")
            p = Post_LEDET(magnet, number, LEDET_folder_path)
            #p.save_key_vectors()
            #p.key_results()
            with open(r'E:\Python\HEL_Q\plot.1D_LEDET.json', 'r') as fp:
                plt1D_var_arr = json.load(fp)
            with open(r'E:\Python\HEL_Q\plot.2D_LEDET.json', 'r') as fp:
                plt2D_var_arr = json.load(fp)
            p.animation(plt1D_var_arr, plt2D_var_arr, postfix="summary", video=False, save=True)
    #         p.plot_trigger()


