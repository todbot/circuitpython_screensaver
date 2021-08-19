
# screensaver.py -- screensavers for CircuitPython
# 17 Aug 2021 - @todbot
#
import time, random
import board, displayio
import adafruit_imageload

try:
    import rainbowio
    def randcolor(): return rainbowio.colorwheel(random.randint(0,255))
except ImportError:
    def randcolor(): return random.randint(0,0xffffff) # not as good but passable

# dvdlogo! currently our main screensaver
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
    vx,vy = display.width / 100, display.height / 150 # initial velocity that seems cool
    
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


# flying toasters!
def screensaver_flyingtoasters(display=board.DISPLAY, should_exit_func=None):

    sprite_w = 48 # width of the sprites
    sprite1_fname="/screensaver/toast_48.bmp"
    sprite2_fname="/screensaver/toaster_48.bmp"
    sprite2_tile_count = 4

    display.auto_refresh = False  # only update display on display.refresh()
    screen = displayio.Group()  # group that holds everything
    display.show(screen) # add main group to display

    sprite1,sprite1_pal = adafruit_imageload.load(sprite1_fname)
    sprite1_pal.make_transparent(0)
    sprite2,sprite2_pal = adafruit_imageload.load(sprite2_fname)
    sprite2_pal.make_transparent(0)

    sprite_hw = sprite_w//2  # integer half-width of our sprite, for bounce detection

    class Sprite:
        def __init__(self, tg, x,y, vx,vy, tile_count=1, anim_speed=0):
            self.tg = tg
            self.x,self.y = x,y
            self.vx,self.vy = vx,vy
            self.tile_count = tile_count
            self.anim_speed = anim_speed
            self.last_time = time.monotonic()
        def update_pos(self):
            self.x = self.x + self.vx
            self.y = self.y + self.vy
            # TileGrids are top-left referenced, so subtract that off
            # and convert to integer pixel x,y before setting tilegrid xy
            self.tg.x = int(self.x - sprite_hw)
            self.tg.y = int(self.y - sprite_hw)
        def next_tile(self):
            if self.tile_count == 1: return
            if time.monotonic() - self.last_time > self.anim_speed:
                self.last_time = time.monotonic()
                tilenum = (toaster.tg[0] + 1) % toaster.tile_count
                toaster.tg[0] = tilenum

    toasts = []
    for i in range(3):
        x,y = random.randint(0,display.width), random.randint(0,display.height)
        vx,vy = -1.4 - random.uniform(0,0.8), 1 # standard toast velocity direction
        tg = displayio.TileGrid(sprite1, pixel_shader=sprite1_pal)
        sprite = Sprite(tg, x,y, vx,vy, 1)
        toasts.append( sprite )
        screen.append(tg)

    toasters = []
    for i in range(2):
        x,y = random.randint(0,display.width), random.randint(0,display.height)
        vx,vy = -1.3 - random.random(), 1 # standard toast velocity direction
        tg = displayio.TileGrid(sprite2, pixel_shader=sprite2_pal,
                                width=1, height=1,
                                tile_width=sprite_w, tile_height=sprite_w)
        sprite = Sprite(tg, x,y, vx,vy, tile_count=sprite2_tile_count, anim_speed=0.1)
        sprite.tg[0] = random.randint(0, sprite2_tile_count-1) # randomize anim sequence
        toasters.append(sprite)
        screen.append(tg)

    flap_time = time.monotonic()
    while True:
        if should_exit_func is not None and should_exit_func(): return

        # update our position based on our velocity
        for toast in toasts:
            toast.update_pos()
            if toast.x < 0 or toast.y > display.height:
                toast.x = display.width
                toast.y = random.randint(0,display.height)/2

        for toaster in toasters:
            toaster.update_pos()
            toaster.next_tile()
            if toaster.x < 0 or toaster.y > display.height:
                toaster.x = display.width
                toaster.y = random.randint(0,display.height)/2
                toaster.tg[0] = random.randint(0, sprite2_tile_count-1)

        # this gives framerate of 20-24 FPS on FunHouse (ESP32S2 240x240 SPI TFT)
        display.refresh(); time.sleep(0.01)
