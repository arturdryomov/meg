import gtk


class Controller:
    def __init__(self):
        self.state = "working"
        self.gui = GUI()

    def main(self):
        self.gui.main()


class GUI:
    def __init__(self):
        self.tray_icon = gtk.StatusIcon()
        self.tray_icon.set_from_stock(gtk.STOCK_ABOUT)
        self.tray_icon.set_tooltip('Meg')
        self.tray_icon.set_visible(True)

    def main(self):
        gtk.main()


if __name__ == "__main__":
    app = Controller()
    app.main()
