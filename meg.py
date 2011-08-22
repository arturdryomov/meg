#!/usr/bin/env python2

import gtk
import gobject
from time import time


MINUTE_LENGTH = 6
UPDATE_INTERVAL = 1


class Controller:
    def __init__(self):
        self.state = "working"
        self.gui = GUI()
        self.timer = Timer()

    def update(self):
        if self.state == "working":
            if time() > self.timer.get_long_rest_time():
                self.gui.call_rest_window(time() + self.timer.long_rest_length)
                self.timer.update_long_rest_time()
            elif time() > self.timer.get_short_rest_time():
                self.gui.call_rest_window(time() + self.timer.short_rest_length)
                self.timer.update_short_rest_time()
        gobject.timeout_add_seconds(UPDATE_INTERVAL, self.update)

    def main(self):
        gobject.timeout_add_seconds(UPDATE_INTERVAL, self.update)
        self.gui.main()


class Timer:
    def __init__(self):
        self.short_rest_length = MINUTE_LENGTH * 1
        self.long_rest_length = MINUTE_LENGTH * 5
        self.short_rest_time = time() + MINUTE_LENGTH * 15
        self.long_rest_time = time() + MINUTE_LENGTH * 60
    
    def update_short_rest_time(self):
        self.short_rest_time += MINUTE_LENGTH * 15

    def update_long_rest_time(self):
        self.long_rest_time += MINUTE_LEGNTH * 60

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
        map(lambda i: i.show(), tray_icon_menu)
        tray_icon_menu.popup(None, None, None, event_button, event_time)

    def call_rest_window(self, rest_time):
        rest_window = gtk.Window()
        rest_window.set_position(gtk.WIN_POS_CENTER)
        rest_window.set_border_width(10)
        label = gtk.Label("Meg")
        rest_window.add(label)
        rest_window.show_all()

        def update_window_state():
            if time() > rest_time:
                rest_window.destroy()
                return
            else:
                gobject.timeout_add_seconds(UPDATE_INTERVAL, update_window_state)
        gobject.timeout_add_seconds(UPDATE_INTERVAL, update_window_state)

    def main(self):
        gtk.main()


if __name__ == "__main__":
    app = Controller()
    app.main()
