import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button, Slider

from vtils.ipc.shared_memory import shared_memory_array

HELP = """
Utility to quickly create on a shared memory interface that can be accessed by multiple programs:
Step
1. Create a shared memory interface:
  - python shared_interface.py
2. Access the shared memory interface values from other programs using
  - from vtils.ipc.shared_memory import shared_memory_array
  - user_ui = shared_memory_array(name="shared_interface", dtype=np.float64, shape=(10,))
"""

n_sl = 5
n_bt = 5
n_ui = n_sl + n_bt
ui_buffer = shared_memory_array(name="shared_interface", init_array=np.zeros(n_ui))

ax = []
ui = []


# Update slider buffers with UI values
def sl_update(val):
    for i_ui in range(n_sl):
        ui_buffer.val[i_ui] = ui[i_ui].val


# Update button buffers with UI values
def bt_update(event, button_index):
    ui_buffer.val[button_index] = 1
    print(event, button_index)


h_fig = plt.figure("Shared Memory Interface")
axcolor = "lightgoldenrodyellow"
# Define the sliders
for i_ui in range(n_ui):
    h_ax = plt.axes(
        [0.2, ((n_ui - 1) / n_ui) - i_ui / (n_ui + 1), 0.65, 0.03], facecolor=axcolor
    )
    # Create the sliders
    if i_ui < n_sl:
        h_ui = Slider(h_ax, f"Prm{i_ui}", 0.0, 1.0, valinit=0.0)
        h_ui.on_changed(sl_update)
    # Create buttons
    else:
        h_ui = Button(h_ax, f"Reset{i_ui-n_sl}", color=axcolor, hovercolor="0.975")
        h_ui.on_clicked(lambda event, index=i_ui: bt_update(event, index))

    ax.append(h_ax)
    ui.append(h_ui)

plt.show()
ui_buffer.close_link()
ui_buffer.delete_memory()
