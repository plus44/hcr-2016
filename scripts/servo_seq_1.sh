#! /bin/bash

python src/pi/step_servo.py -p "9,11,10,14,7,8,15" -d "90,120,0,180,170,1,90" && \
python src/pi/step_servo.py -p "11" -d "39" && \
python src/pi/step_servo.py -p "9,15" -d "0,75" && \
python src/pi/step_servo.py -p "15" -d "100" && \
python src/pi/step_servo.py -p "11,10,14,7,8" -d "120,130,0,80,91" && \
python src/pi/step_servo.py -p "7,8,15" -d "170,1,90" && \
python src/pi/step_servo.py -p "14,10" -d "180,0" 


python src/pi/step_servo.py -p "9,11,10,14,7,8,15" -d "90,120,0,180,170,1,90" && \
python src/pi/step_servo.py -p "11" -d "39" && \
python src/pi/step_servo.py -p "9,15" -d "0,75" && \
python src/pi/step_servo.py -p "15" -d "100" && \
python src/pi/step_servo.py -p "11,10,14,7,8" -d "120,130,0,80,91" && \
python src/pi/step_servo.py -p "7,8,15" -d "170,1,90" && \
python src/pi/step_servo.py -p "14,10" -d "180,0" 

