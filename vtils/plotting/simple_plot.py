import matplotlib as mpl

import warnings
warnings.filterwarnings("ignore",category=UserWarning)  #to suppress: MatplotlibDeprecationWarning: Adding an axes using the same arguments as a previous axes currently reuses the earlier instance.  In a future version, a new instance will always be created and returned.  Meanwhile, this warning can be suppressed, and the future behavior ensured, by passing a unique label to each axes instance.

mpl.use('TkAgg')
import matplotlib.pyplot as plt
from typing import Optional, Tuple
import seaborn as sns
import numpy as np
sns.set_theme()


def get_or_create_figure(fig_name: Optional[str] = None, fig_size: Optional[Tuple[int, int]] = (8, 6)):
    """Retrieve or create a figure based on the figure name.

    Args:
        fig_name: The name or number of the figure.
        fig_size: The size of the figure.

    Returns:
        The figure object.
    """
    if fig_name:
        # Try to retrieve the figure by name or create it if it doesn't exist
        h_fig = plt.figure(num=fig_name, figsize=fig_size)
    else:
        # Create a new figure with the specified size
        h_fig = plt.figure(figsize=fig_size)

    return h_fig


def get_or_create_axis(h_fig, subplot_id: Tuple[int, int, int]):
    """Retrieve or create an axis in the figure based on the subplot ID.

    Args:
        h_fig: The figure object.
        subplot_id: A tuple (nrows, ncols, index) specifying the subplot.

    Returns:
        The axis object corresponding to the subplot ID.
    """
    # Create a unique label for the subplot
    subplot_label = '{}{}{}'.format(subplot_id[0], subplot_id[1], subplot_id[2])

    # Check if an axis with this label already exists
    for ax in h_fig.axes:
        if ax.get_label() == subplot_label:
            return ax

    # If not found, create a new axis
    return h_fig.add_subplot(subplot_id[0], subplot_id[1], subplot_id[2], label=subplot_label)


import matplotlib.pyplot as plt
from typing import Optional, Tuple

def customize_axis(
    h_axis,
    plot_name: Optional[str] = None,
    xaxislabel: Optional[str] = None,
    yaxislabel: Optional[str] = None,
    xaxisscale: Optional[str] = None,  #"linear", "log", "symlog", "logit"
    yaxisscale: Optional[str] = None,  #"linear", "log", "symlog", "logit"
    xticks:Optional[str] = None,
    xticklabels:Optional[str]=None,
    yticks:Optional[str] = None,
    yticklabels:Optional[str]=None,
    xtickrotation:int = 0,
    xaxislimit: Optional[Tuple[float, float]] = None,
    yaxislimit: Optional[Tuple[float, float]] = None,
    border_color: Optional[str] = None,
    border_width: Optional[str] = None,
    bg_color: Optional[str] = None
):
    """Customize the axis with labels, scales, and limits.

    Args:
        h_axis: The axis object to customize.
        plot_name: Title of the plot.
        xaxislabel: Label for the x-axis.
        yaxislabel: Label for the y-axis.
        xaxisscale: Scale for the x-axis (e.g., 'linear', 'log').
        yaxisscale: Scale for the y-axis (e.g., 'linear', 'log').
        xaxislimit: Limits for the x-axis as a tuple (min, max).
        yaxislimit: Limits for the y-axis as a tuple (min, max).
    """
    # Set title and axis lable
    if plot_name:
        h_axis.set_title(plot_name)
    if xaxislabel:
        h_axis.set_xlabel(xaxislabel)
    if yaxislabel:
        h_axis.set_ylabel(yaxislabel)

    # ticks
    if xticks is not None:
        h_axis.set_xticks(xticks)
    if yticks is not None:
        h_axis.set_yticks(yticks)
    # if xticklabels is not None and len(xticklabels) == len(h_axis.get_xticks()):
    if xticklabels is not None:
        if xticklabels:
            assert len(xticklabels) == len(h_axis.get_xticks()), ValueError(f"check xticklabel's size")
        h_axis.set_xticklabels(xticklabels, rotation=xtickrotation)
    if yticklabels is not None:
        if yticklabels:
            assert len(yticklabels) == len(h_axis.get_xticks()), ValueError(f"check yticklabel's size")
        h_axis.set_yticklabels(yticklabels)

    # axis scales
    if xaxisscale:
        h_axis.set_xscale(xaxisscale)
    if yaxisscale:
        h_axis.set_yscale(yaxisscale)

    # axis limits
    if xaxislimit:
        h_axis.set_xlim(xaxislimit)
    if yaxislimit:
        h_axis.set_ylim(yaxislimit)

    # Add a border to the axis
    if border_color is not None or border_width is not None:
        for spine in h_axis.spines.values():
            if border_color:
                spine.set_edgecolor(border_color)
            if border_width:
                spine.set_linewidth(border_width)

    # Set the background color
    if bg_color:
        h_axis.set_facecolor(bg_color)



def plot(xdata, ydata=None, errdata=None, errmin=None, errmax=None,
    legend:Optional[str]=None,
    legend_size:Optional[str]=8,
    subplot_id:Optional[Tuple[int]] = (1,1,1),
    fig_name:Optional[str]=None,
    fig_size:Optional[Tuple[int]]=(8,6),
    marker:Optional[str]=None,
    marker_size:Optional[int]=5,
    linestyle:Optional[str]='-',
    linewidth:Optional[int]=2,
    alpha:Optional[int]=1,
    reset_color_cycle:Optional[bool]=False,
    color:Optional[any]=None,
    **kwargs,
    ):

    # get figure
    h_fig = get_or_create_figure(fig_name, fig_size=fig_size)

    # recover/add axis
    h_axis = get_or_create_axis(h_fig, subplot_id)

    if reset_color_cycle:
        h_axis.set_prop_cycle(None)

    # plot
    if ydata is None:
        h_plot = h_axis.plot(xdata, label=legend, marker=marker, markersize=marker_size, linestyle=linestyle, linewidth=linewidth, color=color, alpha=alpha)
    else:
        h_plot = h_axis.plot(xdata, ydata, label=legend, marker=marker, markersize=marker_size, linestyle=linestyle, linewidth=linewidth, color=color, alpha=alpha)

    # bands
    if errdata is not None: # error graph
        h_axis.fill_between(xdata, ydata-errdata, ydata+errdata, markersize=marker_size, linestyle=linestyle, linewidth=linewidth, color=color, alpha=alpha)
    elif errmin is not None and errmax is not None:
        h_axis.fill_between(xdata, errmin, errmax, alpha=0.3, linewidth=0)

    # process axis
    customize_axis(h_axis, **kwargs)
    # Show legends
    h_axis.legend()

    # finalize
    plt.tight_layout()
    plt.rc('legend',fontsize=legend_size)
    return h_fig, h_axis, h_plot


def show_plot():
    plt.show()


# def save_plot(name, fig_handle=None):
#     if fig_handle:
#         fig_handle.savefig(name)
#     else:
#         plt.savefig(name)
#     print("Saved: "+name)

def save_plot(name, fig_handle=None, hspace=0.5, wspace=0.3):
    """Save the plot with adjusted subplot spacing.

    Args:
        name: The filename to save the plot as.
        fig_handle: The figure handle to save. If None, saves the current figure.
        hspace: The height space between rows of subplots.
        wspace: The width space between columns of subplots.
    """
    if fig_handle:
        fig_handle.subplots_adjust(hspace=hspace, wspace=wspace)
        fig_handle.savefig(name)
    else:
        plt.subplots_adjust(hspace=hspace, wspace=wspace)
        plt.savefig(name)
    print("Saved: " + name)


def bar(xdata,
    height=None,
    bottom=None, # bottom side(s) of the bars.
    errdata=None,
    # errmin=None, errmax=None,
    legend:Optional[str]=None,
    legend_size:Optional[str]=8,
    subplot_id:Optional[Tuple[int]] = (1,1,1),
    fig_name:Optional[str]=None,
    fig_size:Optional[Tuple[int]]=(8,6),
    width:Optional[int]=.25,
    # alpha:Optional[int]=1,
    reset_color_cycle:Optional[bool]=False,
    color:Optional=None,
    **kwargs
    ):

    # get figure
    h_fig = get_or_create_figure(fig_name, fig_size=fig_size)

    # recover/add axis
    h_axis = get_or_create_axis(h_fig, subplot_id)

    # resolve x and y data
    if height is None:
        height = xdata
        xdata = np.arange(len(xdata)) + 0.1*len(h_axis.containers)

    assert len(xdata) == len(height), ValueError("xdata and height must have the same length")
    if bottom is not None:
        assert len(bottom) == len(height), ValueError("xdata and height must have the same length")

    h_bar = h_axis.bar(x=xdata, height=height, width=width, bottom=bottom, yerr=errdata, label=legend, color=color)

    # color cycle
    if reset_color_cycle:
        h_axis.set_prop_cycle(None)

    # fix axis
    customize_axis(h_axis, **kwargs)

    # Show legends
    h_axis.legend()

    # finalize
    plt.tight_layout()
    plt.rc('legend',fontsize=legend_size)
    return h_fig, h_axis, h_bar


def text(positions,
        texts,
        subplot_id: Optional[Tuple[int, int, int]] = (1, 1, 1),
        fig_name: Optional[str] = None,
        fig_size: Optional[Tuple[int, int]] = (8, 6),
        fontsize=12,
        color='black',
        ha='center',
        va='center',
        border_color='lightgrey',
        **kwargs
        ):
    """
    Adds multiple text annotations to a specified subplot.

    Parameters:
    - positions: A list of (x, y) tuples for text positions.
    - texts: A list of text strings to add.
    - subplot_id: Tuple indicating the subplot configuration (nrows, ncols, index).
    - fig_name: Optional name for the figure.
    - fig_size: Size of the figure (width, height).
    - fontsize: The font size of the text.
    - color: The color of the text.
    - ha: Horizontal alignment of the text ('center', 'left', 'right').
    - va: Vertical alignment of the text ('center', 'top', 'bottom', 'baseline').
    """
    # get figure
    h_fig = get_or_create_figure(fig_name, fig_size=fig_size)

    # recover/add axis
    h_axis = get_or_create_axis(h_fig, subplot_id)

    # Add text to the specified subplot
    for (x, y), text in zip(positions, texts):
        h_text = h_axis.text(x, y, text, fontsize=fontsize, color=color, ha=ha, va=va)

    # fix axis
    customize_axis(h_axis, border_color=border_color, xticks=[], yticks=[], **kwargs)

    return h_fig, h_axis, h_text





if __name__ == '__main__':
    n_points = 10
    n_splts = 4
    import numpy as np
    data1 = -1*np.random.uniform(size=10)
    data2 = 1+np.random.uniform(size=10)
    data3 = 2+np.random.uniform(size=10)

    # lables to these plots
    ticks = ['zero', 'one', 'two ', 'three', 'four', 'five ', 'six', 'seven', 'eight ', 'nine']

    print("Testing 2D plots")
    plot(data1, fig_name="test 2dplots", plot_name="top_plot", legend="data1", subplot_id=(n_splts,1,1))
    plot(data2, fig_name="test 2dplots", plot_name="top_plot", legend="data2", subplot_id=(n_splts,1,1))

    print("Testing bar plots")
    bar(data1, fig_name="test 2dplots", legend="data1", subplot_id=(n_splts,1,2))
    bar(data2, fig_name="test 2dplots", legend="data2", subplot_id=(n_splts,1,2), yaxislabel="data(m)")

    print("Testing top bottom plots")
    min_val = data1
    max_val = data2
    bar(xdata=ticks, height=data2-data1, bottom=data1, fig_name="test 2dplots", legend="range", subplot_id=(n_splts,1,3), xticklabels=ticks, xtickrotation=90, color='c')
    bar(data1, fig_name="test 2dplots", legend="min_val", subplot_id=(n_splts,1,3))

    print("Testing text addition")
    text(fig_name="test 2dplots", subplot_id=(n_splts,1,4), plot_name="signature text",
        positions = [(0.05, 0.8), (0.05, 0.6)],
        texts = ['Text A', 'Text B'],
         )

    print("Testing out of order retrieval")
    plot(data3, fig_name="test 2dplots", plot_name="top_plot", legend="data3", subplot_id=(n_splts,1,1), xaxislabel="time(s)")
    bar(data3, fig_name="test 2dplots", legend="data3", subplot_id=(n_splts,1,2))
    bar(data2, fig_name="test 2dplots", legend="max_val", subplot_id=(n_splts,1,3), plot_name="bottom_plot", )
    text(fig_name="test 2dplots", subplot_id=(n_splts,1,4), plot_name="signature text",
        positions = [(0.05, 0.4)],
        texts = ['Text C'],
         )

    show_plot()
