#!/usr/bin/env python2

import gtk
import gobject
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
        gobject.timeout_add_seconds(30, self.update)

    def main(self):
        self.gui.main()
        gobject.timeout_add_seconds(30, self.update)


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
        self.tray_icon.connect("popup-menu", self.tray_icon_right_click)

    def tray_icon_right_click(self, data, event_button, event_time):
        tray_icon_menu = gtk.Menu()
        close_menu_item = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        close_menu_item.connect_object("activate", lambda w: gtk.main_quit(), "Close")
        tray_icon_menu.append(close_menu_item)
        #close_menu_item.show()
        map(lambda i: i.show(), tray_icon_menu)
        tray_icon_menu.popup(None, None, None, event_button, event_time)

    def call_short_rest_window(self):
        pass

    def call_long_rest_window(self):
        pass

    def main(self):
        gtk.main()


if __name__ == "__main__":
    app = Controller()
    app.main()
