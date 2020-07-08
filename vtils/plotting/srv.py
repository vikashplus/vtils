###
# Simple Remote Viz:
# A simple graphing tool for streaming data. 
# Creates a background process for windowing/ rendering.
# Good for timing critical applications.
###

from multiprocessing import Process, Array
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import sched, time, threading
from typing import Optional, Tuple
import collections


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
        self.xaxislabel = xaxislabel
        self.yaxislabel = yaxislabel
        self.xaxislimit = xaxislimit
        self.yaxislimit = yaxislimit
        self.plot_name = plot_name
        self.fig_name = fig_name
        self.fig_size = fig_size

        # add lines to the plot using legends as keys
        self.data_cnt = 0 # total data seen so far
        self.buff_idx = 0
        self.n_lines = 0
        self.legends = []
        self.lines = collections.OrderedDict()
        assert type(legends) is tuple, "legends should be a tuple:"+legends
        for i, legend in enumerate(legends):
            print("Adding lines", i, legend)
            self.add_line(buff_sz, legend, pg.intColor(i))
        # start the process 
        self.start()

    def add_line(self, buff_sz, legend, color='g'):
        self.lines[legend] = Line(buff_sz=buff_sz, name=legend, color=color)
        self.n_lines += 1
        self.legends.append(legend)

    # start child process for rendering
    def start(self):
        # self.run()
        self.p = Process(target=self.run)
        self.p.start()

    # close windows and wait for the child process
    def close(self):
        self.p.join()

    # Append new data to the cyclic buffer.
    # indexed with keys order; legends order if None
    def append(self, x_data=None, y_data=None, keys=None):
        self.data_cnt += 1
        if keys is None:
            keys = self.legends

        assert y_data is not None, "y_data can't be none."
        if x_data is None:
            if np.isscalar(y_data):
                x_data = self.data_cnt
            else:
                x_data = self.data_cnt * np.ones_like(y_data)

        if self.n_lines>1:
            for data_id, key in enumerate(keys):
                self.lines[key].x[self.buff_idx] = x_data[data_id]
                self.lines[key].y[self.buff_idx] = y_data[data_id]
        else:
            self.lines[keys[0]].x[self.buff_idx] = x_data
            self.lines[keys[0]].y[self.buff_idx] = y_data
        self.buff_idx = 0 if (self.buff_idx==self.buff_sz-1) else self.buff_idx+1

        for data_id, key in enumerate(keys):
            self.lines[key].x[self.buff_idx] = np.nan
            self.lines[key].y[self.buff_idx] = np.nan

        

    # Update entire buffer
    def update(self, key, x_data=None, y_data=None):
        assert key in self.lines.keys(), "Provided key: {} not found".format(key)

        if x_data is None and y_data is None: # clear both
            x_data = y_data = 0

        # update x
        if x_data is not None:
            if np.isscalar(x_data):
                self.lines[key].x[:] = x_data*np.ones(self.lines[key].buff_sz)
            else:
                self.lines[key].x[:] = x_data[:] 

        # update y
        if y_data is not None:
            if np.isscalar(y_data):
                self.lines[key].y[:] = y_data*np.ones(self.lines[key].buff_sz)
            else:
                self.lines[key].y[:] = y_data[:]

        self.data_cnt += self.lines[key].buff_sz

    # Clear graph buffer
    def clear(self, keys:tuple=None):
        if keys is None:
            keys = self.legends
            self.buff_idx = 0
        else:
            assert type(keys) is tuple, "keys should be a tuple:"+keys

        for key in keys:
            self.update(key, x_data=None, y_data=None)

        self.data_cnt = 0

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
        
        symbols = ['o', 's', 't', 'd', '+']
        i = 0
        for legend, line in self.lines.items():
            i = i+1
            sym = symbols[i%5]
            line.curve = plot.plot(pen=pg.mkPen(line.color, width=3.0), symbolSize=5,
                connect="finite", symbol=sym, name=line.name)

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
            srv1.append(y_data=s) # used incremental indexes for X
            srv2.append([t, t],[s, -s-1])
            time.sleep(.01)
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
    srv2 = SRV(fig_name="SRV Example-2", buff_sz=sz,
                legends=("srv2:line1", "srv2:line2"), plot_name="Demo plot-2")

    # create static buffer and update plot
    xx_buff = np.array(range(sz))/100
    yy_buff = np.sin(xx_buff)

    xx_buff[2] = np.nan
    yy_buff[2] = np.nan
    srv1.update("srv1:line1", xx_buff, -yy_buff)
    srv2.update("srv2:line1", xx_buff, yy_buff)
    srv2.update("srv2:line2", xx_buff, -yy_buff)
    time.sleep(2)

    # clear data
    srv1.clear(("srv1:line1",))
    srv2.update("srv2:line1", y_data=1)
    srv2.update("srv2:line2", y_data=-1)
    time.sleep(1)

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