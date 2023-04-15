---
author: "Jihoon Og"
title: "Final Project"
date: 2023-04-14
description: "CMPUT-503 Final Project"
tags: ["driving test", "programming", "ROS", "Vehicle following", "image recognition", "apriltag"]
categories: ["robot"]
ShowRelated: false
showToc: true
math: true
ShowBreadCrumbs: false
---

## Team Members

* Jihoon Og
* Qianxi Li

# Final Project

In this final project, we needed to combine all the knowledge we learned from the previous 5 exercises together and finish 3 separate tasks using our Duckiebot.

## Stage 1

We have a Duckietown like the one below, the first stage is to start at the start position, the Duckiebot should move autonomously and following the commands from the Apriltags in Duckietown. Each tag is assigned with one kind of traffic signal, like stop, turn, and go straight. The desired route for the Duckiebot is to follow the purple route on the diagram below.

The diagram below shows one of the route that the Duckiebot needs to take for stage 1. The other route is taking the outside lane of the loop.

![stage 1](/uploads/stage_1.png)

## Stage 2

After stage 1 is finished, it will go straight until it see a pedestrian walk or a duck walk in this case and make a short stop, if there are ducks waddling through the duck walk it will stop until it has been cleared. Otherwise, it will continue ahead. It then makes a turn, and the Duckiebot should stop, then move around the broken Duckiebot on the road and avoid run into it. It then needs to successfully handle a second duck walk following the same rules as the first one.

The diagram below shows what the Duckiebot needs to do to complete stage 2.

![stage 2](/uploads/stage_2.png)

## Stage 3

The last stage is to park the Duckiebot into one of the 4 stalls. Which stall to park into is determined during the start of the demo.

The diagram below shows the 4 different stalls and the path to park in them.

![stage 3](/uploads/stage_3.png)

# Implementation strategies

## Detection

To make the Duckiebot see, we utilized multiple different techniques for detecting different kinds of objects.
For this project, things that need to be detected include:

* White and yellow lanes on the road
* Red stop lines
* Apriltags
* Obstacle detection (like the broken Duckiebot, yellow rubber duck, blue lane for pedestrian crossing)

### Broken Car

As the Duckiebot move toward the broken Duckiebot on the road, it is able to see the circular grid pattern on the back of it. In this case, we use the template code from exercise 4, which is about detecting the Duckiebot from the camera. For distance calculation we used the laser range finder because it is more accurate in determining the distance.

### April Tag

This was prett straightforward, the Apriltag detector has been used in many tasks in the past several exercises. One special things here is that, we needed the pose for each detection so that we can keep the closest detection to the Duckiebot, otherwise it will give up multiple detection and multiple conflicting commands.

### Yellow duck and blue lane for pedestrian crossing

Instead of using machine learning techniques to do the duck detection, we just used a simple color masks to mask out everything that is not yellow. The high-level idea is: first, we detect the stop sign Apriltag, then we detect the blue pedestrian crossing using the color mask, since the blue is unique around the stop sign Apriltag we just need to know whether there's something blue in the image and on the road. Next, for the duck detection, we just need to know whether there's something yellow in the image and on the blue lane, so color masking was used to find the ducks. However, because the yellow colour of the duck is similar to the yellow color of the median, we added an area threshold to only detect yellow that is big enough to be rubber duck sized and not a yellow lane marking.

## Video demo

Below shows a video demo of our bot doing all three stages.

{{< youtube MgHLmd6TGSw >}}

## Repo Link

[Exercise 5 repository link](https://github.com/jihoonog/CMPUT-503-Final-Project)

## References

- https://docs.photonvision.org/en/latest/docs/getting-started/pipeline-tuning/apriltag-tuning.html
- https://docs.duckietown.com/daffy/
- https://github.com/duckietown/lib-dt-apriltags

## Work Division

- Jihoon: PID control, use detection results and make the robot make the right decision (turn, go straight, stop, avoid duck and broken car)
- Qianxi: All the detection things. Detect Apriltag, red and blue lanes and rubber ducks.
- Almas: Parking