#!/bin/sh
trap 'exit' INT TERM
trap 'kill 0' EXIT

python3 code/tpjTempSensorGUI.py &
python3 code/tpjMain.py && misc/resetPins.sh

wait
