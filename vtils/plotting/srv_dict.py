"""
Simple plotting class for dict data
"""

from vtils.plotting.srv import SRV
import time

class srv_dict(SRV):
    """
    Simple plotting with dict inputs
    """
    def __init__(self, buff_sz=100, **kwargs):
        self.initialized = False

    def append(self, data, keys=None, **kwargs):
        """
        Append new data point
        """
        if not self.initialized:
            self.initialize(data, keys, **kwargs)

        if keys:
            plot_data = [val*data[key] for key, val in keys.items()]
            # reward_values = (
            #     reward_dict[key] * weight
            #     for key, weight in self._reward_keys_and_weights.items()
            # )

        else:
            plot_data = [data[key] for key in data.keys()]
        self.viz.append(y_data = plot_data)

    def initialize(self, data, keys=None, **kwargs):
        """
        Initialize viewer
        """
        if keys:
            self.keys = tuple(keys)
        else:
            self.keys = tuple(data.keys())
        self.viz = SRV(legends= self.keys, **kwargs)
        self.initialized = True

    def clear(self):
        """
        Clear Viewer
        """
        self.viz.clear()

    def close(self):
        """
        Close Viewer
        """
        self.viz.close()


# Example usage
if __name__ == '__main__':
    # dummy dict
    data = {'a':1, 'b':2}

    # init class
    dict_plot = srv_dict()

    # plot
    for i in range(10):
        dict_plot.append(data)
        time.sleep(.1)

    # clear
    dict_plot.clear()

    # plot some more
    for i in range(10):
        data['a'] = i*10
        data['b'] = i*5
        dict_plot.append(data)
        time.sleep(.1)

    print("Close all graphs now. \nWaiting for graph window process to join...")
    dict_plot.close()
    print("All process joined successfully.")


