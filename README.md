# Autonomous-Courier-Robot

![alt text](https://github.com/rahulagrawal048/Autonomous-Courier-Robot/blob/master/test4.jpg)

Programming a robot for autonomous courier delivery. The arena represents a city where the first row is the warehouse. The parcels are represented in various shapes and colors and have to be matched for pickup-drop pairs. This top view of the arena is input into the program which processes the image using OpenCV and Python. The shapes and colors are detected to generate pickup-drop pairs. Dijisktra's algorithm and Traveling Salesman algorithm are used for path planning of the robot. The robot is built using Raspberry-pi and a webcam. The robot moves along the black line using images processed through the webcam, and the blue intersections are detected for turns.
