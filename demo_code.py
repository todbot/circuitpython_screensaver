# screensaver_demo_code.py -- demonstrate screensaver use
# 17 Aug 2021

import time  # time is money

from screensaver import screensaver_dvdlogo

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

    screensaver_dvdlogo( should_exit_func=exit_screensaver )
    
    # back to work
    board.DISPLAY.auto_refresh=True
    board.DISPLAY.show(None)
    
