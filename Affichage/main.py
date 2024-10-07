# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

#import open3d as o3d
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import tkinter as tk
from ursina import *
import datetime as tm

class RocketObject(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        #self.name = name
        self.model = None
        self.position = np.array([0,0,0])
        self.previous_position = np.array([0, 0, 0])
        self.satellite = 0
        self.speed = 0
        self.time = None

        self.current_orientation = np.array([0,0,0])
        self.target_orientation = np.array([0, 0, 0])

        for key, value in kwargs.items():
            setattr(self, key, value)

        def input(self, key):
            if key == 'space':
                self.animate_x(2, duration=1)

        def update(self):
            self.x += held_keys['d'] * time.dt * 10
            self.x -= held_keys['a'] * time.dt * 10




def update():
    """
    Function is called each frame.
    :return:
    """

    #Change rotation of 3d rocket object
    rocket.rotation_x +=20*time.dt

    #test.text = str(tm.datetime.now())[:-5]

    #Change value of altitude
    altitude.alt_value += 1
    altitude.set_altitude(altitude.alt_value)
    altitude.update_vertical_display()

    #Change value of rotation
    rotation.roll = 10
    rotation.yaw = 10
    rotation.pitch = 10
    rotation.update()
    maxima.update(altitude.alt_value)

    #alt = altitude.vertical_altitude.anchor.position_getter()

    #altitude.vertical_altitude.anchor.position_setter((alt[0], -altitude.alt_value*0.00225, alt[2]))
    None



def launch_app():
    app = Ursina(
        title='Hemera',
    )
    """
    button_list = ButtonList(
        {
            'widow.position = Vec2(0,0)': Func(setattr, window, 'position', Vec2(0, 0)),
            'widow.size = Vec2(512,512)': Func(setattr, window, 'size', Vec2(512, 512)),
            'widow.center_on_screen()': window.center_on_screen,

            'widow.borderless = True': Func(setattr, window, 'borderless', True),
            'widow.borderless = False': Func(setattr, window, 'borderless', False),

            'widow.fullscreen = True': Func(setattr, window, 'fullscreen', True),
            'widow.fullscreen = False': Func(setattr, window, 'fullscreen', False),

            'widow.vsync = True': Func(setattr, window, 'vsync', True),
            'widow.vsync = False': Func(setattr, window, 'vsync', False),

            'application.base.win.request_properties(self)': Func(application.base.win.request_properties, window),

        }, y=0
    )
    startup_value = Text(y=.5, x=-.5)
    startup_value.text = f'''
            position: {window.position}
            size: {window.size}
            aspect_ratio: {window.aspect_ratio}
            window.main_monitor.width: {window.main_monitor.width}
            window.main_monitor.height: {window.main_monitor.height}

        '''

    position_text = Text(y=.5, )
    """
    window.fullscreen = True
    #window.color = color.color(230, 85.71, 21.96)
    #window.color = color.rgb(8, 16, 56)
    #window.color = color.rgb(0.03137255,0.0627451,0.21960784)
    window.color = color.rgb(0.03125,0.0625,0.21875)

    return app

class RectangleObject(Entity):
    def __init__(self, pos, scale):
        super().__init__(
            parent=camera.ui,
            model='quad',
            #size, position, and rotate your image here
            texture = './obj/rectangle_filled.png',
            position = pos,
            scale = scale)

class DataScreen():
    def __init__(self, pos, scale):
        self.rectangle = RectangleObject(pos, scale)
        self.text = Text(text="0", wordwrap=30, origin =(0,0), world_scale = 32*(scale/0.15))
        #self.text.position = (pos[0], pos[1]+0.01, pos[2])
        self.text.position = pos

    def set_text(self, str):
        self.text.text = str

class VerticalAltitude():
    def __init__(self, pos, scale, parent):
        self.anchor = Entity(parent=camera.ui,
            model='quad',
            #size, position, and rotate your image here
            texture = './obj/rectangle_invisible2.png',
            position = pos,
            scale = scale, origin =(0,0))
        self.texts = [Text(text=str(i*100), wordwrap=10, origin =(0,0), world_scale = 120, position = (pos[0]+0.23, pos[1] + i*1.5, pos[2]+1), parent = self.anchor) for i in range(-5, 90)]
        print(len(self.texts))

    def set_height(self, alt_value):
        pos = self.anchor.position_getter()
        #self.anchor.position_setter((pos[0], pos[1], pos[2]))
        self.anchor.position_setter((pos[0], -altitude.alt_value * 0.00225, pos[2]))


class AltitudeMonitor():
    def __init__(self, pos, scale):
        self.screen = DataScreen(pos, scale)
        self.vertical_altitude = VerticalAltitude(pos, scale, self.screen.text)
        self.alt_value = 0

    def set_altitude(self, alt):
        self.alt_value = alt
        self.screen.set_text(str(alt)+'m')

    def update_vertical_display(self):
        self.vertical_altitude.set_height(str(round(self.alt_value,0)))


class RotationMonitor():
    def __init__(self, pos, scale):
        self.screen_roll = DataScreen(pos, scale)
        self.screen_yaw = DataScreen((pos[0]+ 0.1, pos[1], pos[2]), scale)
        self.screen_pitch = DataScreen((pos[0]+ 0.2, pos[1], pos[2]), scale)
        self.tag_roll = Text(text="ROLL", parent=camera.ui,origin =(0,0), scale=scale, world_scale=24)
        self.tag_roll.position = (pos[0], pos[1]+0.05, pos[2])
        self.tag_yaw = Text(text="YAW", parent=camera.ui, origin=(0, 0), scale=scale, world_scale=24)
        self.tag_yaw.position = (pos[0]+ 0.1, pos[1] + 0.05, pos[2])
        self.tag_pitch = Text(text="PITCH", parent=camera.ui, origin=(0, 0), scale=scale, world_scale=24)
        self.tag_pitch.position = (pos[0]+ 0.2, pos[1] + 0.05, pos[2])
        self.roll = 0
        self.yaw = 0
        self.pitch = 0

    def update(self):
        self.screen_roll.set_text(str(self.roll))
        self.screen_yaw.set_text(str(self.yaw))
        self.screen_pitch.set_text(str(self.pitch))

class CoordinatesMonitor():
    def __init__(self, pos, scale):
        self.screen_lat = DataScreen(pos, scale)
        self.screen_lon = DataScreen((pos[0]+ 0.1, pos[1], pos[2]), scale)
        self.tag_lat = Text(text="LAT", parent=camera.ui, origin=(0, 0), scale=scale, world_scale=24)
        self.tag_lat.position = (pos[0], pos[1] + 0.05, pos[2])
        self.tag_lon = Text(text="LON", parent=camera.ui, origin=(0, 0), scale=scale, world_scale=24)
        self.tag_lon.position = (pos[0] + 0.1, pos[1] + 0.05, pos[2])
        self.lat = 0
        self.lon = 0

class VelocityMonitor():
    def __init__(self, pos, scale):
        self.screen_vel = DataScreen(pos, scale)
        self.tag_vel = Text(text="VEL", parent=camera.ui, origin=(0, 0), scale=scale, world_scale=24)
        self.tag_vel.position = (pos[0], pos[1] + 0.05, pos[2])

        self.vel = 0

    def update(self, vel = None):
        if(vel != None):
            self.vel = vel
        self.screen_vel.set_text(str(self.vel))

class MaximaMonitor():
    def __init__(self, pos, scale):
        self.screen_max = DataScreen(pos, scale)
        self.tag_max = Text(text="MAX", parent=camera.ui, origin=(0, 0), scale=scale, world_scale=24)
        self.tag_max.position = (pos[0], pos[1] + 0.05, pos[2])

        self.max = 0

    def update(self, alt):
        if(alt>self.max):
            self.max = alt
            self.screen_max.set_text(str(self.max))

class AccelerationMonitor():
    def __init__(self, pos, scale):
        self.screen_acc = DataScreen(pos, scale)
        self.tag_max = Text(text="ACC", parent=camera.ui, origin=(0, 0), scale=scale, world_scale=24)
        self.tag_max.position = (pos[0], pos[1] + 0.05, pos[2])

        self.acceleration = 0

    def update(self, acc=None):
        if (acc != None):
            self.acc = acc
        self.screen_acc.set_text(str(self.acc))



###Buttons functions

def CSV_button_action():
    print("CSV button clicked")

def start_button_action():
    print("Start button clicked")

def sleep_button_action():
    print("Sleep button clicked")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #altitude_value = 0

    app = launch_app()
    """descr = dedent('''
          <red>Rainstorm<default> <red>Rainstorm<default>
          Summon a rain storm to deal 5 <blue>water<default> damage to everyone, test including yourself.
          1234 1234 1234 1234 1234 1234 2134 1234 1234 1234 1234 1234 2134 2134 1234 1234 1234 1234
          Lasts for 4 rounds.''').strip()

    Text.default_resolution = 2160 * Text.size
    test = Text(text=descr, wordwrap=30)"""



    rocket = RocketObject(model = './obj/saturne5.obj', rotation = (-90 ,0 , 0), scale = 0.5, origin = (0, 0, -3))

    #screen = ScreenObject()


    altitude = AltitudeMonitor((-1/4, 0, 0), 0.15)
    rotation = RotationMonitor((-0.7, 1/3, 0), 0.1)
    coords = CoordinatesMonitor((-0.65, -1/3, 0), 0.1)
    velocity = VelocityMonitor((1/6,0,0), 0.1)
    maxima = MaximaMonitor((0,0,0), 0.1)
    acceleration = AccelerationMonitor((1/3, 0, 0), 0.1)


    ###Buttons
    button_csv = Button(text="CSV", scale=(0.1,0.05), position=(3/6, 0, 0))
    button_csv._on_click = CSV_button_action

    button_start = Button(text="Start", scale=(0.1, 0.05), position=(4 / 6, 0, 0))
    button_start._on_click = start_button_action

    button_sleep = Button(text="Sleep", scale=(0.1, 0.05), position=(5 / 6, 0, 0))
    button_sleep._on_click = sleep_button_action



    #velocity = VelocityMonitor((0, 0, 0), 0.15)
    #altitude.set_text('')
    rocket.position_setter((-5, 0 ,0))
    print(rocket.position_getter())
    rocket.lookAt((10,0,0))
    #print(rocket.position_getter())


    #EditorCamera()
    app.run()
    #mesh = o3d.io.read_triangle_mesh("./obj/saturne5.obj")
    #visualize(mesh)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
