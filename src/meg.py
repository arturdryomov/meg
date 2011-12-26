#!/usr/bin/env python2
# -*- coding: utf-8 -*-


""" Provides notifications about having break from working """


import gtk
import gobject

from datetime import datetime
from time import time
from os.path import dirname, join, realpath


# TODO: Break to separate modules

class Controller():
    """ Controls all classes and work process """

    def __init__(self):
        """ Initialization of own GUI and Timer """

        self.gui = GUI()
        self.timer = Timer()

    def update(self):
        """ Circle of updating, meanwhile controls rest window
            and timer update """

        if self.gui.state == "working":
            # Update tooltip anyway
            self.update_tray_icon_tooltip()

            # Handle long rest first
            if time() > self.timer.long_rest_time:
                self.gui.call_rest_window()

                self.timer.rest_time_ending = (time() +
                    self.timer.long_rest_length)

                self.update_rest_window()

                self.timer.update_long_rest_time()

            elif time() > self.timer.short_rest_time:
                self.gui.call_rest_window()

                self.timer.rest_time_ending = (time() +
                    self.timer.short_rest_length)

                self.update_rest_window()

                self.timer.update_short_rest_time()
        else:
            # Reinit timer data for currect timing after idle state
            self.timer.reinit_timer()

        # Check in circle
        gobject.timeout_add_seconds(5, self.update)

    def update_tray_icon_tooltip(self):
        """ Update tooltip with time for next breaks """

        long_break_delta = self.timer.long_rest_time - time()
        short_break_delta = self.timer.short_rest_time - time()

        # Pango Markup is using for formatting
        tooltip_text = "<b>Meg</b>"
        tooltip_text += "\nTime for next breaks"
        tooltip_text += "\nShort: " + self.present_time(short_break_delta)
        tooltip_text += "\nLong: " + self.present_time(long_break_delta)

        self.gui.update_tray_icon_tooltip(tooltip_text)

    def present_time(self, convertion_time):
        """ Converts time presented as time to string
            in format MM:SS """

        # There are no hours or whatever, just don't need it
        minutes = datetime.fromtimestamp(convertion_time).minute
        seconds = datetime.fromtimestamp(convertion_time).second

        return "{0:02d}:{1:02d}".format(minutes, seconds)

    def update_rest_window(self):
        """ Circle of updating rest window timer """

        if time() > self.timer.rest_time_ending:
            self.gui.destroy_rest_window()
        else:
            delta = self.timer.rest_time_ending - time()

            self.gui.set_rest_window_timer("Rest time is "
                + self.present_time(delta))

            # Update rest window timer (call yourself) once a second
            gobject.timeout_add_seconds(1, self.update_rest_window)

    def main(self):
        """ Main method, starts work """

        self.update()
        self.gui.main()


class Timer:
    """ Time manipulating class """

    def __init__(self):
        """ Main initialization function for rest lengths and stuff """

        # For easy debugging and other planets
        #self.minute_length = 60
        self.minute_length = 5

        self.short_rest_length = self.minute_length * 0.5
        self.long_rest_length = self.minute_length * 3

        self.short_rest_time = time() + self.minute_length * 15
        self.long_rest_time = time() + self.minute_length * 60

        self.rest_time_ending = time()

    def reinit_timer(self):
        """ Reinit timer values """

        self.__init__()

    def update_short_rest_time(self):
        """ Updates short rest time for next rest """

        self.short_rest_time += self.minute_length * 15

    def update_long_rest_time(self):
        """ Updates long rest time for next rest """

        # Don't forget update short rest, it coincides with long rest time
        self.short_rest_time += self.minute_length * 15
        self.long_rest_time += self.minute_length * 60


class GUI:
    """ Windows and other shiny icons class """

    def __init__(self):
        """ Initialization of the interface """

        self.state = "idle"

        self.tray_icon = gtk.StatusIcon()
        self.tray_icon.set_visible(True)
        # Signals connection
        self.tray_icon.connect("activate", self.update_state)
        self.tray_icon.connect("popup-menu", self.tray_icon_right_click)

        self.rest_window = gtk.Window()

        # Timer widget is here, because it's updating is external
        self.time_label = gtk.Label()

    def update_state(self, dummy=None):
        """ Updates state of GUI inversionally """

        if self.state == "working":
            self.state = "idle"
        else:
            self.state = "working"

        self.update_tray_icon_tooltip("<b>Meg</b> is " + self.state)

        # Do not forget to change icon
        self.tray_icon.set_from_file(join(dirname(realpath(__file__)),
            "..", "icons", self.state + ".svg"))

    def tray_icon_right_click(self, data, event_button, event_time):
        """ Signal nandler for right click """

        # Construct menu
        tray_icon_menu = gtk.Menu()
        close_menu_item = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        close_menu_item.connect_object("activate",
            lambda w: gtk.main_quit(), "Close")
        tray_icon_menu.append(close_menu_item)

        # Go threw all menu items and show them
        map(lambda i: i.show(), tray_icon_menu)
        tray_icon_menu.popup(None, None, None, event_button, event_time)

    def update_tray_icon_tooltip(self, tooltip_text):
        """ Updates icon tooltip with tooltip_text in Markup format """

        self.tray_icon.set_tooltip_markup(tooltip_text)

    def call_rest_window(self):
        """ Creates and calls rest window """

        self.rest_window.set_title("Meg")
        self.rest_window.set_size_request(260, 150)
        self.rest_window.set_position(gtk.WIN_POS_CENTER)
        self.rest_window.set_keep_above(True)
        self.rest_window.set_skip_pager_hint(True)
        self.rest_window.set_resizable(False)
        self.rest_window.set_icon_from_file(join(dirname(realpath(__file__)),
            "..", "icons", "working.svg"))

        text_label = gtk.Label("Give yourself a break!")
        skip_button = gtk.Button("Skip")
        skip_button.connect("clicked", self.destroy_rest_window)
        skip_button.set_size_request(70, 30)

        # Put button at center
        skip_button_align = gtk.Alignment(0.5, 0.5, 0, 0)
        skip_button_align.add(skip_button)

        rest_window_box = gtk.VBox(True, 5)
        rest_window_box.pack_start(text_label)
        rest_window_box.pack_start(self.time_label)
        rest_window_box.pack_start(skip_button_align)

        self.rest_window.add(rest_window_box)
        self.rest_window.show_all()

    def set_rest_window_timer(self, timer_text):
        """ Updates timer widget on rest window """

        self.time_label.set_text(timer_text)

    def destroy_rest_window(self, dummy=None):
        """ Kills rest window """

        self.rest_window.destroy()

    def main(self):
        """ Main circle, contains gtk.main() control """

        self.update_state()
        gtk.main()


# Create application instance and run it
if __name__ == "__main__":
    app = Controller()
    app.main()
