#!/usr/bin/env bash

sudo hciconfig hci0 piscan
sudo hciconfig hci0 sspmode 1

python3 -m bt_server
