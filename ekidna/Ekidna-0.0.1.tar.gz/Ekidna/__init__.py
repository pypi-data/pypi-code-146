def make_pretty(ax, title='', xTitle='', yTitle=''):
    ax.spines['left'].set_color('black')
    ax.spines['top'].set_color('black')
    ax.spines['bottom'].set_color('black')
    ax.spines['right'].set_color('black')

    ax.spines['left'].set_linewidth(2)
    ax.spines['top'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['right'].set_linewidth(2)
    
    ax.set_title(title, fontsize = 20)
    ax.set_xlabel(xTitle, fontsize=16)
    ax.yaxis.set_label_coords(-0.15, 0.5)
    ax.set_ylabel(yTitle, rotation = 'horizontal', fontsize = 16)
    
    ax.tick_params(axis='both', labelsize = 16)
    
    ax.grid(True)
    return