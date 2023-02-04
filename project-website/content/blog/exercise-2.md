---
author: "Jihoon Og"
title: "Exercise 2"
date: 
description: "Second Lab Assignment"
tags: ["bulding","programming", "ROS", "docker","odometry"]
categories: ["robot"]
ShowRelated: false
showToc: true
math: true
ShowBreadCrumbs: false
---
This is the second lab assignment of the course.

# Part 1

## Screenshots

### Screenshot of the new image subscriber

![image sub](/uploads/new_node_rqt_image_view.png)

### Screenshot of the source code of the image subscriber

![image sub code](/uploads/new_subpub_node.png)

## Questions and Answers

1. What is the relation between your initial robot frame and world frame? How do you transform between them?

The initial world frame is 0.32, 0.32 in the x and y coordinates respectively and the theta component is
{{< rawhtml >}}
\(\dfrac{1*\pi}{2}\)
{{< /rawhtml >}}.
The robot frame is 0, 0 for the x and y coordinates respectively with the theta component being the same. We can convert between the two frames using a forward and reverse kinematics equation.
To convert between the world frame to the robot frame we use this equation:

$$
\begin{bmatrix}\dot{x_I}\\\\\dot{y_I}\\\\\dot{\theta_I}\\ \end{bmatrix}  = \begin{bmatrix}\cos(\theta) & -\sin(\theta) & 0\\\sin(\theta) & \cos(\theta) & 0\\\\ 0 & 0 & 1\\ \end{bmatrix} \begin{bmatrix}   \dot{x_R}\\\\\dot{y_R}\\\\\dot{\theta_R}\\ \end{bmatrix}
$$

2. How do you convert the location and theta at the initial robot frame to the world frame?

To convert between the robot frame to the world frame we use this equation:

$$
\begin{bmatrix}\dot{x_R}\\\\\dot{y_R}\\\\\dot{\theta_R}\\ \end{bmatrix}  = \begin{bmatrix}\cos(\theta) & \sin(\theta) & 0\\\\ -\sin(\theta) & \cos(\theta) & 0\\\\ 0 & 0 & 1\\ \end{bmatrix} \begin{bmatrix}   \dot{x_I}\\\\\dot{y_I}\\\\\dot{\theta_I}\\ \end{bmatrix}
$$

3. Can you explain why there is a difference between actual and desired location?

There could be many factors that could cause an error between the true location and the desired location. Some of these factors could include:

- Wheel slip.
- Loose tolerances within the encoders.
- Non consistent driving surface.
- No feedback mechanism to check if the motors moved the desired amount.
- Overshooting and undershooting of the desired target distance. 

4. Which topic(s) did you use to make the robot move? How did you figure out the topic that could make the motor move?

We used the `/hostname/wheels_driver_node/wheels_cmd` and published `WheelsCmdStamped` messages to move the left and right motors at a desired velocity. We figured that this topic would move the robot as we looked at the list of all available topics using `rostopic list` and using intuition guessed that this topic will move the wheels based on the descriptive topic name.

5. Which speed are you using? What happens if you increase/decrease the speed?

We used a value of `0.5` for forward movement and `0.25` for rotational movement. If we increase the speed the robot will move faster but runs the risk of overshooting the desired distance. However, decreasing the speed could prevent the robot from moving as the static friction is greater the motor's torque for the given wheel. 

6. How did you keep track of the angle rotated?

By using the following kinematic equation below:

$$\begin{bmatrix}\dot{x}_R \\\\\dot{y}_R \\\\\dot{\theta}_R \\\\ \end{bmatrix} = \begin{bmatrix}   \frac{r\dot{\varphi}_r}{2} + \frac{r\dot{\varphi}_l}{2} \\\\   0  \\\\    \frac{r\dot{\varphi}_r}{2\cdot l} - \frac{r\dot{\varphi}_l}{2\cdot l} \\\\ \end{bmatrix}$$

We can find the change of the robot's directional pose based on the left and right wheels' linear distance change.

7. Which topic(s) did you use to make the robot rotate?

We used the same topic to rotate the robot as to move the robot forward.

8. How did you estimate/track the angles your duckieBot has traveled?

Using the equation listed from the previous answer for question 6. We added all the changes of the robot's angle to the initial angle the robot started with throughout the whole execution of the robot's movement.

# Part 2

1. What is the final location of your robot as shown in your odometry reading?

The final location of the robot is: 0.2, 0.4, 90 degress for x, y, and theta respectively

1. Is it close to your robot’s actual physical location in the mat world frame?

It's sometimes reasonably close. Within 30 centimeters.