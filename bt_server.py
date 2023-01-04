import bluetooth
import subprocess


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
client_sock, address = server_sock.accept()
print("Connection from ", address)

try:
    while True:
        data = client_sock.recv(1024)
        if not data:
            break
        received = data.decode("utf-8").splitlines()
        duty_cycle = received[1][0:2]
        if not duty_cycle[-1].isdigit():
            duty_cycle = duty_cycle[0:1]
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
        if movement == 'shutdown':
            subprocess.run(["shutdown", "now"])
except OSError:
    pass

print("Disconnected")
client_sock.close()
server_sock.close()
