# screensaver_demo_code.py -- demonstrate screensaver use
# 17 Aug 2021
# 5 Apr 2024 - @DJDevon3 - Demo for non-built-in display using ST7796S

import time
import board
import displayio
import fourwire
from circuitpython_st7796s import ST7796S
from screensaver import screensaver_dvdlogo

spi = board.SPI()
tft_cs = board.D9
tft_dc = board.D10
tft_rst = board.D17

# 3.5" ST7796S Display
DISPLAY_WIDTH = 480
DISPLAY_HEIGHT = 320

displayio.release_displays()
display_bus = fourwire.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)
display = ST7796S(display_bus, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, rotation=180)

# This is our main loop
# where we do our very important work
while True:
    for i in range(20):
        print(time.monotonic(),"doing busy work...")
        time.sleep(0.3)

    # but now it's time for a break
    print("*** now screensavering")

    # how to get out of the screensaver
    saver_time = time.monotonic()
    def exit_screensaver():
        return (time.monotonic() - saver_time > 10) # allow 10 secs of savering

    screensaver_dvdlogo(display=display, should_exit_func=exit_screensaver )
    
    # back to work
    display.auto_refresh=True
