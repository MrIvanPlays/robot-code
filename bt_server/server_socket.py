#!/usr/lib/env python3

# Some test server socket code

import bluetooth

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"


def start():
    bluetooth.advertise_service(server_sock, "RPi Robot server", service_id=uuid,
                                service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                                profiles=[bluetooth.SERIAL_PORT_PROFILE],
                                protocols=[bluetooth.OBEX_UUID]
                                )
    print("Waiting for connection on RFCOMM channel", port)

    client_sock, client_info = server_sock.accept()
    print("Accepted connection from", client_info)

    try:
        while True:
            data = client_sock.recv(1024)
            if not data:
                break
            print("Received", data)
    except OSError:
        pass

    print("Disconnected.")
    client_sock.close()
    server_sock.close()
    print("All done.")
