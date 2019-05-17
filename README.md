# Automated Cable Cross

https://www.youtube.com/watch?v=fpqCy7uoiqk&t=1s

![Front View]()

This is my Automated Cable Cross machine for my final project in ECE 387. I wanted to prototype a machine for beginners to make the cable cross machine more useful and intuitive. Cable excercises are some of the best for beginners because they are not intimidating like deadlifts and bench presses, but they are often told to do a lift with very little instruction. My machine's touch screen interface is very easy to read, all of the excercicses featured can be pressed, and the arms of the machine will move the postion for the lift. The arrows next to the picture control the corresponding arms. Arms can be moved up and down for personal prefrences for an excercise or for a custom lift. The muscle group buttons, when pressed, will hide all excercise icons that are for the selected muscle group. The servos have full range of motion, unlike the preset locations of the typical cable machine. The arms can also be rotated forward and back for an even wider range of excercises.

## Materials Used
- 30 feet of PVC pipe
- 12 square ft. of ply wood
- 2x 55g Servos
- 2x 20 kg Servos
- 1x Raspberry Pi 3
- 1x Ardiuno Uno
- 65 lb. fishing line
- 2x M15 Stainless Steel Pulley
- 7" Touchscreen display
- 3x Small wall hooks
- 6V external power supply

## How it Works
The touch screen display works like a normal screen via hdmi, and connects to the Rasoberry Pi via usb and works like a mouse when touched. The GUI was programmed in python using the pygame library because it works the best with GPIO connections, although it can sacrifice speed. The servos are all controlled by the arduino, and the Raspberry Pi uses the pyfirmata library to communicate over serial to the arduino. This allows for the python script to control the arduino pins directly. The 55g servos are used to pivot the arms, rotating forward and backwards, acting like a platform for the motor controlling the arms. The 20 kg servos control the pvc arms, and their range of motion is 270 degrees, so the code had to output 2/3 of the intended pwm signal to servos to ensure an accurate arm location. 
