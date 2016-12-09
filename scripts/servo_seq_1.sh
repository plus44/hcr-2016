#! /bin/bash

python src/pi/step_servo.py -p "9,11,10,8" -d "90,90,0,0"
sleep 3
python src/pi/step_servo.py -p "11" -d "0"
sleep 1
python src/pi/step_servo.py -p "9" -d "0"
sleep 1
python src/pi/step_servo.py -p "11,10" -d "90,130"
