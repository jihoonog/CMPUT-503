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

# Team Members

* Jihoon Og
* Qianxi Li

# Part 1 - Computer Vision

Part 1 was primarily done by my lab partner Qianxi Li, the report is mostly from his website [here](https://sites.google.com/ualberta.ca/qianxi-duckie/exercises/exercise-3)

For this exercise, we were required to interact with the transformation between different frames in the Duckietown environment. We first needed to recognize the different AprilTags using the built-in computer vision library. For section 1 of exercise 3, we basically needed to undo the distortion caused by the camera, then use the AprilTags detector library to get the tag's id, location, rotation pose, and corner locations within the camera frame. We then needed to label the edge of the tag and give a type to it. Depending on the type of the AprilTag, we needed to change the color of the LED emitter based on the table below:

- Red: Stop Sign
- Blue: T-Intersection
- Green: U of A Tag
- White: No Detections

In certain situations the camera may capture multiple tags within it's field of view. However, we only want to detect the closest one. So we only keep the one with the smallest z-value (closest to our camera) and the clamp the maximum z-value to be accepted to 0.5 meters. In addition, the margin of our detection should be larger than 10 to get classified as an AprilTag with a strong confidence.

Because the lens of the camera distort our image, the lines within the image are not straight. Therefore, when people deal with 3-D tasks from photo image input, an undistortion stage is required.

## Questions

1. What does the april tag library return to you for determining its position?

For each tag it detects, it returns the x, y coordinates for the tag's center and its corners. It uses the image coordinate system meaning the origin starts in the top left corner and increases as you go right and down. It can also estimate the pose of the tag with respect to the camera in (x,y,z).

2. Which directions do the X, Y, Z values of your detection increase / decrease?

The z-axis points from the camera's center out from the camera's lens.
The x-axis is to the right in the image taken by the camera.
The y-axis goes down from the top frame of the camera.
So moving away from the camera will increase the z value, moving to the right of the camera will increase the x value, and moving downward of the camera will crease the y value.

3. What frame orientation does the april tag use?

The tag's coordinate frame is centered at the center of the tag, with the x-axis to the right, y-axis pointing down, and the z-axis pointing into the tag.

https://github.com/AprilRobotics/apriltag/wiki/AprilTag-User-Guide

4. Why are detections from far away prone to error?

Tags that are further away will make it harder for the camera to distinguish the smaller "pixels" that identifies the AprilTags. Moreover, the focal length is set for a particular distance from the camera and objects that are farther away from the focal length will be out-of-focus thus making it harder for the detection algorithm to find and identify the tag.

5. Why may you want to limit the rate of detections?

Detecting the AprilTags too frequently will add unnecessary overhead to the system adding additional latency that could negatively affect other systems that are critical.

## Video

The video below shows how the Duckiebot detects and labels the AprilTag using a bounding box and a text label. A tag with a type of intersection is detected by the camera.

{{< rawhtml >}}<iframe src="https://drive.google.com/file/d/1DAXbdUZXFY1npf_VjEOVV97hlnL_UAvL/preview" width="640" height="480" allow="autoplay"></iframe>{{< /rawhtml >}}

# Part 2 - Lane Following

This part was primarily done by me.

## Implementation

In order to ease development of the lane following functionality we've decided to reuse the lane following pipeline from the `dt-core` module. Below is a diagram from the Duckietown documentation showing an overview of the lane following pipeline.

![lane following pipeline](/uploads/data-from-img-image_pipeline_overview-77bbe28a.png)

For this lab exercise we've implemented our own lane controller node that take in `lane pose` generated by the lane filter node from the Duckiebot's built-in lane following pipeline. The main difference between their implementation and mine is that We use all three PID parameters (Proportional, Integral, and Derivative) for both the lateral and angular error while they use only proportional and integral terms for the lateral and angular error. The main rational is to further improve performance by using a `D` term to decrease overshoot as well settling time.

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

## Video Demo

The video below shows the robot performing some basic lane following driving on the right lane:

{{< youtube lgFcwYm_tRE >}}

The video below shows the robot performing some basic lane following driving on the left lane:

{{< youtube MQJUCQqfxbg >}}

# Part 3 - Localization Using Sensor Fusion

Part 3 was primarily done by my lab partner Qianxi Li, the report is mostly from his website [here](https://sites.google.com/ualberta.ca/qianxi-duckie/exercises/exercise-3

The top-level goal for this part is to utilize:

1. The known locations of all AprilTags in the world frame (from part 1)
2. Use the node we wrote in part 1 to detect the presence of April tags in the image to get a better lane following in a world shown below.

![figure](https://lh4.googleusercontent.com/36C5gYovAqNRHZWxK6JLJIC2jyGWC86t_VuJaVaIFslpzLUIPpIhG-tx5SFRfCselZzEKxFOmeNwePCcYBqFtkfXUS7tY-4FD1ztzWoU6m2IS8oBO1S-q7K1xCUe_F243w=w1280)

As we are using the lane following system from part 2, if we detect an AprilTag the camera, we then can figure out where the robot is in the world frame and update its pose to the true location, otherwise, we continue to use odometry which may be inaccurate.

The image above is the Duckietown environment our Duckiebots are interacting with, in the next several sections, our Duckiebots will travel along the blue lane, and we will examine the odometry and how the frames of robot interact with each other.

### Section 3.1-3.2

In these two sections, the two primary things we needed to get familiar with were: 

1. Using Rviz to visualize different frames and transformations in different forms
2. Given some fixed landmarks in the world, compare the path the robot traveled measured in world frame with the measurements produced by odometry.

We need to use the method `static_transform_publisher` of TF2 to broadcast the locations and orientations of 10 different Apriltags in the world frame. Rviz can then be used to visualize all of their locations in the world frame.

#### Questions


1. Where did your odometry seem to drift the most? Why would that be?

It drifted to the right more frequently. One reason could be that it's hard to make a perfect 90-degree turn by only looking at the camera image, usually when it makes the turn, you feel that it’s a little too over, so you adjust the yaw to the opposite angle a little, which confuse the odometry. The lane we are following has 4 right turns, so it’s easy to get errors at each turn and drift to the right.

2. Did adding the landmarks make it easier to understand where and when the odometry drifted?

Yes, adding the landmarks is very easy to see the current location of our Duckiebot and get to know where and when it is drifted.

### Section 3.3

In this section, we need to obtain a transform tree graph, which is a tree structure with nodes being different frames and edges being transformations.

To generate the graph, we did the following procedure:

1. Go to dashboard
2. Open portainer
3. Open a console of the ROS container
4. Install ros-noetic-tf2-tools
5. Run `rosrun tf2_tools view_frames.py` to get the PDF file 
6. Copy it to /data and download it.

The transform tree graph looks like this, you can see the root is `vehicle_name/footprint`

![transform graph tree](/uploads/transform_graph_1.png)

### Section 3.4

For this section, we can visualize all the frames in the Duckiebot using RViz, and figure out which joint is responsible for rotating the wheels.

#### Question

1. What's the type of joint that moves when we move the wheels?

The joint is continuous. Since we need to **rotate** the wheel to move it and a continuous joint can rotate around the axis and has no upper and lower limits.

### Section 3.5

In this section, we want to see both the frames on a Duckiebot, and it should also change the location and orientation in the world frame if we move it. To do this, we let the parent frame be the odometry frame and the child frame be the `/footprint frame`, since the odometry frame is the child to the world frame, the root is now the world frame. The image below shows the current transform graph:

![transform graph tree 2](/uploads/transform_graph_2.png)


The reason why no frame is moving is that we are now using the baselink frame (`/footprint`) of the Duckiebot, whenever you move the robot, the frame will also be there and the relative location of different frames on a Duckiebot will be the same.

#### Questions

1. What should the translation and rotation be from the odometry child to robot parent frame? In what situation would you have to use something different?

The translation and rotation should all be zero. We should consider changing the values when the robot root frame is not the same as the odometry frame.

2. After creating this link generate a new transform tree graph. What is the new root/parent frame for your environment?

The new root is `/world`, the world frame.

3. Can a frame have two parents? What is your reasoning for this?

No, a frame cannot have two parents. The transform tree graph means, for every two nodes in the same tree, it is possible to have a transformation between them, but if you have two parents of the same frame, you cannot have a transformation that transforms one to another. And TF expects a tree structure and cannot deal with the case that has multiple parents.

4. Can an environment have more than one parent/root frame?

Yes, an environment can have more than one parent frame, just like before 3.5, we have a parent world frame with child AprilTag static frames and the odometry frame. And another parent footprint frame with a couple of other frames on the robot. And you cannot have one frame in a tree that transforms into another frame in another tree.

### Section 3.6

The video below shows how the robot moves in the world frame, where are the estimated location of the AprilTags, and the ground truth locations visualized by RViz. The delay is high since at the time we record this video, there were many people working in the lab causing high network contention. The estimated location of the AprilTags is obtained in the following way:

1. We have the rotation and location information in the camera frame from the raw image
2. Then we transformed that from the camera frame to the estimated location relative to the camera frame. You can also see all the frames on the robot are also moving as the robot moves, that's because in section 3.5 we attached the odometry frame with the robot root frame.

{{< rawhtml >}}
<iframe src="https://drive.google.com/file/d/1qPbVoIe3fzPE6ydsNJZNGGuvadNQeenC/preview" width="640" height="480" allow="autoplay"></iframe>
{{< /rawhtml >}}

#### Questions

1. How far off are your detections from the static ground truth?

If an AprilTag is detected in the image, the estimated AprilTag's frame will show up in RViz immediately. One issue with our design is that after one detection disappeared from the image, the last broadcasted frame will still be there and it will also rotate and move relative to the camera until we have a new April tag detected.

The error between the ground truth and the estimation is within 20 centimeters, if there's a tag detected in the current image.

2. What are two factors that could cause this error?

- The resolution of the image can be low, since we can control the resolution of the image we pass to the detector, the higher it is, the more computation we will do, the more accurate location of the tag we can obtain (corner, edge...)

- The light and the angle at that the camera observes the tag also matter. The dimmer the room is, the smaller the angle is, the harder for the camera to estimate its location and other information.

### Section 3.7

This section combines the previous sections were we use camera input as the sensor fusion to help localize our robot in the Duckietown.

The robot travels along the lane shown in the image below, when it detects an Apriltag, it will estimate its location based on the tag's information. When no Apriltag is available, it will just use odometry.

![duckietown environment](/uploads/duckietown_env.png)

From the video below, you can see in the RViz window, all the April tag frames and all the frames on the Duckiebot are visualized, along with the greyscaled, undistorted camera input that shows where the robot it and what it sees

{{< rawhtml >}}
<iframe src="https://drive.google.com/file/d/1ODkNdsQbXfnpIHm4olukFoFHA5_r3sLg/preview" width="640" height="480" allow="autoplay"></iframe>
{{< /rawhtml >}}

The network was slow at the time we record the video so sometimes the delay can be high. We were using keyboard control to make it move. As you can see in the video, each time when it detects a tag, it will transport it to a more accurate location in the world, the robot is located at the place where a lot of different frames overlapping together since we are also displaying other frames on the robot. Due to the wifi's problem, it sometimes takes a while for the robot to transport it to the right location and publish the current camera image.

With the help of the sensor fusion, now the robot travels pretty well, there's only a minor difference between the end location and the start location, and that is also because the wifi is slow so we need to decrease the frequency of the detection and use more odometry.

#### Questions

1. Is this a perfect system?

Of course not. Although we are using geometry to calculate where the robot actually is in the world frame based on sensor fusion, the detection is not in real-time so there might be a delay for updating location, and the geometry can also bring larger error if the robot is observing the tag in a large angle (look from the side).

2. What are the causes for some of the errors?

- Wifi. There were a lot of people at the lab when we record the videos, sometimes I failed to build my images and connect to my robot. Because of this, I decreased the detection frequency to 1 per second and use more odometry, which prunes to errors sometimes.
- The estimated April tag location based on the detection result. There's always going to be an error here since you cannot estimate the tag location perfectly.

3. What other approaches could you use to improve localization?

- It would be nice to have more than one camera, just like when you use 2 eyes to observe the world, you can always get a better sense of where things are located, then you can get a better sense of where you are located. 
- Use lane following instead of keyboard control. Control the robot manually usually make the odometry more confusing since you can accidentally make a turn too over and need to adjust back to the right direction, I did this multiple times and it always makes the odometry lost completely.
- Optimize our detector to make it faster.

# What I learned from this exercise

For this exercise I learned how to implement PID control for following the lanes within Duckietown. Moreover, I learned how to reuse the existing lane following pipeline to implement my own lane following node using PID control.

# Repo Link

[Exercise 3 repository link](https://github.com/liqianxi/503_ex3)

# References

This is a list of references that I used to do this exercise.

1. Lane Controller Node: https://github.com/duckietown/dt-core/blob/6d8e99a5849737f86cab72b04fd2b449528226be/packages/lane_control/src/lane_controller_node.py
2. Lane Controller: https://github.com/duckietown/dt-core/blob/6d8e99a5849737f86cab72b04fd2b449528226be/packages/lane_control/include/lane_controller/controller.py
3. PID Controller: https://en.wikipedia.org/wiki/PID_controller
4. PID controller code: https://github.com/jellevos/simple-ros-pid/blob/master/simple_pid/PID.py
5. Qianxi Li's website: https://sites.google.com/ualberta.ca/qianxi-duckie/exercises/exercise-3
6. URDF Joints: http://wiki.ros.org/urdf/XML/joint
7. URDF parameters for the Duckiebot: https://github.com/duckietown/dt-duckiebot-interface/blob/56a299aa5739e7f03a6b96d3b8dac3a8beca532c/packages/duckiebot_interface/urdf/duckiebot.urdf.xacro
8. TF2: http://wiki.ros.org/tf2/Tutorials/Introduction%20to%20tf2
9. TF2 Static Broadcaster: http://wiki.ros.org/tf2/Tutorials/Writing%20a%20tf2%20static%20broadcaster%20%28Python%29
10. TF transformations: http://wiki.ros.org/tf/Overview/Transformations
11. Sensor Fusion: https://docs.duckietown.org/daffy/duckietown-classical-robotics/out/exercise_sensor_fusion.html#fig:rviz-final-tf-tree
12. AprilTag with Python: https://pyimagesearch.com/2020/11/02/apriltag-with-python/