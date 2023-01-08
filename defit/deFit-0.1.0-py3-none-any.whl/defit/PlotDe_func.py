import pandas as pd
import matplotlib.pyplot as plt
def PlotDe_func(userdata,calcdata):
    plot_data = pd.merge(userdata,calcdata,left_on='time',right_on='time')
    mid_time = plot_data['time']
    mid_data = plot_data.copy()
    del mid_data['time']
    for i in mid_data.columns:
        if 'solver_' in i:
            plt.plot(plot_data['time'], plot_data.loc[:, i],label=i)
        else:
            plt.scatter(mid_time, plot_data.loc[:, i],label= i)
    # plt.scatter(plot_data['time'],plot_data.iloc[:,1])
    # plt.plot(plot_data['time'],plot_data.iloc[:,2])
    plt.legend()
    plt.show()