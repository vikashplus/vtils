import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from typing import Optional, Tuple
import seaborn as sns
sns.set()

def plot(xdata, ydata=None, errdata=None,
    legend:Optional[str]=None, 
    xaxislabel:Optional[str]=None, 
    yaxislabel:Optional[str]=None,
    xaxislimit:Optional[Tuple[float]]=None,
    yaxislimit:Optional[Tuple[float]]=None,
    subplot_id:Optional[Tuple[int]] = (1,1,1),
    plot_name:Optional[str]=None,
    fig_name:Optional[str]=None,
    fig_size:Optional[Tuple[int]]=(8,6)):
    
    # get figure
    if fig_name:
        h_fig = plt.figure(fig_name, figsize=fig_size)
    else: 
        h_fig = plt.figure(figsize=fig_size)

    # get axis
    h_axis = h_fig.add_subplot(subplot_id[0], subplot_id[1], subplot_id[2], 
        label='{}{}{}'.format(subplot_id[0],subplot_id[1],subplot_id[2]))
    
    # plot
    if ydata is None:
        h_plot = plt.plot(xdata, label=legend)
    else:
        h_plot = plt.plot(xdata, ydata, label=legend)
    if errdata is not None: # error graph
        h_axis.fill_between(xdata, ydata-errdata, ydata+errdata, alpha=0.3)

    # texts
    h_axis.set_xlabel(xaxislabel)
    h_axis.set_ylabel(yaxislabel)
    h_axis.set_title(plot_name)
    h_axis.legend()

    # limits
    if xaxislimit:
        h_axis.set_xlim(xaxislimit)
    if yaxislimit:
        h_axis.set_ylim(yaxislimit)

    # finalize
    plt.tight_layout()
    return h_fig, h_axis, h_plot

def show_plot():
    plt.show()

def save_plot(name):
    plt.savefig(name)
    print("Saved: "+name)