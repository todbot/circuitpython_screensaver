
# screensaver.py -- dvdlogo screensaver for CircuitPython
# 17 Aug 2021 - @todbot
#
import time, random
import board, displayio, rainbowio  
import adafruit_imageload

try:
    import rainbowio
    def randcolor(): return rainbowio.colorwheel(random.randint(0,255))
except ImportError:
    def randcolor(): return random.randint(0,0xffffff) # not as good but passable

# currently our only screensaver
def screensaver_dvdlogo(display=board.DISPLAY, should_exit_func=None):

    sprite_w = 70 # width of the sprite to create
    sprite_fname="/screensaver/dvdlogo_70.bmp"

    display.auto_refresh = False  # only update display on display.refresh()
    screen = displayio.Group()  # group that holds everything
    display.show(screen) # add main group to display

    sprite1,sprite1_pal = adafruit_imageload.load(sprite_fname)
    sprite1_pal.make_transparent(0)
    sprite1_tg = displayio.TileGrid(sprite1, pixel_shader=sprite1_pal)
    screen.append(sprite1_tg)

    x, y = display.width/2, display.height/2 # starting position, middle of screen
    vx,vy = 2.5, 1.8  # initial velocity, seems cool
    
    sprite_hw = sprite_w//2  # integer half-width of our sprite, for bounce detection

    while True:
        if should_exit_func is not None and should_exit_func(): return
        # update our position based on our velocity
        x,y  = x + vx, y + vy
        # x,y is centered on our sprite, so to check bounds
        # add in half-width to get at edges
        # a bounce just changes the polarity of the velocity 
        if x - sprite_hw < 0 or x + sprite_hw > display.width:
            vx = -vx  # bounce!
            sprite1_pal[1] = randcolor() # rainbowio.colorwheel(random.randint(0,255))
        if y - sprite_hw < 0 or y + sprite_hw > display.height:
            vy = -vy  # bounce!
            sprite1_pal[1] = randcolor() # rainbowio.colorwheel(random.randint(0,255))
        # TileGrids are top-left referenced, so subtract that off
        # and convert to integer pixel x,y before setting tilegrid xy
        sprite1_tg.x = int(x - sprite_hw)
        sprite1_tg.y = int(y - sprite_hw)
    
        # this gives framerate of 20-24 FPS on FunHouse (ESP32S2 240x240 SPI TFT)
        display.refresh(); time.sleep(0.01)
        # whereas this is jerky: every other frame 11 FPS & 0 FPS, at 20 FPS rate
        #display.refresh(target_frames_per_second=20, minimum_frames_per_second=0)

