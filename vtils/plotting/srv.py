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


# Simple Remote Viz
class SRV():
    def __init__(self, 
            buff_sz:[int]=500,
            xaxislabel:Optional[str]=None, 
            yaxislabel:Optional[str]=None,
            xaxislimit:Optional[Tuple[float]]=None,
            yaxislimit:Optional[Tuple[float]]=None,
            subplot_id:Optional[Tuple[int]] = (1,1,1),
            plot_name:Optional[str]=None,
            fig_name:Optional[str]="Simple Remote Viz",
            fig_size:Optional[Tuple[int]]=(1000,600),
        ):
        self.xaxislabel = xaxislabel
        self.yaxislabel = yaxislabel
        self.xaxislimit = xaxislimit
        self.yaxislimit = yaxislimit
        self.plot_name = plot_name
        self.fig_name = fig_name
        self.fig_size = fig_size
        self.buff_sz = buff_sz
        self.buff_idx = 0

        # multiprocess buffers shared between processes for hosting displayed data
        self.x = Array('d', (self.buff_sz))
        self.y = Array('d', (self.buff_sz))

        # start the process 
        self.start()

    # start child process for rendering
    def start(self):
        self.p = Process(target=self.run)
        self.p.start()

    # close windows and wait for the child process
    def join(self):
        self.p.join()

    # Append new data to the cyclic buffer
    def append(self, x_data, y_data):
        self.x[self.buff_idx] = x_data
        self.y[self.buff_idx] = y_data
        self.buff_idx = 0 if (self.buff_idx==self.buff_sz-1) else self.buff_idx+1
        
        # handle wrap around
        self.x[self.buff_idx] = x_data
        self.y[self.buff_idx] = 0.
        buff_idx1 = 0 if (self.buff_idx==self.buff_sz-1) else self.buff_idx+1
        self.y[buff_idx1] = 0.

    # Update entire buffer
    def update(self, x_data, y_data):
        self.x[:] = x_data[:]
        self.y[:] = y_data[:]

    # refresh plot with new data
    def refresh(self):
        self.curve.setData(self.x[:] ,self.y[:])

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
        if self.xaxislimit:
            plot.setXRange(min=self.xaxislimit[0], max=self.xaxislimit[1])
        if self.yaxislimit:
            plot.setYRange(min=self.yaxislimit[0], max=self.yaxislimit[1])
        self.curve = plot.plot(pen='r', connect="finite")

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
            srv2.append(t,-s)
            time.sleep(.001)
        print("Done")
        
    #To stop IO thread
    run = threading.Event()
    run.set()

    sz = 1000
    # create the plot
    srv1 = SRV(fig_name="SRV Example-1",
                buff_sz=sz,
                plot_name="Demo plot-1",
                xaxislabel="x-label",
                yaxislabel="y-label",
                xaxislimit=(-1, 100),
                yaxislimit=(-2, 3))

    # create a second plot
    srv2 = SRV(fig_name="SRV Example-2", buff_sz=1000, plot_name="Demo plot-2")

    # create static buffer 
    xx_buff = np.array(range(sz))/100
    yy_buff = np.sin(xx_buff)
    srv2.update(xx_buff, yy_buff)
    srv1.update(xx_buff, -yy_buff)
    time.sleep(3)

    # start IO thread
    t = threading.Thread(target=io, args=(run, srv1, srv2))
    t.start()

    input("Type Enter to quit.")
    run.clear()
    print("Waiting for IO thread to join...")
    t.join()
    print("Clsoe all graphs. Waiting for graph window process to join...")
    srv1.join()
    srv2.join()
    print("All process joined successfully.")