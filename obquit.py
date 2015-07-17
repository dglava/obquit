#!/usr/bin/env python

from gi.repository import Gtk, Gdk
import configparser
import os.path
import subprocess
import cairo

class OBquit:
    def __init__(self):
        # parse config
        self.parse_config()

        # window attributes
        self.window = Gtk.Window()
        self.window.fullscreen()
        self.window.set_decorated(False)
        self.window.connect("delete-event", Gtk.main_quit)

        self.get_resolution()

        # widget used to stack wifgets on top of each other
        self.overlay = Gtk.Overlay()
        self.window.add(self.overlay)

        # widget containing a screengrab of the root window
        self.background_img = self.get_background()

        self.shade = Gtk.DrawingArea()
        self.shade.connect("draw", self.on_draw)

        # widget holding all the buttons
        self.button_line = Gtk.Box(
            spacing=10,
            halign=Gtk.Align.CENTER,
            valign=Gtk.Align.CENTER,
            homogeneous=True
            )

        # stacking the background and buttons to achieve
        # fake transparency
        self.overlay.add_overlay(self.background_img)
        self.overlay.add_overlay(self.shade)
        self.overlay.add_overlay(self.button_line)

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

    def on_draw(self, widget, cairo_context):
        cairo_context.set_source_rgba(0, 0, 0, 0.5)
        cairo_context.rectangle(
            0, 0,
            self.screen_width, self.screen_height
            )
        cairo_context.fill()

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

    def get_resolution(self):
        self.root_window = Gdk.get_default_root_window()
        self.screen_width = self.root_window.get_width()
        self.screen_height = self.root_window.get_height()

    def get_background(self):
        # grabs the window (screenshot)
        pixbuf = Gdk.pixbuf_get_from_window(
            self.root_window,
            0, 0,
            self.screen_width, self.screen_height
            )

        return Gtk.Image.new_from_pixbuf(pixbuf)

if __name__ == "__main__":
    app = OBquit()
    app.window.show_all()
    Gtk.main()
