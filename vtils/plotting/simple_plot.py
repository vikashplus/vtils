import matplotlib as mpl

import warnings
warnings.filterwarnings("ignore",category=UserWarning)  #to suppress: MatplotlibDeprecationWarning: Adding an axes using the same arguments as a previous axes currently reuses the earlier instance.  In a future version, a new instance will always be created and returned.  Meanwhile, this warning can be suppressed, and the future behavior ensured, by passing a unique label to each axes instance.

mpl.use('TkAgg')
import matplotlib.pyplot as plt
from typing import Optional, Tuple
import seaborn as sns
sns.set()

def plot(xdata, ydata=None, errdata=None, errmin=None, errmax=None,
    legend:Optional[str]=None,
    legend_size:Optional[str]=8,
    xaxislabel:Optional[str]=None,
    yaxislabel:Optional[str]=None,
    xaxislimit:Optional[Tuple[float]]=None,
    yaxislimit:Optional[Tuple[float]]=None,
    xaxisscale:Optional[str]="linear", #"linear", "log", "symlog", "logit"
    yaxisscale:Optional[str]="linear", #"linear", "log", "symlog", "logit"
    subplot_id:Optional[Tuple[int]] = (1,1,1),
    plot_name:Optional[str]=None,
    fig_name:Optional[str]=None,
    fig_size:Optional[Tuple[int]]=(8,6),
    marker:Optional[str]=None,
    marker_size:Optional[int]=5,
    linestyle:Optional[str]='-',
    linewidth:Optional[int]=2,
    alpha:Optional[int]=1,
    reset_color_cycle:Optional[bool]=False,
    color:Optional[any]=None
    ):

    # get figure
    if fig_name:
        h_fig = plt.figure(fig_name, figsize=fig_size)
    else:
        h_fig = plt.figure(figsize=fig_size)

    # recover/add axis
    if len(h_fig.axes)>=subplot_id[2]:
        h_axis = h_fig.axes[subplot_id[2]-1]
    else:
        h_axis = h_fig.add_subplot(subplot_id[0], subplot_id[1], subplot_id[2],
            label='{}{}{}'.format(subplot_id[0],subplot_id[1],subplot_id[2]))

    if reset_color_cycle:
        h_axis.set_prop_cycle(None)

    # plot
    if ydata is None:
        h_plot = plt.plot(xdata, label=legend, marker=marker, markersize=marker_size, linestyle=linestyle, linewidth=linewidth, color=color, alpha=alpha)
    else:
        h_plot = plt.plot(xdata, ydata, label=legend, marker=marker, markersize=marker_size, linestyle=linestyle, linewidth=linewidth, color=color, alpha=alpha)

    # bands
    if errdata is not None: # error graph
        h_axis.fill_between(xdata, ydata-errdata, ydata+errdata, markersize=marker_size, linestyle=linestyle, linewidth=linewidth, color=color, alpha=alpha)
    elif errmin is not None and errmax is not None:
        h_axis.fill_between(xdata, errmin, errmax, alpha=0.3, linewidth=0)

    # texts
    h_axis.set_xlabel(xaxislabel)
    h_axis.set_ylabel(yaxislabel)
    h_axis.set_title(plot_name)
    h_axis.legend()
    h_axis.set_xscale(xaxisscale)
    h_axis.set_yscale(yaxisscale)

    # limits
    if xaxislimit:
        h_axis.set_xlim(xaxislimit)
    if yaxislimit:
        h_axis.set_ylim(yaxislimit)

    # finalize
    plt.tight_layout()
    plt.rc('legend',fontsize=legend_size)
    return h_fig, h_axis, h_plot

def show_plot():
    plt.show()

def save_plot(name, fig_handle=None):
    if fig_handle:
        fig_handle.savefig(name)
    else:
        plt.savefig(name)
    print("Saved: "+name)


def bar(xdata, ydata=None,
    errdata=None,
    # errmin=None, errmax=None,
    legend:Optional[str]=None,
    legend_size:Optional[str]=8,
    xaxislabel:Optional[str]=None,
    yaxislabel:Optional[str]=None,
    xticklabels:Optional[str]=None,
    xtickrotation:Optional[int]=90,
    xaxislimit:Optional[Tuple[float]]=None,
    yaxislimit:Optional[Tuple[float]]=None,
    xaxisscale:Optional[str]="linear", #"linear", "log", "symlog", "logit"
    yaxisscale:Optional[str]="linear", #"linear", "log", "symlog", "logit"
    subplot_id:Optional[Tuple[int]] = (1,1,1),
    plot_name:Optional[str]=None,
    fig_name:Optional[str]=None,
    fig_size:Optional[Tuple[int]]=(8,6),
    # marker:Optional[str]=None,
    # marker_size:Optional[int]=5,
    # linestyle:Optional[str]='-',
    width:Optional[int]=.25,
    # alpha:Optional[int]=1,
    reset_color_cycle:Optional[bool]=False,
    # color:Optional=None
    ):

    # get figure
    if fig_name:
        h_fig = plt.figure(fig_name, figsize=fig_size)
    else:
        h_fig = plt.figure(figsize=fig_size)

    # # get axis
    # h_axis = h_fig.add_subplot(subplot_id[0], subplot_id[1], subplot_id[2],
    #     label='{}{}{}'.format(subplot_id[0],subplot_id[1],subplot_id[2]))

    # recover/add axis
    if len(h_fig.axes)>=subplot_id[2]:
        h_axis = h_fig.axes[subplot_id[2]-1]
    else:
        h_axis = h_fig.add_subplot(subplot_id[0], subplot_id[1], subplot_id[2],
            label='{}{}{}'.format(subplot_id[0],subplot_id[1],subplot_id[2]))

    if ydata is None:
        xind = np.arange(len(xdata)) + 0.1*len(h_axis.containers)
        h_bar = h_axis.bar(xind, xdata, width, yerr=errdata, label=legend)
        h_axis.set_xticks(ticks=xind)
    else:
        h_bar = h_axis.bar(xdata, ydata, width, yerr=errdata, label=legend)
        h_axis.set_xticks(ticks=xdata)

    if reset_color_cycle:
        h_axis.set_prop_cycle(None)

    # texts
    h_axis.set_xlabel(xaxislabel)
    h_axis.set_ylabel(yaxislabel)

    h_axis.set_title(plot_name)
    h_axis.legend()
    h_axis.set_xscale(xaxisscale)
    h_axis.set_yscale(yaxisscale)

    # limits
    if xaxislimit:
        h_axis.set_xlim(xaxislimit)
    if yaxislimit:
        h_axis.set_ylim(yaxislimit)

    if xticklabels:
        h_axis.set_xticklabels(xticklabels, rotation=xtickrotation)

    # finalize
    plt.tight_layout()
    plt.rc('legend',fontsize=legend_size)
    return h_fig, h_axis, h_bar


if __name__ == '__main__':
    n_points = 10
    import numpy as np
    data1 = np.random.uniform(size=10)
    data2 = np.random.uniform(size=10)
    data3 = np.random.uniform(size=10)

    print("Testing 2D plots")
    plot(data1, fig_name="test 2dplots", plot_name="top_plot", legend="data1", subplot_id=(2,1,1))
    plot(data2, fig_name="test 2dplots", plot_name="top_plot", legend="data2", subplot_id=(2,1,1))
    plot(data3, fig_name="test 2dplots", plot_name="top_plot", legend="data3", subplot_id=(2,1,1))

    print("Testing bar plots")
    bar(data1, fig_name="test 2dplots", legend="data1", subplot_id=(2,1,2))
    bar(data2, fig_name="test 2dplots", legend="data2", subplot_id=(2,1,2))
    bar(data3, fig_name="test 2dplots", legend="data3", subplot_id=(2,1,2))

    show_plot()
