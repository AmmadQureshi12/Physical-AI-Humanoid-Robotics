# ROS 2 Exercises
# Chapter 1: ROS 2 Fundamentals

## Exercise 1: Basic ROS 2 Package
Create a simple ROS 2 package that includes:
1. A publisher node that sends "Hello, ROS 2!" messages
2. A subscriber node that receives and logs these messages
3. A launch file to run both nodes together

## Exercise 2: Topic Subscription
Implement a node that subscribes to sensor data (e.g., IMU or joint states) and:
1. Processes the data
2. Publishes a processed result to a new topic
3. Verifies the data flow works correctly

## Exercise 3: Service Implementation
Create a service server and client that:
1. Server provides a calculation service (e.g., adding two numbers)
2. Client calls the service with parameters
3. Verify the request/response cycle works correctly