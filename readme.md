# train-control

Train Control is just that - a python train controller designed for running on a pcduino using a basic motor driver

## Progress

At this point we can make a train move, and can interface the application using the web interface.

- [x] GPIO interface files
- [x] abstraction of GPIO interface (ie: fwd(), rev(), etc.)
- [x] command line interface
- [x] pwm driver
- [ ] switch driver
- [x] network driver
- [ ] prettify network GUI (add images, make easier to see, perhaps an overlay of the layout on top, etc)
- [ ] lighting driver (add lighting abilites on GPIO pins)
- [ ] lighting abstraction for GPIO
- [ ] interface for lighting on GUI

## GPIO Information

Checked if pin currently connected (todo if not done)

Pins 2-7 are planned for lighting

- [ ] 2
- [ ] 3
- [ ] 4
- [ ] 5
- [ ] 6
- [ ] 7

- [x] 8 - Switch left (todo)
- [x] 9 - Switch enable (todo)
- [x] 10 - Train enable/pwm
- [x] 11 - Switch right (todo)
- [x] 12 - Train FWD
- [x] 13 - Train REV

There is also another header P10 with 4 more GPIO pins

This might get used for lighting also? Might be difficult to access with shield

- [ ] 14
- [ ] 15
- [ ] 16
- [ ] 17

No uses yet for analog pins

## Credits

Kudos to the folks at Sparkfun for their basic [python GPIO code](https://github.com/sparkfun/pcDuino/blob/master/examples/gpio/gpio_test.py). It works wonders for interfacing the GPIO

