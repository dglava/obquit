#!/usr/bin/env python

# Obquit
# Copyright (C) 2015  dinomol@mail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import configparser
import os.path
import subprocess
import sys

try:
    from gi.repository import Gtk, Gdk
except ImportError:
    print("Python-GObject not found. You need to install it.")
    sys.exit()

try:
    import cairo
except ImportError:
    print("Python-cairo not found. You need to install it.")
    sys.exit()

class OBquit:
    def __init__(self):
        # parse config
        self.parse_config()

        # window attributes
        self.window = Gtk.Window()
        self.window.fullscreen()
        self.window.set_decorated(False)
        self.window.connect("delete-event", Gtk.main_quit)

        self.window_screen = self.window.get_screen()
        self.screen_width = self.window_screen.get_width()
        self.screen_height = self.window_screen.get_height()

        # widget holding all the buttons
        self.button_line = Gtk.Box(
            spacing=10,
            halign=Gtk.Align.CENTER,
            valign=Gtk.Align.CENTER,
            homogeneous=True
            )

        # adds a button/label Box() for each command
        for command in self.commands:
            self.add_button(self.button_line, command[0], command[1])
        # TODO: maybe remove this and add a cancel button to the config
        self.add_button(self.button_line, "cancel")

        # runs the composited version with actual transparency
        # if a compositor is available;
        # TODO: maybe add config option to use the fake one even
        #       with a compositor
        if self.window_screen.is_composited():
           self.run_composited()
        else:
            self.run_fake_transparency()

    def parse_config(self):
        user = os.path.expanduser("~/.config/obquit/obquit.conf")
        system = "/etc/obquit/obquit.conf"

        # a local user config takes precedence
        if os.path.exists(user):
            config_file = user
        elif os.path.exists(system):
            config_file = system
        else:
            # falls back to these defaults
            config_file = None

            self.commands = [
                ("shutdown", "systemctl poweroff"),
                ("suspend", "systemctl suspend"),
                ("logout", "openbox --exit"),
                ("hibernate", "systemctl hibernate"),
                ("reboot", "systemctl reboot")
                ]

            self.opacity = 0.7

        if config_file:
            config = configparser.ConfigParser()
            config.read(config_file)

            # Commands section
            self.commands = []
            for name, command in config["Commands"].items():
                self.commands.append((name, command))

            # Options section
            self.opacity = config.getfloat("Options", "opacity")

    def run_composited(self):
        self.window.set_app_paintable(True)

        # TODO: will probably cause issues if it returns None
        visual = self.window_screen.get_rgba_visual()
        if visual:
            self.window.set_visual(visual)

        self.window.connect(
            "draw",
            self.on_draw_composited,
            self.opacity
            )
        self.window.add(self.button_line)

    def run_fake_transparency(self):
        # widget used to stack wifgets on top of each other
        self.overlay = Gtk.Overlay()
        self.window.add(self.overlay)

        # widget containing a screengrab of the root window
        self.background_img = self.get_background()

        self.shade = Gtk.DrawingArea()
        self.shade.connect("draw", self.on_draw_fake, self.opacity)

        # stacking the background and buttons to achieve
        # fake transparency
        self.overlay.add_overlay(self.background_img)
        self.overlay.add_overlay(self.shade)
        self.overlay.add_overlay(self.button_line)

    def add_button(self, parent, name, command=None):
        # creates a Box() containing a Button() and Label() with
        # the specified name and command
        box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)

        # TODO: probably add icons to buttons or image theme support
        button = Gtk.Button("")
        button.connect("clicked", self.on_click, command)
        label = Gtk.Label()
        label.set_markup(
            "<span fgcolor='white' size='large'>{}</span>".format(name)
            )

        box.pack_start(button, False, False, 0)
        box.pack_start(label, False, False, 0)
        parent.pack_start(box, False, True, 0)

    def on_click(self, widget, command):
        if command:
            subprocess.call(command.split())
        Gtk.main_quit()

    def on_draw_fake(self, widget, cairo_context, opacity):
        # fills the widget with a solid black color and chosen opacity
        cairo_context.set_source_rgba(0, 0, 0, opacity)
        cairo_context.rectangle(
            0, 0,
            self.screen_width, self.screen_height
            )
        cairo_context.fill()

    def on_draw_composited(self, widget, cairo_context, opacity):
        cairo_context.set_source_rgba(0, 0, 0, opacity)
        # copy/pasted; maybe figure out what it actually does
        cairo_context.set_operator(cairo.OPERATOR_SOURCE)
        cairo_context.paint()

    def get_background(self):
        # grabs the window (screenshot)
        root_window = Gdk.get_default_root_window()
        pixbuf = Gdk.pixbuf_get_from_window(
            root_window,
            0, 0,
            self.screen_width, self.screen_height
            )

        return Gtk.Image.new_from_pixbuf(pixbuf)

if __name__ == "__main__":
    app = OBquit()
    app.window.show_all()
    Gtk.main()
