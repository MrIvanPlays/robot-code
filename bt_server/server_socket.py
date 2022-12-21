import bluetooth
import subprocess

def readlines(socket):
    buffer = socket.recv(1024)
    buffering = True
    while buffering:
        if "\n".encode() in buffer:
            (line, buffer) = buffer.split("\n".encode(), 1)
            yield line
        else:
            more = socket.recv(1024)
            if not more:
                buffering = False
            else:
                buffer += more
    if buffer:
        yield buffer

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)
port = server_sock.getsockname()[1]

#Arbitrary uuid - must match Android side
sid = "133f71c6-b7b6-437e-8fd1-d2f59cc76066"

bluetooth.advertise_service(server_sock,
        'RPiServer',
        service_id = sid,
        service_classes = [sid, bluetooth.SERIAL_PORT_CLASS],
        profiles = [bluetooth.SERIAL_PORT_PROFILE]
    )

print("Listening for incoming connections")
client_sock, address = server_sock.accept()
print("Connection from ", address)

# TODO: Need to make it so that it doesn't disconnect the server

for line in readlines(client_sock):
    print("Received [%s]" % line)
    if line == "quit":
        break
    if line == b'forward':
        forward_cmd = subprocess.run(["rcontr", "control", "--movement forward", "--time 120", "--duty-cycle 10"])
        print("Exit code: %d" % forward_cmd.returncode)
    if line == b'backward':
        backward_cmd = subprocess.run(["rcontr", "control", "--movement backward", "--time 120", "--duty-cycle 10"])
        print("Exit code: %d" % backward_cmd.returncode)
    if line == b'left':
        left = subprocess.run(["rcontr", "control", "--movement left", "--time 120", "--duty-cycle 10"])
        print("Exit code: %d" % left.returncode)
    if line == b'right':
        right = subprocess.run(["rcontr", "control", "--movement right", "--time 120", "--duty-cycle 10"])
        print("Exit code: %d" % right.returncode)
    if line == b'parallelLeft':
        pLeft = subprocess.run(["rcontr", "control", "--movement parallel_left", "--time 120", "--duty-cycle 10"])
        print("Exit code: %d" % pLeft.returncode)
    if line == b'parallelRight':
        pRight = subprocess.run(["rcontr", "control", "--movement parallel_right", "--time 120", "--duty-cycle 10"])
        print("Exit code: %d" % pRight.returncode)

client_sock.close()