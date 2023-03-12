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

# Team Members

* Jihoon Og
* Qianxi Li

# Video

Embed video link

# What I learned from this exercise

For this exercise I learned how to implement PID control for following the lanes within Duckietown. Moreover, I learned how to reuse the existing lane following pipeline to implement my own lane following node using PID control.

# Questions

1. How well did your implemented strategy work?
2. Was it reliable?
3. In what situations did it perform poorly?

# Repo Link

[Exercise 4 repository link](https://github.com/jihoonog/CMPUT-503-Exercise-4)

# References

This is a list of references that I used to do this exercise.

1. Lane Controller Node: https://github.com/duckietown/dt-core/blob/6d8e99a5849737f86cab72b04fd2b449528226be/packages/lane_control/src/lane_controller_node.py
2. Lane Controller: https://github.com/duckietown/dt-core/blob/6d8e99a5849737f86cab72b04fd2b449528226be/packages/lane_control/include/lane_controller/controller.py
3. PID Controller: https://en.wikipedia.org/wiki/PID_controller
4. PID controller code: https://github.com/jellevos/simple-ros-pid/blob/master/simple_pid/PID.py