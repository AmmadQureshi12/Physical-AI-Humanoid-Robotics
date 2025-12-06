# Chapter 2 Exercises: Simulation Skills

## Exercise 1: URDF Creation
1. Create a custom URDF model for a simple mobile robot (differential drive)
2. Add two visual sensors: a camera at the front and a LiDAR on top
3. Verify the model loads correctly in RViz
4. Export the URDF to SDF format for Gazebo

## Exercise 2: Physics Simulation
1. Create a Gazebo world with uneven terrain
2. Add your robot model to the world
3. Configure physics properties (friction, restitution, etc.)
4. Test how different physics settings affect robot movement
5. Record and analyze the simulation results

## Exercise 3: Sensor Integration
1. Add an IMU sensor to your robot model
2. Configure the sensor to publish to appropriate ROS 2 topics
3. Create a ROS 2 node that subscribes to the IMU data
4. Implement a simple Kalman filter to process the IMU readings
5. Visualize the processed data in a graph