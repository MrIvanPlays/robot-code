#!/usr/bin/env bash

sudo hciconfig hci0 piscan

python3 -m bt_server
