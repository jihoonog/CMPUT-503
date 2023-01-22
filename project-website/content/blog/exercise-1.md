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
Because I have my own domain `forkprocess.com` I wanted to use it to point it to my course website. I use subdomains to access external web services so I created a new subdomain `quackquack` that will point to project's website that is being hosted on GitHub. For deployment I used GitHub Actions to build the content of the site and deploy it automatically once something has been committed to the main repo.

Also, after working with Jekyll for a little bit I decided to move to Hugo as it was a framework that I was much more familiar with and can generate a blog style site faster with more diversity of themes.

## Assembling the robot

Assembling the robot wasn't too bad except for inserting the metal nuts into the chassis. I had to file down the inserts a bit so it can accept the metal nuts more easily.

Other then that I was able to assemble the robot in about 3 hours.

## Flashing the SD card

Flashing the SD card wasn't too bad it was just long. Running this command `dts init_sd_card --hostname csc22935 --type duckiebot --configuration DB21M --wifi 'DuckieNet:CMPUT412_1234!!!Rox' --no-steps verify` took a little over an hour to finish. I skipped the verification step because it takes a while to do and I felt confident that the sd card flashed properly. 

Note: I had to do this multiple times because I had issues getting my bot to move/boot. To improve the process I kept the compressed image file for the Nvidia Jetson Nano used in the Duckiebot within my home directory, and copy the file over to the `tmp` working space that the `init_sd_card` program used for downloading and unpacking the image file.

## Dashboard

After the first boot I was able to connect to my Duckiebot's dashboard by loading it in my web browser by accessing `csc22935.local` or the hostname of my Duckiebot. After the initial setup I was able to see the motor commands and camera output on the dashboard as shown below.

![Duckiebot Dashboard](https://user-images.githubusercontent.com/25281309/213753468-49cb40f8-4640-4e86-8d48-ab5757ff36db.png)

## Getting the robot to move and debugging pain

At first the robot didn't move using `dts duckiebot keyboard_control`. 
I followed the debugging steps, checking to see if the `duckiebot-interface` is up and running. Then when that didn't resolve the problem I updated the containers which lead to other issues due to what I initially thought my docker package being incompatible with this version of `dts`. So I uninstalled everything and reflashed the SD card again to double check nothing when wrong during installation, same issue. Then I tried to update the Duckiebot firmware by using `dts duckiebot update` which lead to another issue this time an 500 server error that I originally thought was caused by docker installation as well.

Well after many hours spent debugging the issues, doing multiple SD card reflashes and software reinstallations, I found that the problems were not from a single core issue but from multiple, seemly independent sources, here is a list to keep things brief:

- 500 Server Error: Removed my DockerHub credentials from the `dts` config file as that was interfering with the login process that was giving the 500 server error.
- Never apt-get upgrade on the Duckiebot itself as it will brink the entire system, use the `dts duckiebot upgrade` command instead
- The HUT needed to be reflashed again as it was running the wrong version but was reporting the latest version on the dashboard, thus wasn't a clue at first.
- If the WiFi disconnects it's easier to remove the WiFi adapter and plug it back in as the hotplug parameter was set during initialization therefore it will try and reconnect once the adapter is reconnected into the USB port. 
- Don't let your battery get too low otherwise it will lead to unexpected behaviors like improper shutdowns and WiFi disconnections. 
- Make sure that all your micro USB cables are connected properly so that it can power on properly and prevent unnecessary SD card reflashes.

## Calibrating the motors

Following the guide on calibrating the motors I drove the robot in a straight line to see the drift. It it drifted left then I would decrease the trim value and if it drifted right I would increase the trim value.
The trim parameter is a ratio of how much one motor should move compare to the other. If `trim > 0` then the right motor will spin faster compared to the left and vice versa. 
The gain parameter is a scalar value applied to both motors on how much to spin based on the commanded signal. There is a careful balancing act between having enough gain that the robot will move when commanded at the lowest speed but lower enough that any errors aren't amplified to be unpredictable.
For both values I used binary search to find a good enough trim value such that the robot would travel straight with at most a 10 cm drift driving 2 meters. The values I settled on for `trim = 0.0515` and `gain = 0.85`. The video below shows the straight line performance of the robot using these values. 

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

Intrinsic calibration takes into accound the small manufacturing discrepancies the lens and the sensor will have on an image. By moving the camera or bot back and forth, side to side, up and down, rotating off plane, etc I was able to get the calibration software to learn about these discrepances and make adjustments to the raw outputs so they accurately replicate reality.
Extrinsic calibration tries to learn the camera's location in 3-D space, how it's positioned and how it's rotated. This is important for trying to find the lane markings in Duckietown.
## Lane following

Running the lane following demo was fairly easy I made sure that both `duckiebot-interface` and `car-interface` was running and start the lane following container by running this command in `dts`:
```bash
dts duckiebot demo --demo_name lane_following --duckiebot_name csc22935 --package_name duckietown_demos
```
Once the container was running I opened the keyboard control for my bot and pressed the `a` key to start the lane following demo. The video below shows the lane following demo in action:

{{< youtube T9IJy8rgorI >}}

Note: I had to tune the parameters so that I can make the turns in duckietown. I had to increase the `k_theta` and `k_d` values a little bit so the robot can turn more aggressively and make the turns without going over the lines.

## Colour Detection

This was the most difficult part of the exercise, something I put way too much effort into when we are not going to use this code base for anything as we are going to use ROS to get the images from the camera node, but it was a good exercise nonetheless. I followed the instructions from the basic development guide from Duckietown and found that a lot of the documentation was outdated. Particularly the GStreamer pipeline code was not for the DB21 platform. I found the correct GStreamer pipeline code from the `dt-duckiebot-interface` repository and used that to open the camera. However, this still lead to an issue initialization the camera in OpenCV. I think the main issue is caused by missing runtime environments that GStreamer requires that isn't being initialized by Dockerfile. I might be able to find the correct initialization procedure in the `dt-duckiebot-interface` repository but at this point I spent too much time trying to get this minor code to work. So I just ignored it for now.
