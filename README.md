# CMPUT-503
Experimental Mobile Robotics Graduate Course

## How to run the programs

Each lab submissions are in their own sub-directory within this repo. Most of these sub-directories are submodules from other repositories, to clone them it is much easier to clone this repo with the `--recurse-submodules` flag. i.e., `git clone --recurse-submodules https://github.com/jihoonog/CMPUT-503.git`.

If you accidentally clone the repo without the flag then you can run `git submodule update --init` at the root of the repository to clone all the submodules.

Each sub-directory will have their own README on how to run their programs or packages.

## Exercise 1

Exercise 1 is an intro lab where we (grad students) had to build our own Duckiebot and learn how to use the Duckiebot software stack.

## Exercise 2

Exercise 2 is where we made our own custom ROS nodes for moving the robot around the lab's Duckietown.

## Exercise 3

Exercise 3 is where we implement our own computer vision and sensor fusion for localization and lane following.

## Exercise 4

Exercise 4 is where we implement a crash avoidance and leader following mechanism for our Duckiebots. It's a combination of work from previous exercises.

## Exercise 5

Exercise 5 is where we implement a machine learning model that can detect single numerical digits posted around Duckietown.

## Final Project

For our final project we combined all that we've learned from the previous exercise to program our bot to drive through a driving course and park at the end.
