###
# Simple Remote Viz:
# A simple graphing tool for streaming data. 
# Creates a background process for windowing/ rendering.
# Good for timing critical applications.
###

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from multiprocessing import Process, Array
import sched, time, threading
from typing import Optional, Tuple
import collections

colors = ('r', 'g', 'b', 'c', 'm', 'y')

class Line():
    def __init__(self, buff_sz=100, name=None, color='b'):
        self.buff_sz = buff_sz
        self.name = name
        self.curve = None
        self.color = color
        
        # multi-process buffers shared between processes for hosting displayed data
        # buffers can be safely accessed from multiple processes
        self.x = Array('d', self.buff_sz)
        self.y = Array('d', self.buff_sz)

# Simple Remote Viz
class SRV():
    def __init__(self, 
            buff_sz:int=500,
            legends:Tuple[str]=None,
            xaxislabel:Optional[str]=None, 
            yaxislabel:Optional[str]=None,
            xaxislimit:Optional[Tuple[float]]=None,
            yaxislimit:Optional[Tuple[float]]=None,
            subplot_id:Optional[Tuple[int]] = (1,1,1),
            plot_name:Optional[str]=None,
            fig_name:Optional[str]="Simple Remote Viz",
            fig_size:Optional[Tuple[int]]=(1000,600),
        ):
        self.buff_sz = buff_sz
        self.legends = legends
        self.xaxislabel = xaxislabel
        self.yaxislabel = yaxislabel
        self.xaxislimit = xaxislimit
        self.yaxislimit = yaxislimit
        self.plot_name = plot_name
        self.fig_name = fig_name
        self.fig_size = fig_size

        # add lines to the plot using legends as keys
        self.buff_idx = 0
        self.n_lines = 0
        self.lines = collections.OrderedDict()
        assert type(legends) is tuple, "legends should be a tuple:"+legends
        for i, legend in enumerate(legends):
            print("Adding lines", i, legend)
            self.add_line(buff_sz, legend, colors[i%len(colors)])
        # start the process 
        self.start()

    def add_line(self, buff_sz, legend, color='g'):
        self.lines[legend] = Line(buff_sz=buff_sz, name=legend, color=color)
        self.n_lines += 1

    # start child process for rendering
    def start(self):
        # self.run()
        self.p = Process(target=self.run)
        self.p.start()

    # close windows and wait for the child process
    def close(self):
        self.p.join()

    # Append new data (indexed with keys order) to the cyclic buffer. 
    def append(self, x_data, y_data):
        if self.n_lines>1:
            data_id = 0
            for legend, line in self.lines.items():
                line.x[self.buff_idx] = x_data[data_id]
                line.y[self.buff_idx] = y_data[data_id]
                data_id += 1
        else:
            self.lines[self.legends[0]].x[self.buff_idx] = x_data
            self.lines[self.legends[0]].y[self.buff_idx] = y_data
        self.buff_idx = 0 if (self.buff_idx==self.buff_sz-1) else self.buff_idx+1

    # Update entire buffer
    def update(self, key, x_data, y_data):
        if key in self.lines.keys():
            self.lines[key].x[:] = x_data[:] 
            self.lines[key].y[:] = y_data[:] 

    # refresh plot with new data
    def refresh(self):
        for legend, line in self.lines.items():
            line.curve.setData(line.x[:], line.y[:])

    # Run viewer
    def run(self):
        # create window
        app = QtGui.QApplication([])
        win = pg.GraphicsWindow(title=self.fig_name)
        win.resize(self.fig_size[0],self.fig_size[1])
        
        # create plot
        plot = win.addPlot(title=self.plot_name)
        plot.setLabel(axis='left', text=self.xaxislabel)
        plot.setLabel(axis='bottom', text=self.yaxislabel)
        plot.addLegend()
        if self.xaxislimit:
            plot.setXRange(min=self.xaxislimit[0], max=self.xaxislimit[1])
        if self.yaxislimit:
            plot.setYRange(min=self.yaxislimit[0], max=self.yaxislimit[1])
        
        for legend, line in self.lines.items():
            line.curve = plot.plot(pen=line.color, 
                connect="finite", symbol='o', name=line.name)

        # update trigger
        timer = QtCore.QTimer()
        timer.timeout.connect(self.refresh)
        timer.start(50)

        # start process
        app.exec_()

if __name__ == '__main__':
    def io(running, srv1, srv2):
        t = 0.
        while running.is_set():
            s = np.sin(2 * np.pi * t)
            t += 0.01
            srv1.append(t,s)
            srv2.append([t, t],[s, -s-1])
            time.sleep(.02)
        print("Done")
        
    #To stop IO thread
    run = threading.Event()
    run.set()

    sz = 1000
    # create the plot
    srv1 = SRV(fig_name="SRV Example-1",
                buff_sz=sz,
                legends=("srv1:line1",),
                plot_name="Demo plot-1",
                xaxislabel="x-label",
                yaxislabel="y-label",
                xaxislimit=(-1, 30),
                yaxislimit=(-2, 3))

    # create a second plot
    srv2 = SRV(fig_name="SRV Example-2", buff_sz=1000,
                legends=("srv2:line1", "srv2:line2"), plot_name="Demo plot-2")

    # create static buffer and update plot
    xx_buff = np.array(range(sz))/100
    yy_buff = np.sin(xx_buff)

    srv1.update("srv1:line1", xx_buff, -yy_buff)
    srv2.update("srv2:line1", xx_buff, yy_buff)
    srv2.update("srv2:line2", xx_buff, -yy_buff)
    time.sleep(3)

    # start IO thread
    t = threading.Thread(target=io, args=(run, srv1, srv2))
    t.start()

    input("Type Enter to quit.")
    run.clear()
    print("Waiting for IO thread to join...")
    t.join()
    print("Clsoe all graphs. Waiting for graph window process to join...")
    srv1.close()
    srv2.close()
    print("All process joined successfully.")