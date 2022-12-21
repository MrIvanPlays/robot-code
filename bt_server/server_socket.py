import bluetooth
import subprocess


def readlines(socket):
    buffer = socket.recv(1024).decode("utf-8")
    buffering = True
    while buffering:
        if "\n" in buffer:
            return buffer
        else:
            more = socket.recv(1024)
            if not more:
                buffering = False
            else:
                buffer += more.decode("utf-8")
    # buffer = socket.recv(1024)
    # buffering = True
    # while buffering:
    #     if "\n".encode() in buffer:
    #         (line, buffer) = buffer.split("\n".encode(), 1)
    #         yield line
    #     else:
    #         more = socket.recv(1024)
    #         if not more:
    #             buffering = False
    #         else:
    #             buffer += more
    # if buffer:
    #     yield buffer
    #return socket.recv(1024).decode("utf-8").splitlines()


server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)
port = server_sock.getsockname()[1]

# Arbitrary uuid - must match Android side
sid = "133f71c6-b7b6-437e-8fd1-d2f59cc76066"

bluetooth.advertise_service(server_sock,
                            'RPiServer',
                            service_id=sid,
                            service_classes=[sid, bluetooth.SERIAL_PORT_CLASS],
                            profiles=[bluetooth.SERIAL_PORT_PROFILE]
                            )

print("Listening for incoming connections")
while True:
    client_sock, address = server_sock.accept()
    print("Connection from ", address)

    received = readlines(client_sock).splitlines()
    duty_cycle = received[1]
    movement = received[0]
    print("read duty_cycle of " + duty_cycle + " with movement type of " + movement)

    if movement == 'forward':
        forward_cmd = subprocess.run(["rcontr", "control", "--movement forward", "--duty-cycle " + duty_cycle])
        print("Exit code: %d" % forward_cmd.returncode)
    if movement == 'backward':
        backward_cmd = subprocess.run(["rcontr", "control", "--movement backward", "--duty-cycle " + duty_cycle])
        print("Exit code: %d" % backward_cmd.returncode)
    if movement == 'left':
        left = subprocess.run(["rcontr", "control", "--movement left",  "--duty-cycle " + duty_cycle])
        print("Exit code: %d" % left.returncode)
    if movement == 'right':
        right = subprocess.run(["rcontr", "control", "--movement right", "--duty-cycle " + duty_cycle])
        print("Exit code: %d" % right.returncode)
    if movement == 'parallelLeft':
        pLeft = subprocess.run(["rcontr", "control", "--movement parallel_left", "--duty-cycle " + duty_cycle])
        print("Exit code: %d" % pLeft.returncode)
    if movement == 'parallelRight':
        pRight = subprocess.run(["rcontr", "control", "--movement parallel_right", "--duty-cycle " + duty_cycle])
        print("Exit code: %d" % pRight.returncode)
