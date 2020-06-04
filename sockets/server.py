import socket
import numpy as np
import time 

# configs
UDP_IP = "169.254.163.96"
UDP_PORT = 5005
print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)

# socket
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
t_strat = time.time()

# send
while True:
    time_now = time.time() - t_strat
    MESSAGE = np.array([time_now], dtype=np.float32)
    sock.sendto(MESSAGE.tobytes(), (UDP_IP, UDP_PORT))
