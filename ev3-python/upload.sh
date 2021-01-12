#!/bin/bash
rm -rf __pycache__/
scp -r ../ev3-python pi@192.168.1.11:/home/pi 
scp -r ../ev3-python pi@192.168.1.22:/home/pi
