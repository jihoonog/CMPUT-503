---
author: "Jihoon Og"
title: "Exercise 3"
date: 2023-03-03
description: "Third Lab Assignment"
tags: ["lane following", "programming", "ROS", "pid", "sensor fusion"]
categories: ["robot"]
ShowRelated: false
showToc: true
math: true
ShowBreadCrumbs: false
---
This is the third lab assignment of the course.

# Part 1

## Questions

1. What does the april tag library return to you for determining its position?

For each tag it detects, it returns the x, y coordinates for the tag's center and its corners. It uses the image coordinate system meaning the origin starts in the top left corner and increases as you go right and down. It can also estimate the pose of the tag with respect to the camera in (x,y,z)

2. Which directions do the X, Y, Z values of your detection increase / decrease?

The z-axis points from the camera's center out from the camera's lens.
The x-axis is to the right in the image taken by the camera.
The y-axis goes down from the top frame of the camera.

3. What frame orientation does the april tag use?

The tag's coordinate frame is centered at the center of the tag, with the x-axis pointing to the right, y-axis pointing down, and the z-axis pointing into the tag.

https://github.com/AprilRobotics/apriltag/wiki/AprilTag-User-Guide

4. Why are detections from far away prone to error?

Tags that are further away will make it harder for the camera to distinguish the smaller "pixels" that identifies the april tags. Moreover, the focal length is set for a particular distance from the camera and objects that are farther away from the focal length will be out-of-focus thus making it harder for the detection algorithm to find and identify the tag.

5. Why may you want to limit the rate of detections?

Detecting the april tags too frequently will add unnecessary overhead to the system adding additional latency that could negatively affect other systems that are critical.

# Part 2

The video below shows the robot performing some basic lane following driving on the right lane:

{{< youtube lgFcwYm_tRE >}}

The video below shows the robot performing some basic lane following driving on the left lane:

{{< youtube MQJUCQqfxbg >}}

## Questions

1. What is the error for your PID controller?

We used two errors, one is the lateral error, and the other is the angular error from the centerline. While we could just use the lateral error for correction, we've decided to use bot the lateral and angular error as they are provided by the lane filter node. Moreover, having the additional angular error will help with the lane following as the Duckiebot could be in the center of a lane but at an off angle where moving forward will cause it to drift out of the lane.

2. If your proportional controller did not work well alone, what could have caused this?

Using proportional control led to decent on-center performance on a straight lane tile, however it led to poor on-center performance during a turn. This is
because the proportional term only handles errors happening at present time. On a straight lane if the robot was already aligned with the center of the lane very little correction is needed so long as the trim is set correctly. However, during a turn the center of the lane is constantly moving thus requiring the Duckiebot to make constant corrections. If the proportional term is too small then it can't make a large enough correction to stay within the lane. However, if the term is too large then it will over-correct and create oscillation during the straights. Moreover, a happy medium doesn't really exist that works well for both turns and straights. Therefore, we needed to give more feedback.

3. Does the `D` term help your controller logic? Why or why not?

Adding a `D` term helped a lot with the overshoot from having too high of a `P` term. Because the `D` term tries to look at future trends in error it provides a dampening component if the `P` and `I` components leads to an overshoot.

4. (Optional) Why or why not was the `I` term useful for your robot?

The `I` term was useful at the turning tiles as there was a constant change in direction as well as the location of the center line with respect to the Duckiebot's lateral axis. As the error grows over time the `I` component will add more and more corrective effort in order to bring the Duckiebot back to the center of the lane.

# Part 3

## Questions

# Repo Link

[Exercise 3 repository link (TODO)]()

# References

This is a list of references that I used to do this exercise.

1. Lane Controller Node: https://github.com/duckietown/dt-core/blob/6d8e99a5849737f86cab72b04fd2b449528226be/packages/lane_control/src/lane_controller_node.py
2. Lane Controller: https://github.com/duckietown/dt-core/blob/6d8e99a5849737f86cab72b04fd2b449528226be/packages/lane_control/include/lane_controller/controller.py
3. PID Controller: https://en.wikipedia.org/wiki/PID_controller
4. PID controller code: https://github.com/jellevos/simple-ros-pid/blob/master/simple_pid/PID.py
