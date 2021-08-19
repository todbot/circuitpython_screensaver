# circuitpython_screensaver
Do you need a screensaver for CircuitPython? Of course you do

Demo video of dvdlogo screensaver:

https://user-images.githubusercontent.com/274093/129969608-a1ea6c81-c9af-4391-923e-143fcaf08a24.mp4

Demo video of flyingtoasters screensaver:

https://user-images.githubusercontent.com/274093/129991271-908bda7a-8aca-4b34-a2d6-8dba57bfbeea.mp4


For more info, see [this tweet thread](https://twitter.com/todbot/status/1428096525217931264).

## Installation

- Copy the entire `screensaver` directory to your CIRCUITPY drive
- See the `demo_code.py` example (or just copy it over as `code.py`) to see how to use it

## Usage

To load up a screensaver and run the screensaver forever:

```py
from screensaver import screensaver_dvdlogo
screensaver_dvdlogo()
```

or

```py
from screensaver import screensaver_flyingtoasters
screensaver_flyingtoasters()

```

or

```py
from screensaver import screensaver_boingball
screensaver_boingball()

```

To make a screensaver stop after a condition is met, pass in a function as the
`should_exit_func` parameter. If this function returns `True` the screensaver
exits.

For example. this `exit_screensaver()` function returns `True` after 10 seconds:

```py
saver_time = time.monotonic()
def exit_screensaver():
  return (time.monotonic() - saver_time > 10) # allow 10 secs of savering

screensaver_dvdlogo( should_exit_func=exit_screensaver )
```

## Notes

- Assumes CircuitPython 7, but only for `rainbowio`. And should work in CP6.

