import socket
import numpy as np

# configs
UDP_IP = "169.254.163.96"
UDP_PORT = 5005
print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)

# socket
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

# receive
while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print("received:", np.frombuffer(data, dtype=np.float32).tolist())

