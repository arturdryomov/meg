#!/usr/bin/env python2

""" Provides notifications about having break from working """

import gtk
import gobject
from time import time
from datetime import datetime


class Controller():
    """ Controls work of all classes and work process """

    def __init__(self):
        """ Initialization of own GUI and Timer """
        self.gui = GUI()
        self.timer = Timer()

    def update(self):
        """ Circle of updating, meanwhile controls rest window
            and timer updating """
        if self.gui.get_state() == "working":
            self.update_tray_icon_tooltip()
            # Handle long rest first
            if time() > self.timer.get_long_rest_time():
                self.gui.call_rest_window()
                self.timer.set_rest_time_ending(time() +
                    self.timer.long_rest_length)
                self.update_rest_window()
                self.timer.update_long_rest_time()
            elif time() > self.timer.get_short_rest_time():
                self.gui.call_rest_window()
                self.timer.set_rest_time_ending(time() +
                    self.timer.short_rest_length)
                self.update_rest_window()
                self.timer.update_short_rest_time()
        else:
            # Reinit timer data for currect timing after idle state
            self.timer.init_timer()
        # Check in circle
        gobject.timeout_add_seconds(5, self.update)

    def update_rest_window(self):
        """ Circle of updating rest window, which includes timer widget """
        if time() > self.timer.get_rest_time_ending():
            self.gui.destroy_rest_window()
            return
        else:
            delta = self.timer.get_rest_time_ending() - time()
            self.gui.set_rest_window_timer("Rest time is "
                + self.present_time(delta))
            gobject.timeout_add_seconds(1, self.update_rest_window)

    def update_tray_icon_tooltip(self):
        """ Updating tooltip with timer for next breaks """
        long_breat_delta = self.timer.get_long_rest_time() - time()
        short_break_delta = self.timer.get_short_rest_time() - time()
        # Used Pango Markup
        tooltip_text = "<b>Meg</b>"
        tooltip_text += "\nTime for next breaks"
        tooltip_text += "\nShort: " + self.present_time(short_break_delta)
        tooltip_text += "\nLong: " + self.present_time(long_breat_delta)
        self.gui.update_tray_icon_tooltip(tooltip_text)

    def present_time(self, convertion_time):
        """ Converts time presented as double to string
            in format MM:SS """
        minutes = datetime.fromtimestamp(convertion_time).minute
        seconds = datetime.fromtimestamp(convertion_time).second
        return str(minutes) + ":" + str(seconds)

    def main(self):
        """ Main start working method """
        self.update()
        self.gui.main()


class Timer:
    """ Time manipulating class """

    def __init__(self):
        """ Initialization override """
        self.init_timer()

    def init_timer(self):
        """ Main initialization function for rest length and stuff """
        # For easy debugging
        self.minute_length = 60

        self.short_rest_length = self.minute_length * 1
        self.long_rest_length = self.minute_length * 5
        self.short_rest_time = time() + self.minute_length * 15
        self.long_rest_time = time() + self.minute_length * 60
        self.rest_time_ending = time()

    def update_short_rest_time(self):
        """ Updates short rest time for next rest """
        self.short_rest_time += self.minute_length * 15

    def update_long_rest_time(self):
        """ Updates long rest time for next rest """
        self.short_rest_time += self.minute_length * 15
        self.long_rest_time += self.minute_length * 60

    def get_short_rest_time(self):
        """ Returns short rest time in double format """
        return self.short_rest_time

    def get_long_rest_time(self):
        """ Returns long rest time in double format """
        return self.long_rest_time

    def set_rest_time_ending(self, rest_time):
        """ Sets rest time ending with given rest_time """
        self.rest_time_ending = rest_time

    def get_rest_time_ending(self):
        """ Returns rest time ending in double format """
        return self.rest_time_ending


class GUI:
    """ Windows and other shiny icons class """

    def __init__(self):
        """ Initialization, sets tray icon up """
        self.state = "working"
        self.tray_icon = gtk.StatusIcon()
        self.tray_icon.set_from_stock(gtk.STOCK_YES)
        self.tray_icon.set_tooltip_markup("<b>Meg</b>")
        self.tray_icon.set_visible(True)
        # Signals connection
        self.tray_icon.connect("popup-menu", self.tray_icon_right_click)
        self.tray_icon.connect("activate", self.update_state)

    def get_state(self):
        """ Returs current state of GUI """
        return self.state

    def update_state(self, dummy=None):
        """ Updates state of GUI inversionally """
        if self.state == "working":
            self.state = "idle"
            self.update_tray_icon_tooltip("Meg is idle")
            self.tray_icon.set_from_stock(gtk.STOCK_NO)
        else:
            self.state = "working"
            self.update_tray_icon_tooltip("Meg is working")
            self.tray_icon.set_from_stock(gtk.STOCK_YES)

    def tray_icon_right_click(self, data, event_button, event_time):
        """ Signal nandler for right click """
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
        self.rest_window = gtk.Window()
        self.rest_window.set_title("Meg")
        self.rest_window.set_size_request(260, 150)
        self.rest_window.set_position(gtk.WIN_POS_CENTER)

        text_label = gtk.Label("Give yourself a break!")
        self.time_label = gtk.Label("Rest time is 00:00")
        skip_button = gtk.Button("Skip")
        skip_button.connect("clicked", self.destroy_rest_window)
        skip_button.set_size_request(70, 30)

        # For putting button on center
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
        gtk.main()


# Create application instance and show it
if __name__ == "__main__":
    app = Controller()
    app.main()
