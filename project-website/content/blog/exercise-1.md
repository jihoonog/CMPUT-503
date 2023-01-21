---
author: "Jihoon Og"
title: "Exercise 1"
date: 2023-01-20T19:24:50-07:00
description: "First Lab Assignment"
tags: ["bulding","programming", "linux", "docker"]
categories: ["robot"]
ShowRelated: false
showToc: true
ShowBreadCrumbs: false
---
This is the first lab assignment of the course. Graduate students needed to build their Duckiebots as well as flash the SD card and demonstrate moving the robot in a straight line and show that it can stay within a lane using the built-in Duckiebot lane-following module.
## Setting up the website

Setting up the website wasn't too difficult as it was just following the instructions on GitHub Pages with Jekyll.
Installing Jekyll wasn't too bad on my system just needed to install Ruby and install the framework using Gem.
Because I have my own domain `forkprocess.com` I wanted to use it to point it to my course website. I use subdomains to access different services so I create a new subdomain `quackquack` that will point to project's website that is being hosted on GitHub.

I use GitHub Actions to build the content that is stored on the website directory of the repo to to build and deploy the site when the repo is updated.

## Assembling the robot

Assembling the robot wasn't too bad except for inserting the metal nuts into the chassis. I had to file down the inserts a bit so it can accept the metal nuts more easily.

Other then that I was able to assemble the robot in about 3 hours.

## Flashing the SD card

Flashing the SD card wasn't too bad it was just long. Running this command `dts init_sd_card --hostname csc22935 --type duckiebot --configuration DB21M --wifi 'DuckieNet:CMPUT412_1234!!!Rox' --no-steps verify`. Took a little over an hour to finish flashing the SD card. I skipped the verification step because it takes a while to do and I feel confident enough that it flashed properly.

Note: I had to do this multiple times because I had issues getting my bot to move but that will be described later.


## Dashboard

![Duckiebot Dashboard](https://user-images.githubusercontent.com/25281309/213753468-49cb40f8-4640-4e86-8d48-ab5757ff36db.png)

## Getting the robot to move

At first the robot didn't move using `dts duckiebot keyboard_control`. 
I followed the debugging steps, checking to see if the `duckiebot-interface` is up and running. Updating the containers which lead to other issues due to my docker package being incompatible with this version of `dts`. Basically, the issue was that my HUT firmware was broken and needed to be updated. I followed the guide on updating the HUT firmware using their docs, reboot the duckiebot, tried the keyboard control again and finally after hours of debugging and many SD reflashes the duckiebot seems to move. 

## Calibrating the motors

Following the guide on calibrating the motors I drove the robot in a straight line to see the drift. It it drifted left then I would decrease the trim value and if it drifted right I would increase the trim value. I basically used binary search to find a good enough trim value such that the robot would travel straight with at most a 10 cm drift driving 2 meters.
I also set the gain value to 0.85 to make it easier for the robot to drive in a straight line.

{{< youtube _oTIF_Z0tsU >}}
## Calibrating the camera

Calibrating the camera was pretty easy. Following the instructions outlined in the Duckiebot documentation. I was able to calibrate both the intrinsic and extrinsic values of the robot by calling:
```bash
dts duckiebot calibrate_intrinsics csc22935
```
and
```bash
dts duckiebot calibrate_extrinsics csc22935 
```
and follow the instructions outlined from the terminal.


## Lane following

{{< youtube T9IJy8rgorI >}}
