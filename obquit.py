from gi.repository import Gtk, Gdk
import configparser
import os.path
import subprocess

class OBquit:
    def __init__(self):
        # window attributes
        self.window = Gtk.Window()
        self.window.fullscreen()
        self.window.set_decorated(False)
        self.window.connect("delete-event", Gtk.main_quit)

        # parse config
        self.parse_config()

        # widget holding all the buttons
        self.button_line = Gtk.Box(
            spacing=10,
            halign=Gtk.Align.CENTER,
            valign=Gtk.Align.CENTER,
            homogeneous=True
            )
        self.window.add(self.button_line)

        # adds a button/label Box() for each command
        # TODO: replace class att with instance atts Qbit.buttons
        for name in self.config["Commands"]:
            self.add_button(
                self.button_line,
                name,
                self.config.get("Commands", name)
                )
        # adds a cancel button
        self.add_button(self.button_line, "Cancel")

    def add_button(self, parent, name, command=None):
        """
        creates a Box() containing a Button() and Label() with
        the specified name and command
        """
        box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)

        # TODO: add image/theme support for buttons instead of empty label
        button = Gtk.Button("")
        button.connect("clicked", self.on_click, command)
        label = Gtk.Label(name)

        box.pack_start(button, False, False, 0)
        box.pack_start(label, False, False, 0)
        parent.pack_start(box, False, True, 0)

    def on_click(self, widget, command):
        if command:
            subprocess.call(command.split())
        # the Cancel button has no command
        else:
            Gtk.main_quit()

    def parse_config(self):
        # TODO: handle error caused when no user and system wide
        #       config file exists;
        #       add some kind of defaults;
        #       maybe add flag for generating a default config
        user = os.path.expanduser("~/.config/obquit/obquit.conf")
        system = "/etc/obquit/obquit.conf"
        if os.path.exists(user):
            config_file = user
        else:
            config_file = system

        self.config = configparser.ConfigParser()
        self.config.read(config_file)

if __name__ == "__main__":
    app = OBquit()
    app.window.show_all()
    Gtk.main()
