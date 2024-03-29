Python Robotics Simulator
================================

This is a simple, portable robot simulator developed by [Student Robotics](https://studentrobotics.org).


## General idea about the simulator
-----------------------------------
The main idea of this code is to control a robot in a way that will always grab the silver token and not the golden ones, while it will turn under specific conditions and angles that we set in this code once it detects a golden token. All these conditions and actions will be done due to some functions used in this code, like the function 'R.see' that will detect the type of the token and some will return values like the distances and angles between the robot and a specific token, and others will return right and left distances that will help on turning the robot where he has more space to do so. 

How to install and run the code?
--------------------------------

The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).


To run one or more scripts in the simulator, use `run.py`, passing it the file names. 

When done, you can run the program with:

```bash
$ python run.py Assignment1_pia.py
```

Robot API
---------

The API for controlling a simulated robot is designed to if the distance
 between
the robot and the
 silver token is
 less than 1 and the angle
between them
is less than 85be as similar as possible to the [SR API][sr-api].

### Motors ###

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

### The Grabber ###

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.

### Vision ###

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

For example, the following code lists all of the markers the robot can see:

```python
markers = R.see()
print "I can see", len(markers), "markers:"

for m in markers:
    if m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER):
        print " - Token {0} is {1} metres away".format( m.info.offset, m.dist )
    elif m.info.marker_type == MARKER_ARENA:
        print " - Arena marker {0} is {1} metres away".format( m.info.offset, m.dist )
```

[sr-api]: https://studentrobotics.org/docs/programming/sr/  

Describing the flowchart 
-------------------------

![Flowchart-RT1-Assignment1 (1)](https://user-images.githubusercontent.com/94491181/142486425-a486f0be-6fb5-47ce-b4e7-83525b9947b2.jpg)

Here is the procedure of a robot following a specific path in a way to grab the silver token and turn once a golden one is detected.

Firstly,the robot will start by driving below the path, then by receiving the distances and angles of each token returned from a function.

Therefore, it will start by comparing the distance between the golden token and the robot from a fixed distance chosen by the programer,if its less than this fixed one and the angle between this token and the robot is also less than 75 degrees then, the robot has to check now if the distance between the silver token and the robot is less than 1 and if the angle between them is less than 85 degrees.This means that a silver token is near the robot so he should drive toward the token and grab it.Else,the robot has to check the nearest golden tokens on his left and right, in such a way that he will have to go where there is more space due to a function used in the code which is 'R.see' that will return the distances on the right and on the left of the robot and compared them together.Thus the robot will take the direction  where the distance is greater and drive toward it.

Secondly, if the distance between the robot and the golden token is greater than the fixed distance and the angle between them is greater tahn 75 then it will check the distance and angle between the silver one, so if silver token detected, the robot will drive and go to grab it, else if no silver token is detected, then the robot just has to drive following the path.

Noting that, after all these steps, we have a loop  where the procedure will be repeated.


Possible Improvement:
---------------------
Autonomous path planning is the most important issue which must be resolved first in the process of improving robotic manipulator intelligence. This can be done by using the RRT algorithm which stands for a rapidly exploring random tree. It's an algorithm used to high-dimensional spaces by randomly building a space-filling tree. It can do both, creates and finds a path, in addition it aims to achieve a shortest path.RRT's logic is very simple and straight forward, each vertex (highest point) will be created,a check is made such that the vertex lies outside of an obstacle,The algorithm ends when a node is generated within the goal region
![ezgif com-gif-maker](https://user-images.githubusercontent.com/94491181/142485633-26255c0f-2772-4637-b7d9-9a867c202cdc.jpg)
