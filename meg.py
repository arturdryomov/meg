#!/usr/bin/env python2

import gtk
import gobject
from time import time
from datetime import datetime


MINUTE_LENGTH = 60
UPDATE_INTERVAL = 10


class Controller():
    def __init__(self):
        self.gui = GUI()
        self.timer = Timer()

    def update(self):
        if self.gui.get_state == "working":
            if time() > self.timer.get_long_rest_time():
                self.gui.call_rest_window()
                self.timer.set_rest_time_ending(time() + self.timer.long_rest_length)
                self.update_rest_window()
                self.timer.update_long_rest_time()
            elif time() > self.timer.get_short_rest_time():
                self.gui.call_rest_window()
                self.timer.set_rest_time_ending(time() + self.timer.short_rest_length)
                self.update_rest_window()
                self.timer.update_short_rest_time()
        gobject.timeout_add_seconds(UPDATE_INTERVAL, self.update)

    def update_rest_window(self):
        if time() > self.timer.get_rest_time_ending():
            self.gui.destroy_rest_window()
            return
        else:
            delta = self.timer.get_rest_time_ending() - time()
            minutes = datetime.fromtimestamp(delta).minute
            seconds = datetime.fromtimestamp(delta).second

            self.gui.set_rest_window_timer("Rest time is " + str(minutes) + ":" + str(seconds))
            gobject.timeout_add_seconds(1, self.update_rest_window)

    def main(self):
        gobject.timeout_add_seconds(UPDATE_INTERVAL, self.update)
        self.gui.main()


class Timer:
    def __init__(self):
        self.short_rest_length = MINUTE_LENGTH * 1
        self.long_rest_length = MINUTE_LENGTH * 5
        self.short_rest_time = time() + MINUTE_LENGTH * 15
        self.long_rest_time = time() + MINUTE_LENGTH * 60
        self.rest_time_ending = time()
    
    def update_short_rest_time(self):
        self.short_rest_time += MINUTE_LENGTH * 15

    def update_long_rest_time(self):
        self.long_rest_time += MINUTE_LENGTH * 60

    def get_short_rest_time(self):
        return self.short_rest_time

    def get_long_rest_time(self):
        return self.long_rest_time

    def set_rest_time_ending(self, rest_time):
        self.rest_time_ending = rest_time

    def get_rest_time_ending(self):
        return self.rest_time_ending


class GUI:
    def __init__(self):
        self.state = "working"
        self.tray_icon = gtk.StatusIcon()
        self.tray_icon.set_from_stock(gtk.STOCK_ABOUT)
        self.tray_icon.set_tooltip('Meg')
        self.tray_icon.set_visible(True)
        self.tray_icon.connect("popup-menu", self.tray_icon_right_click)
        self.tray_icon.connect("activate", self.update_state)

    def get_state(self):
        return self.state

    def update_state(self, dummy):
        if self.state == "working":
            self.state = "idle"
        else:
            self.state = "working"

    def tray_icon_right_click(self, data, event_button, event_time):
        tray_icon_menu = gtk.Menu()
        close_menu_item = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        close_menu_item.connect_object("activate", lambda w: gtk.main_quit(), "Close")
        tray_icon_menu.append(close_menu_item)
        map(lambda i: i.show(), tray_icon_menu)
        tray_icon_menu.popup(None, None, None, event_button, event_time)

    def call_rest_window(self):
        self.rest_window = gtk.Window()
        self.rest_window.set_title("Meg")
        self.rest_window.set_size_request(260, 150)
        self.rest_window.set_position(gtk.WIN_POS_CENTER)

        text_label = gtk.Label("Give yourself a break!")
        self.time_label = gtk.Label("Rest time is 00:00")
        skip_button = gtk.Button("Skip")
        # TODO: Connect skip button with skip action
        skip_button.set_size_request(70, 30)
        
        skip_button_align = gtk.Alignment(0.5, 0.5, 0, 0)
        skip_button_align.add(skip_button)

        rest_window_box = gtk.VBox(True, 5)
        rest_window_box.pack_start(text_label)
        rest_window_box.pack_start(self.time_label)
        rest_window_box.pack_start(skip_button_align)

        self.rest_window.add(rest_window_box)
        self.rest_window.show_all()

    def set_rest_window_timer(self, timer_text):
        self.time_label.set_text(timer_text)

    def destroy_rest_window(self):
        self.rest_window.destroy()

    def main(self):
        gtk.main()


if __name__ == "__main__":
    app = Controller()
    app.main()
