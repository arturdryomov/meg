#!/usr/bin/env python2

import gtk
from time import time


class Controller:
    def __init__(self):
        self.state = "working"
        self.gui = GUI()
        self.timer = Timer()

    def update(self):
        if state == "working":
            if time() > timer.get_long_rest_time():
                gui.call_long_rest_window()
                timer.update_long_rest_time()
            elif time() > timer.get_short_rest_time():
                gui.call_short_rest_window()
                timer.update_short_rest_time()

    def main(self):
        self.gui.main()


class Timer:
    def __init__(self):
        self.short_rest_time = time() + 60 * 15
        self.long_rest_time = time() + 60 * 60
    
    def update_short_rest_time(self):
        self.short_rest_time += 60 * 15

    def update_long_rest_time(self):
        self.long_rest_time += 60 * 60

    def get_short_rest_time(self):
        return self.short_rest_time

    def get_long_rest_time(self):
        return self.long_rest_time


class GUI:
    def __init__(self):
        self.tray_icon = gtk.StatusIcon()
        self.tray_icon.set_from_stock(gtk.STOCK_ABOUT)
        self.tray_icon.set_tooltip('Meg')
        self.tray_icon.set_visible(True)

    def call_short_rest_window(self):
        pass

    def call_long_rest_window(self):
        pass

    def main(self):
        gtk.main()


if __name__ == "__main__":
    app = Controller()
    app.main()
