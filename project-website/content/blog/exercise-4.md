---
author: "Jihoon Og"
title: "Exercise 4"
date: 2023-03-11
description: "Fourth Lab Assignment"
tags: ["lane following", "programming", "ROS", "pid", "Vehicle following", "collision avoidence"]
categories: ["robot"]
ShowRelated: false
showToc: true
math: true
ShowBreadCrumbs: false
---
This is the third lab assignment of the course.

## Team Members

* Jihoon Og
* Qianxi Li

# Exercise 4 Don't Crash! Trailing Behaviour

For this exercise we were tasked on implementing a following behaviour on our Duckiebot where it will follow a leader bot if it detects one around the Duckietown environment.
This involves combining different components from previous exercises such as lane following, Apriltag detection, and custom LED emitter patterns.
With new components like vehicle detection and distance calculation.
All of these components are fed into a single node that handles the robot and lane following behaviour.

## Video

The video below shows the Duckiebot with the yellow duck following a leader bot around the Duckietown environment.
It stops at intersections and signals its intention to other robots to its rear.
We didn't use the front LED as it could affect the computer vision system for detecting the stop line and leader bot.
Note, there are some instances where the robot stops for a prolong period of time. This was caused by network congestion that prevented the robot from getting new data as the ROS master was running locally on a laptop, not the robot for faster processing.

{{< youtube W3gIKMUOscg >}}

## Brief Implementation Strategy

Each subsection below contains a brief paragraph describing our implementation strategy for maintaining a safe driving distance and avoiding collisions
### Lane following

For lane following we took our implementation from [exercise 3](https://quackquack.forkprocess.com/blog/exercise-3/#part-2---lane-following) and incorporated it into this exercise. It worked well for the Duckietown environment and we decided to reused it for this exercise with some minor parameter changes to the PID controllers for lane following.

### Leader Robot Detection, Distance Calculation, and Collision Avoidance

For robot detection and distance calculation we decided to use the `duckiebot_detection_node` and `duckiebot_distance_node` provided to use for this exercise as it provided a reasonably accurate detection and distance calculation based on the vehicle tag on the back of the Duckiebot. To utilize this information we have two callback functions, one for detecting if a robot exist within its camera's field-of-view, another is to store the distance from the robot. In the `get_control_action` function which is responsible for moving the robot in a controlled manner a check is done to see if the distance to the leader bot is below a set threshold. If so it will stop the robot until the leader bot move beyond the set threshold.

### Intersection Detection and Handling

For intersection detection and handling we based our code from the stop_line_filter_node from dt-core. At a high-level it takes all red line segments generated from the lane detector node from the Duckiebot lane following pipeline and convert them into lane frame (or its frame of reference from the robot). It then takes the average of all the x values from the converted line segments and determine the distance from the red stop line. If the distance is within a set threshold then the robot stops at the red stop line following the rules of the road and either follows the leader bot or drives autonomously using via lane following if it loses track of the leader bot. The robot also signal its intention when its handling intersections, with flashing turn signals and red brake lights when it's stopped at intersections.

### Vehicle Tracking at Intersections

For tracking the lead vehicle at intersections we compute the average x values from the 21 dots behind the Duckiebot as seen from the camera. Depending if the averaged x value is on the left, center, or right side of the image we can make an educated guess on where the lead robot will go. To improve robustness in the system we take a history and take the most common prediction at an intersection.
If no lead bot is detected then a `None` value is added to the prediction causing the robot to drive autonomously (lane follow) around Duckietown.

## Brief Dissions on Results 
## Questions

1. How well did your implemented strategy work?

Our implemented strategy worked well for lane following, vehicle detection, stop line detection, and going straight at an intersection. This is because most of our implementation is based on Duckietown's implementation that we just built upon.  

1. Was it reliable?

It was mostly reliable when it was lane following and following behind the leader bot without making any turns at an intersection i.e., going straight. Any complicated behaviours like right turns at intersections where it can lose track behind an april tag or non-precise movements from the leader bot lead to less than ideal behaviour.

3. In what situations did it perform poorly?

If the leader bot makes a right turn at an intersection then the follower bot might lose track as the rear vehicle tag is hidden behind the Apriltags causing it to lose track and revert back to lane following which if possible defaults to driving straight at an intersection.  

## Repo Link

[Exercise 4 repository link](https://github.com/jihoonog/CMPUT-503-Exercise-4)

## References

This is a list of references that I used to do this exercise.

1. Lane Controller Node: https://github.com/duckietown/dt-core/blob/6d8e99a5849737f86cab72b04fd2b449528226be/packages/lane_control/src/lane_controller_node.py
2. Lane Controller: https://github.com/duckietown/dt-core/blob/6d8e99a5849737f86cab72b04fd2b449528226be/packages/lane_control/include/lane_controller/controller.py
3. PID Controller: https://en.wikipedia.org/wiki/PID_controller
4. PID controller code: https://github.com/jellevos/simple-ros-pid/blob/master/simple_pid/PID.py
5. Stop line filter node code: https://github.com/duckietown/dt-core/blob/daffy/packages/stop_line_filter/src/stop_line_filter_node.py