# Exercise 1

Exercise 1 is an intro lab where we built our own robot and drove around our own Duckietown. We also ran the built-in lane following program.

## Running the demo

Assuming you have a built, and calibrated Duckiebot as well as having the `dts` software you can run the lane following demo by calling this in the repo's root directoy

```bash
dts duckiebot demo --demo_name lane_following --duckiebot_name csc22935 --package_name duckietown_demos
```

Color detection is not implemented due to a runtime issue.