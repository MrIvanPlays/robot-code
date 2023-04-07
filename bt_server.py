import bluetooth
import subprocess
import RPi.GPIO as GPIO
import threading

from robot import robot as controls

LED = 11 # GPIO17

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(LED, GPIO.OUT)

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
GPIO.output(LED, True)
client_sock, address = server_sock.accept()
print("Connection from ", address)


class RepeatTimer(threading.Timer):
    def run(self):
        while not self.finished.wait:
            controls.initialize()
            self.function(*self.args, **self.kwargs)


task = None
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
        if task is not None:
            task.cancel()
        print("read duty_cycle of " + duty_cycle + " with movement type of " + movement)

        if movement == 'forward':
            task = RepeatTimer(0.01, controls.forward(int(duty_cycle))).start()
        if movement == 'backward':
            task = RepeatTimer(0.01, controls.backward(int(duty_cycle))).start()
        if movement == 'left':
            task = RepeatTimer(0.01, controls.left(int(duty_cycle))).start()
        if movement == 'right':
            task = RepeatTimer(0.01, controls.right(int(duty_cycle))).start()
        if movement == 'parallelLeft':
            task = RepeatTimer(0.01, controls.parallel_left(int(duty_cycle))).start()
        if movement == 'parallelRight':
            task = RepeatTimer(0.01, controls.parallel_right(int(duty_cycle))).start()
        if movement == 'shutdown':
            subprocess.run(["shutdown", "now"])
        if movement == 'stop':
            controls.cleanup()
except OSError:
    pass

print("Disconnected")
GPIO.output(LED, False)
client_sock.close()
server_sock.close()
